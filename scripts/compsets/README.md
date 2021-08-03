# libEnsemble with WAM-IPE

Use libEnsemble (libE) Python library for resource allocation with large WAM ensembles. 
See libEnsemble documentation for installation: https://libensemble.readthedocs.io/en/main/introduction.html

## Scripts

1. submit_libE.sh - submit libE job, i.e. 'submit_libE.sh cheyenne_libE.config'
    * Update the number of nodes, wallclock time, n_workers and n_sim as appropriate.
    * Update libE environment (i.e. make sure python with libE is in the path)
    * The temp_libE_job.sh that is created enters the Conda environment with libE and calls the libE calling function. It also creates a node_list file that libE requires. 
2. libE_calling_func.py (no need to edit)
3. libE_allocation_function - Steps through ensemble members (no need to edit)
4. libE_sim.py - The Python simulation function (no need to edit)
    * Calls libE_WAM_member.sh
5. libE_WAM_member.sh 
    * Update base_job_name if desired
    * Update the ensemble inputs. Default is reading daily kp and F10p7 from a file.
6. cheyenne_libE.config
    * This is essentially a copy of cheyenne.config tailored to the specific needs of an ensemble. For instance, updating FIX_F107 and FIX_KP to be altered for each member. 
7. libE_WAM_submit.sh - essentially submit.sh, but with the PBS statements removed. (no need to edit)

When an ensemble is run some additional files will appear in this directory. 
* ensemble.log - a log file provided by libE, useful to check that workers were placed on different nodes
* libE_stats.txt - stats file provided by libE
* libE_mem_config - directory with member configuration scripts
* node_list - libE requires the PBS_NODEFILE to be written to file
