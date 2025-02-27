#!/bin/bash

# Reintializes the database so there's no data or migrations run against it.


# This script should always run as if it were being called from
# the directory it lives in.
script_directory="$(perl -e 'use File::Basename;
 use Cwd "abs_path";
 print dirname(abs_path(@ARGV[0]));' -- "$0")"
cd "$script_directory" || exit

# Clear it out.
docker rm -f drdb
echo "sudo is required to delete the existing postgres volume because Docker."
sudo rm -r ../volumes_postgres

# Get it goin' again.
./run_postgres.sh
sleep 10
./install_db_docker.sh
./update_models.sh
