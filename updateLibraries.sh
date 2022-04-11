#!/bin/bash

# To be ran from station-validation

#[start] properly launch conda enviornment into the local bash (to avoid permission denied with current bash shell opened in command terminal)
source /nrn/home/NRN/haissa/.conda/envs/stationverification/bin/activate
conda activate base
#[end] properly launch conda enviornment into the local bash (to avoid permission denied with current bash shell opened in command terminal)

# [start] clean the build directories
rm -rf dist/
rm -rf ../ISPAQ/ispaq/dist/
# [end] clean the build directories

# [start] build station and packages
python -m build
pip3 install ./dist/stationverification-3.1.2.tar.gz 
cd ../ISPAQ/ispaq 
python -m build
pip3 install dist/cmdline-ispaq-3.1.0b0.tar.gz
# [end] build packages


