#!/bin/bash



setup(){
  HASHID=$(git log | grep commit | head -1 | awk -F " " '{print substr($2,1,8)}')
  echo 'Model Hash ID :' ${HASHID}
  STMPDIR="/scratch4/NCEPDEV/stmp4/${USER}/${HASHID}"
  PTMPDIR="/scratch4/NCEPDEV/stmp3/${USER}/${HASHID}"
}

run_model(){
  cp ${CONFIG_FILE} regression_${CONFIG_FILE}
  export CONFIG_FILE=regression_${CONFIG_FILE}
  # Modify the config file so that the JOBNAME corresponds to the hash id
  sed -i '/JOBNAME/c\export JOBNAME='${HASHID} ${CONFIG_FILE}
  if [[ `grep REGRESSION ${CONFIG_FILE} | wc -l` == "0" ]] ; then
    echo "export REGRESSION=YES" >> $CONFIG_FILE
  fi
  # Submit the job and pipe the output to a temporary file
  ./submit.sh ${CONFIG_FILE} 1 ${NCYCLES}
  rm -rf ${CONFIG_FILE}
}

# ----- Parse through command line options ----- #
HELP="no"
POSITIONAL=()

if [ $# -eq 0 ]; then
    HELP="yes"
fi

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -r|--regression-config)
    export CONFIG_FILE="$2"
    shift # past argument
    shift # past value
    ;;
    -h|--help)
    HELP="yes"
    shift # past argument
    shift # past value
    ;;
    -n|--ncycles)
    NCYCLES="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

echo ${CONFIG_FILE}
if [ -z "$CONFIG_FILE" ]; then
  HELP="yes"
fi

if [ -z "$NCYCLES" ]; then
  NCYCLES=1
fi

if [ "${HELP}" = "yes" ]; then
  echo 'Usage: ./handle_regressions.sh [options]'
  echo '  Options:'
  echo '    -h   | --help '
  echo '        Display this help message '
  echo ' '
  echo '    -r  <config-file>   | --regression-config <config-file>'
  echo '        Sets which base regression test config file to use'
  echo '        This option is required'
  echo ' '
  echo '    -n  <number of cycles>   | --ncycles <number of cycles>'
  echo '        Sets the number of forecast cycles to run for the test'
  echo ' '
  echo ' --------------------------------------------------------------------- '
  echo ' '
  echo ' Suggested Usage: '
  echo '    Run the coupled_20130316 test case for five cycles. This attempts'
  echo '    5 days of model forecasts through 1 day forecasts with restarts. '
  echo ' '
  echo '      ./handle_regressions.sh -r coupled_20130316.config -n 5        '
  echo ' '
  echo ' --------------------------------------------------------------------- '

fi

# ----- Parse through command line options ----- #


if [ "${HELP}" = "no" ]; then
  setup
  run_model
fi


