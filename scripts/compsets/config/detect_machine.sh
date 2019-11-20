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
			PEX=1
		else
			# phase 2
			FMID=wcoss.phase2
			PEX=2
		fi
	else
		if [[ ! -e /cm ]] ; then
			# phase 3
			FMID=wcoss.phase3
			PEX=3
		else
			# WCOSS Cray
			FMID=wcoss.cray
			PEX=c
		fi
	fi
elif [[ -e /appfs && -e /scratch3 && -e /scratch4 ]] ; then
	export FMID=theia
	export MACHINE=theia
elif [[ -e /xcatpost && -e /scratch1 && -e /scratch2 ]] ; then
	export FMID=hera
	export MACHINE=hera
elif [[ -e /glade ]] ; then
	export FMID=yellowstone
	export MACHINE=yellowstone
elif [[ -e /pan2 && -e /lfs3 ]] ; then
	export FMID=jet
	export MACHINE=jet
elif ( hostname | grep -i gaea ) ; then
	export FMID=gaea
	export MACHINE=gaea
elif [[ -e /nobackupp8 ]] ; then
	export FMID=pleiades
	export MACHINE=pleiades
else
	# cannot ID machine
	echo "cannot identify current machine... check config/detect_machine"
	exit 1
fi

# now check if config file exists
if [ ! -e $CONFIGDIR/$FMID.config ] ; then
	echo "machine configuration file not found for FMID: $FMID"
	exit 2
fi
