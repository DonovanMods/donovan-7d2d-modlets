#!/usr/bin/bash

create_zips() {
  for f in $(ls -d ${1}/donovan-*); do
    if [ -d "$f" ]; then
      dir_name=$(dirname $f)
      mod_name=$(basename $f)
      zip_file="${ZIP_DIR}/${mod_name}.zip"

      echo "Compressing $mod_name"

      (cd "$dir_name" && zip -rq "$zip_file" "$mod_name")
    fi
  done
}

# This script creates the zip files for the release.
ZIP_DIR="${PWD}/ZIPs"

create_zips modlets || exit $?
create_zips modlets/a-la-carte || exit $?
create_zips modlets/optional || exit $?

exit 0
