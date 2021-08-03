import numpy as np

# Import libEnsemble items
from libensemble.libE import libE
from libensemble.tools import parse_args
from libensemble.executors.mpi_executor import MPIExecutor
from libensemble import libE_logger
libE_logger.set_level('DEBUG')

#from mpi4py import MPI

# Import custom scripts
from libE_sim import submit_wam as sim_f
from libE_allocation_func import test_alloc as alloc_f

from datetime import datetime
import sys

def call_ensemble(nworkers, n_sim):

    #exctr = MPIExecutor(central_mode=True)
    exctr = MPIExecutor()

    libE_specs = {'nworkers': nworkers, 'comms': 'local'}
    #libE_specs = {'comms': 'mpi'}
    sim_specs = {'sim_f': sim_f, 'in': ['x'], 'out': [('y', float)]}
    gen_specs = {}

    # Set up H0 - used as run_ID
    H0 = np.zeros(n_sim, dtype=[('x', float), ('sim_id', int)])
    H0['sim_id'] = range(n_sim)
    
    for i in range(n_sim):
        H0['x'][i] = i
    
    alloc_specs = {'alloc_f': alloc_f, 'out': [('x',float)]}

    exit_criteria = {'sim_max':len(H0)}

    print(datetime.now().hour,':', datetime.now().minute, ':', datetime.now().second,'.', datetime.now().microsecond, " Starting libE")

    # Peform the run
    H, persis_info, flag = libE(sim_specs, gen_specs, exit_criteria, alloc_specs=alloc_specs, libE_specs=libE_specs, H0=H0)
    
    print(datetime.now().hour,':', datetime.now().minute, ':', datetime.now().second,'.', datetime.now().microsecond, " Ending libE")

### Ensemble settings
n_workers = int(sys.argv[1]) # excludes the master node where libE runs
n_sim = int(sys.argv[2])

call_ensemble(n_workers, n_sim)
