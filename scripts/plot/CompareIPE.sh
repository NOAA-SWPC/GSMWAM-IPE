#!/bin/bash
#set -ax
# ********* Settings that you should modify ********* #

# Set the path to the base WAM-IPE directory (containing IPELIB)
WAMIPEDIR=`pwd`/../..

# Set the path to the directory where reference netcdf output can be found
REFDIR="/scratch3/NCEPDEV/swpc/noscrub/Joseph.Schoonover/bug_check/before_vector_regridding/netcdf/"
# Set the path to where your netcdf output can be found that you want to compare against the reference data.
IPEDIR="/scratch3/NCEPDEV/swpc/noscrub/Joseph.Schoonover/bug_check/merged_vector_regridding/netcdf/"
# Set the path to where you want the difference file.
OUTDIR="/scratch3/NCEPDEV/swpc/noscrub/Joseph.Schoonover/bug_check/merged_vector_regridding/netcdf_diff/"

# *************************************************** #

# //////////////////////////////////////////////////////////////////////// #
# Do not modify below this point unless you really know what you are doing
# //////////////////////////////////////////////////////////////////////// #

# Build the i2hg executable
module purge
module load intel netcdf nco

CompareStates (){

# Extract the file name without the path
filename=$(echo $1 | awk -F / '{print $NF}')

# Take the difference of the two netcdf files passed in
# and store the output in a temporary file (diff.nc)
ncdiff -O $1 $2 diff.nc

# Use the ncap script to compute absolute max and rms difference
ncap2 -v -O -S ncapOperations.nco diff.nc ${3}${filename}

return 0

}

[ ! -d $OUTDIR ]  && mkdir -p $OUTDIR

for file in ${REFDIR}IPE_State.*.nc
do

  filename=$(echo $file | awk -F / '{print $NF}')

  if [ -e $IPEDIR/$filename ]
  then

    CompareStates $file $IPEDIR/$filename $OUTDIR

  fi
  
done



