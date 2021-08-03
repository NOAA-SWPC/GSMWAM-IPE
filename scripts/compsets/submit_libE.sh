#!/bin/bash

# Submit WAM-IPE with libEnsemble.
# Prepares libE jobcard with job submission details plundered from cheyenne.config and config/cheyenne.config.  
# Presently setup for wamStandalone 

# Total nodes for parallel forecast members (1 node is needed for libE manager). 
libE_nodes=3 
# Total wallclock time for entire ensemble
libE_wallclock=00:20:00
# Number of libE workers (If one simulation runs per node, n_workers = libE_nodes -1)
n_workers=2
# Number of ensemble members/simulations (typically a multple of workers)
n_sim=4

export JOBNAME=libE_test11

## Check WAM configuration
pwd=$(pwd)
bn=$(basename $1)

## set restart
export cycle=${2:-1}
if [[ $cycle == 1 ]] ; then
  export RESTART=.false.
else
  export RESTART=.true.
fi

export libE_JOBNAME=$JOBNAME 

## Save environment prior to configuration - we don't want exported variables to interfer with member configurations
blacklisted () {
    case $1 in
        PWD|OLDPWD|SHELL|STORAGE|SCHEDULER_SUB|libE_JOBNAME) return 0 ;;
        *) return 1 ;;
    esac
}

env_save () { # Assume "$STORAGE/#1.sh" is empty
    local VAR
    for VAR in $(compgen -A export); do
        blacklisted $VAR || \
            echo "export $VAR='${!VAR}'" >> "$STORAGE/$1.sh"
    done
}

env_restore () {
    local VAR
    for VAR in $(compgen -A export); do
        blacklisted $VAR || \
            unset $VAR
    done
    source "$STORAGE/$1.sh"
}

export STORAGE=$PWD
env_save

## source config
CONFIG=$( echo $bn | cut -d'.' -f 1 )
. $pwd/config/workflow.sh $1

if [ $? != 0 ]; then echo "setup failed, exit"; exit; fi

NODES=$libE_nodes
## PBS stuff
SCHEDULER_SUB=${SCHEDULER_SUB:-'qsub'}
SCHEDULER=${SCHEDULER:-'#PBS'}
SUBFLAG1=${SUBFLAG1:-'$SCHEDULER -N ${JOBNAME}'}
SUBFLAG2=${SUBFLAG2:-'$SCHEDULER -A ${ACCOUNT}'}
SUBFLAG3=${SUBFLAG3:-'$SCHEDULER -l walltime=${WALLCLOCK}'}
SUBFLAG4=${SUBFLAG4:-'$SCHEDULER -o ${ROTDIR}/'}
SUBFLAG5=${SUBFLAG5:-'$SCHEDULER -j oe'}
SUBFLAG6=${SUBFLAG6:-'$SCHEDULER -l select=${NODES}:ncpus=${TASKPN}:mpiprocs=${TASKPN}'}
SUBFLAG7=${SUBFLAG7:-'$SCHEDULER -q ${QUEUE}'}
SUBFLAG8=${SUBFLAG8:-'$SCHEDULER -W umask=022'}

## create job file
tmp=temp_libE_job.sh
rm -rf $tmp
touch $tmp
chmod +x $tmp

## cp config to $ROTDIR if $cycle == 1
if [[ $cycle == 1 ]] || [[ ! -f $ROTDIR/$1 ]] ; then
         cp $1 $ROTDIR/.
fi

## Note ROTDIR to save $tmp at end
libE_ROTDIR=$ROTDIR
libE_cycle=$cycle

## set up PBS/LSF/whatever
echo "#!/bin/bash" > $tmp
# the below is a little hacky but it sure works
d=0
while
        d=$((d+1))
        eval SUBFLAG=\$SUBFLAG$d
        [[ -n "$SUBFLAG" ]]
do
        echo `eval echo $SUBFLAG` >> $tmp
done

# Make ROTDIR prior to job submission, so that if job waits in queue the jobscript is still successfully moved to $ROTDIR
mkdir -p $ROTDIR

## calling_func.py
cat >> $tmp << 'EOF'

# conda environment with python 3.6.12 and libEnsemble
export PATH="/glade/work/felixn/anaconda3/bin:$PATH"
source activate myenv

## remove repeated nodes from node_list
cat $PBS_NODEFILE | uniq > node_list
## remove first node from node_list file
sed -i 1d node_list
EOF

cat >> $tmp << EOF
# setup ensemble directory RUNDIR and ROTDIR (clean up from the configure check)
rm -rf $RUNDIR
mkdir -p $RUNDIR

python libE_calling_func.py $n_workers $n_sim
EOF

cat >> $tmp << 'EOF'
exit $status
EOF

env_restore

#./$tmp
$SCHEDULER_SUB <$tmp
mv $tmp $libE_ROTDIR/jobcard_libE_$libE_cycle
