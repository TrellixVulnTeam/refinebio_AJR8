import os
import shutil
import urllib.request
from contextlib import closing

from data_refinery_common.enums import ProcessorPipeline
from data_refinery_common.logging import get_and_configure_logger
from data_refinery_common.message_queue import send_job
from data_refinery_common.models import (
    DownloaderJob,
    DownloaderJobOriginalFileAssociation,
    OriginalFile,
    ProcessorJob,
    ProcessorJobOriginalFileAssociation,
)
from data_refinery_common.utils import get_env_variable
from data_refinery_workers.downloaders import utils

logger = get_and_configure_logger(__name__)
LOCAL_ROOT_DIR = get_env_variable("LOCAL_ROOT_DIR", "/home/user/data_store")
CHUNK_SIZE = 1024 * 256  # chunk_size is in bytes


def _download_file(download_url: str, file_path: str, job: DownloaderJob) -> DownloaderJob:
    """Download the file via FTP.

    I spoke to Erin from Ensembl about ways to improve this. They're looking into it,
    but have decided against adding an Aspera endpoint.

    She suggested using `rsync`, we could try shelling out to that.

    """
    try:
        logger.debug(
            "Downloading file from %s to %s.", download_url, file_path, downloader_job=job.id
        )
        urllib.request.urlcleanup()
        target_file = open(file_path, "wb")
        with closing(urllib.request.urlopen(download_url)) as request:
            shutil.copyfileobj(request, target_file, CHUNK_SIZE)

        # Ancient unresolved bug. WTF python: https://bugs.python.org/issue27973
        urllib.request.urlcleanup()
    except Exception:
        failure_template = "Exception caught while downloading file from: %s"
        logger.exception(failure_template, download_url, downloader_job=job.id)
        job.failure_reason = failure_template % download_url
        job.success = False
        return job
    finally:
        target_file.close()

    job.success = True
    return job


def download_transcriptome(job_id: int) -> None:
    """The main function for the Transcriptome Index Downloader.

    Two files are needed for the Transcriptome Index Downloader: a
    fasta file and a gtf file. However each pair need to be processed
    into two different sized indices. (See the
    processors.transcriptome_index._create_index function's docstring
    for more info.) Therefore we only download each set once, then
    let each processor find it in the same location.
    """
    job = utils.start_job(job_id)

    file_assocs = DownloaderJobOriginalFileAssociation.objects.filter(downloader_job=job)
    long_files_to_process = []
    short_files_to_process = []

    for assoc in file_assocs:
        long_original_file = assoc.original_file

        if long_original_file.is_archive:
            filename_species = "".join(long_original_file.source_filename.split(".")[:-2])
        else:
            # Does this ever happen?
            filename_species = "".join(long_original_file.source_filename.split(".")[:-1])

        # First download the files and make the original files for the
        # long transciptome index.
        long_dir = os.path.join(LOCAL_ROOT_DIR, filename_species + "_long")
        os.makedirs(long_dir, exist_ok=True)
        long_dl_file_path = os.path.join(long_dir, long_original_file.source_filename)
        job = _download_file(long_original_file.source_url, long_dl_file_path, job)

        if not job.success:
            break

        long_original_file.is_downloaded = True
        long_original_file.absolute_file_path = long_dl_file_path
        long_original_file.filename = long_original_file.source_filename
        long_original_file.has_raw = True
        long_original_file.calculate_size()
        long_original_file.calculate_sha1()
        long_original_file.save()
        long_files_to_process.append(long_original_file)

        # Next copy the files to another directory and create the
        # original files for the short transcriptome index.
        short_dir = os.path.join(LOCAL_ROOT_DIR, filename_species + "_short")
        os.makedirs(short_dir, exist_ok=True)
        short_dl_file_path = os.path.join(short_dir, long_original_file.source_filename)
        shutil.copyfile(long_dl_file_path, short_dl_file_path)

        short_original_file = OriginalFile(
            source_filename=long_original_file.source_filename,
            source_url=long_original_file.source_url,
            is_downloaded=True,
            absolute_file_path=short_dl_file_path,
            filename=long_original_file.filename,
            has_raw=True,
        )
        short_original_file.calculate_size()
        short_original_file.calculate_sha1()
        short_original_file.save()
        short_files_to_process.append(short_original_file)

    if job.success:
        logger.debug("Files downloaded successfully.", downloader_job=job_id)

        create_long_and_short_processor_jobs(job, long_files_to_process, short_files_to_process)

    utils.end_downloader_job(job, job.success)


def create_long_and_short_processor_jobs(
    downloader_job, long_files_to_process, short_files_to_process
):
    """Creates two processor jobs for the files needed for this transcriptome"""

    processor_job_long = ProcessorJob()
    processor_job_long.downloader_job = downloader_job
    processor_job_long.pipeline_applied = "TRANSCRIPTOME_INDEX_LONG"
    processor_job_long.ram_amount = 4096
    processor_job_long.save()

    for original_file in long_files_to_process:

        assoc = ProcessorJobOriginalFileAssociation()
        assoc.original_file = original_file
        assoc.processor_job = processor_job_long
        assoc.save()

    try:
        send_job(ProcessorPipeline[processor_job_long.pipeline_applied], processor_job_long)
    except Exception:
        # This is fine, the foreman will requeue these later.
        logger.exception("Problem with submitting a long transcriptome index job.")

    processor_job_short = ProcessorJob()
    processor_job_short.downloader_job = downloader_job
    processor_job_short.pipeline_applied = "TRANSCRIPTOME_INDEX_SHORT"
    processor_job_short.ram_amount = 4096
    processor_job_short.save()

    for original_file in short_files_to_process:

        assoc = ProcessorJobOriginalFileAssociation()
        assoc.original_file = original_file
        assoc.processor_job = processor_job_short
        assoc.save()

    try:
        send_job(ProcessorPipeline[processor_job_short.pipeline_applied], processor_job_short)
    except Exception:
        # This is fine, the foreman will requeue these later.
        logger.exception("Problem with submitting a long transcriptome index job.")
