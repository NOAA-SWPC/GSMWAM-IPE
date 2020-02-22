#!/bin/bash
#set -ax
# ********* Settings that you should modify ********* #
# Set the path to the directory where your IPE output can be found
IPE_RUNDIR="/scratch4/NCEPDEV/stmp4/Joseph.Schoonover/ipe_refactor_test014/"


# Set the path to where you want the eps files and the Latex file.
# *************************************************** #

# //////////////////////////////////////////////////////////////////////// #
# Do not modify below this point unless you really know what you are doing
# //////////////////////////////////////////////////////////////////////// #

# Set the path to the base WAM-IPE directory (containing IPELIB)
WAMIPEDIR=${1:-`pwd`/../..}

# Clean house first, just in case
rm -rf tmp*

# Build the i2hg executable
module purge
module load intel/18.1.163 impi/5.1.2.150 hdf5parallel/1.8.14 netcdf-hdf5parallel/4.4.0
TASKS=2

# Make the output and plot directories if they don't already exist
PLOTDIR="$IPE_RUNDIR/plots"
[ ! -d $PLOTDIR ] && mkdir -p $PLOTDIR


## Create job file.
tmp=tmp_job.sh
touch $tmp
chmod +x $tmp

cat >> $tmp << EOF
#!/bin/bash --login
#
#PBS -l procs=$TASKS
#PBS -l walltime=00:05:00
#PBS -q debug
#PBS -A swpc
#PBS -N convert_ipe
#PBS -j oe
set -ax
#
# change directory to the working directory of the job
# Use the if clause so that this script stays portable
#

if [ x\$PBS_O_WORKDIR != x ]; then
   cd \$PBS_O_WORKDIR
fi
cp plot_settings.yaml $IPE_RUNDIR

module purge
module load intel/18.1.163 impi/5.1.2.150 hdf5parallel/1.8.14 netcdf-hdf5parallel/4.4.0
cd $IPE_RUNDIR
ls $IPE_RUNDIR/IPE_State.apex.*.h5 > h5list
mpirun -np 1 $WAMIPEDIR/IPELIB/bin/ipe_postprocess input h5list


# Start plotting routine
module use -a /contrib/modulefiles
module load anaconda
#
## Run the matlab plotting script
python $WAMIPEDIR/scripts/plot/plot.py -i ./ -o $PLOTDIR

exit 0
EOF

qsub $tmp
