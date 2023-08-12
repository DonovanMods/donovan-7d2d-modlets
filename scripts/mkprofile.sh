#!/bin/sh

BASE="https://github.com/DonovanMods/donovan-7d2d-modlets/tree/stable"

for D in $(ls -d modlets/donovan-* modlets/**/donovan-*); do
  echo "${BASE}/${D}"
done
