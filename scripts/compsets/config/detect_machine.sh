#!/bin/bash
### basically the idea is to just check if directories exist that are specific to certain machines

if [[ -e /gpfs/hps && -e /usrx ]] ; then
	MACHINE_ID=wcoss
	if [[ -d /usrx && -d /global && -e /etc/redhat-release && \
	-e /etc/prod ]] ; then
		# We are on WCOSS Phase 1 or 2.
		if ( ! cat /proc/cpuinfo |grep 'processor.*32' ) ; then
			# Fewer than 32 fake (hyperthreading) cpus, so Phase 1.
			FMID=wcoss.phase1
			export BUILD_TARGET=wcoss_phase1
			PEX=1
		else
			# phase 2
			FMID=wcoss.phase2
			export BUILD_TARGET=wcoss_phase2
			PEX=2
		fi
	else
		if [[ ! -e /cm ]] ; then
			# phase 3
			FMID=wcoss.phase3
			export BUILD_TARGET=wcoss_dell_p3
			PEX=3
		else
			# WCOSS Cray
			FMID=wcoss.cray
			export BUILD_TARGET=wcoss_cray
			PEX=c
		fi
	fi
elif [[ -e /xcatpost && -e /scratch1 && -e /scratch2 ]] ; then
	export FMID=hera
	export MACHINE=hera
elif [[ -e /glade ]] ; then
	export FMID=cheyenne
	export MACHINE=cheyenne
elif [[ -e /pan2 && -e /lfs3 ]] ; then
	export FMID=jet
	export MACHINE=jet
elif ( hostname | grep -i gaea ) ; then
	export FMID=gaea
	export MACHINE=gaea
else
	# cannot ID machine
	echo "cannot identify current machine... check config/detect_machine"
	exit 1
fi
export BUILD_TARGET=${BUILD_TARGET:-$MACHINE.intel}

# now check if config file exists
if [ ! -e $CONFIGDIR/$FMID.config ] ; then
	echo "machine configuration file not found for FMID: $FMID"
	exit 2
fi
