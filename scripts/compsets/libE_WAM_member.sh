#!/bin/bash

base_job_name=ensemble_
input_address=/glade/work/felixn/noscrub/ensemble_test/wam_input_2.csv

ptmp=/glade/work/$USER/scrub/ptmp

#for i in $(seq 0 $((members-1))) ; do
# mem should be input, same for MAXCOUNT
#mem=$(printf %02d $i)
mem=$(printf %02d $1)

COUNT=1 
MAXCOUNT=$1
while IFS=, read col1 col2; do
    (( COUNT++ ))
    if (( COUNT -1 < MAXCOUNT )); then
      # Continue if we haven't hit the line yet
      continue
    fi
    if (( COUNT - 1 > MAXCOUNT )); then
      #If we've passed the line, we're done
      break
    fi
done < ${input_address}   
  
if ((COUNT-1 < MAXCOUNT )); then 
    # Warn if we ran out of parameter combinations in the file
    echoComment "Reached end of parameter file ${input_address}. Ending Script"
    exit
fi
  
#echo "Member $i has F10p7 ${col2} and kp ${col1}"

export JOBNAME=${libE_JOBNAME}/${base_job_name}mem${mem}  
export F10p7=${col2}
export kp=${col1}

#job_dir=${ptmp}/${JOBNAME}
#mkdir -p $job_dir
#cd $job_dir

mkdir -p libE_mem_config
envsubst '${JOBNAME} ${F10p7} ${kp}' < cheyenne_libE.config > libE_mem_config/mem_${mem}.config

#./submit.sh mem_${mem}.config 1 $cycles
./libE_WAM_submit.sh libE_mem_config/mem_${mem}.config ${mem}

#rm -rf mem_${mem}.config
#done
