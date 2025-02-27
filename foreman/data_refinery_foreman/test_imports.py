from django.test import TestCase, tag


class ImportTestCase(TestCase):
    def test_imports(self):
        # Make sure we can import the foreman tests
        import data_refinery_foreman.foreman.management.commands.check_computed_files
        import data_refinery_foreman.foreman.management.commands.check_missing_results
        import data_refinery_foreman.foreman.management.commands.correct_affy_cdfs
        import data_refinery_foreman.foreman.management.commands.create_compendia
        import data_refinery_foreman.foreman.management.commands.create_missing_downloader_jobs
        import data_refinery_foreman.foreman.management.commands.create_missing_processor_jobs
        import data_refinery_foreman.foreman.management.commands.create_quantpendia
        import data_refinery_foreman.foreman.management.commands.feed_the_beast
        import data_refinery_foreman.foreman.management.commands.fix_compendia
        import data_refinery_foreman.foreman.management.commands.generate_dataset_report
        import data_refinery_foreman.foreman.management.commands.get_job_to_be_run
        import data_refinery_foreman.foreman.management.commands.get_quant_sf_size
        import data_refinery_foreman.foreman.management.commands.import_external_sample_attributes
        import data_refinery_foreman.foreman.management.commands.import_external_sample_keywords
        import data_refinery_foreman.foreman.management.commands.import_ontology
        import data_refinery_foreman.foreman.management.commands.mark_samples_unprocessable
        import data_refinery_foreman.foreman.management.commands.organism_shepherd
        import data_refinery_foreman.foreman.management.commands.remove_dead_computed_files
        import data_refinery_foreman.foreman.management.commands.rerun_salmon_old_samples
        import data_refinery_foreman.foreman.management.commands.retry_jobs
        import data_refinery_foreman.foreman.management.commands.retry_samples
        import data_refinery_foreman.foreman.management.commands.retry_timed_out_jobs
        import data_refinery_foreman.foreman.management.commands.run_tximport
        import data_refinery_foreman.foreman.management.commands.stop_jobs
        import data_refinery_foreman.foreman.management.commands.test_correct_affy_cdfs
        import data_refinery_foreman.foreman.management.commands.test_create_compendia
        import data_refinery_foreman.foreman.management.commands.test_create_missing_downloader_jobs
        import data_refinery_foreman.foreman.management.commands.test_create_missing_processor_jobs
        import data_refinery_foreman.foreman.management.commands.test_create_quantpendia
        import data_refinery_foreman.foreman.management.commands.test_import_external_sample_attributes
        import data_refinery_foreman.foreman.management.commands.test_import_external_sample_keywords
        import data_refinery_foreman.foreman.management.commands.test_organism_shepherd
        import data_refinery_foreman.foreman.management.commands.test_rerun_salmon_old_samples
        import data_refinery_foreman.foreman.management.commands.test_retry_samples
        import data_refinery_foreman.foreman.management.commands.test_run_tximport
        import data_refinery_foreman.foreman.management.commands.test_update_experiment_metadata
        import data_refinery_foreman.foreman.management.commands.update_downloadable_samples
        import data_refinery_foreman.foreman.management.commands.update_experiment_metadata
        import data_refinery_foreman.foreman.management.commands.update_sample_metadata
        import data_refinery_foreman.foreman.test_downloader_job_manager
        import data_refinery_foreman.foreman.test_end_to_end
        import data_refinery_foreman.foreman.test_job_control
        import data_refinery_foreman.foreman.test_job_requeuing
        import data_refinery_foreman.foreman.test_processor_job_manager
        import data_refinery_foreman.foreman.test_survey_job_manager
        import data_refinery_foreman.foreman.test_utils
        import data_refinery_foreman.surveyor.management.commands.test_unsurvey
        import data_refinery_foreman.surveyor.test_array_express
        import data_refinery_foreman.surveyor.test_external_source
        import data_refinery_foreman.surveyor.test_geo
        import data_refinery_foreman.surveyor.test_harmony
        import data_refinery_foreman.surveyor.test_sra
        import data_refinery_foreman.surveyor.test_surveyor
        import data_refinery_foreman.surveyor.test_transcriptome_index
