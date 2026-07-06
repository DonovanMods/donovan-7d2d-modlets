#!/usr/bin/bash

# This script creates the zip files for the release.
#
# Archives are recreated from scratch each run so that files deleted or
# renamed in a modlet never linger inside a previously-built ZIP.

ZIP_DIR="${PWD}/ZIPs"

create_zips() {
  for f in "${1}"/donovan-*/; do
    if [ -d "$f" ]; then
      dir_name=$(dirname "$f")
      mod_name=$(basename "$f")
      zip_file="${ZIP_DIR}/${mod_name}.zip"

      echo "Compressing $mod_name"
      rm -f "$zip_file"

      if command -v zip >/dev/null 2>&1; then
        (cd "$dir_name" && zip -rq "$zip_file" "$mod_name")
      else
        (cd "$dir_name" && bsdtar --format zip -cf "$zip_file" "$mod_name")
      fi
    fi
  done
}

[[ "$1" == "--clean" ]] && rm -fv "${ZIP_DIR}"/*.zip

create_zips modlets
create_zips modlets/a-la-carte

exit 0
