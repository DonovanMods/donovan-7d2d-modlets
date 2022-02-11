#!/bin/sh

BASE="https://github.com/donovan522/donovan-7d2d-modlets/tree/stable"

for D in $(ls -d donovan-*); do
  echo "${BASE}/${D}"
done
