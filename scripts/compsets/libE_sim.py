import subprocess
import numpy as np


def submit_wam(H, persis_info, sim_specs, _):
    """
    Evaluates WAM forecast
    H           - History array. Updated by workers with gen_f and sim_f inputs and outputs. H is passed to generator in case user wants to generate new samples based on previous data
    persis_info - Dictionary with worker-specific information. 
    """

    out = np.zeros(1, dtype=sim_specs['out'])

    # Identify simulation number
    run_id = int(H['x'][0])

    print("LibE simulation number: " + str(run_id))

    # inputs are updated in bash script
    subprocess.run(["./libE_WAM_member.sh", str(run_id)], shell=False)

    out['y'] = 0.8
    return out, persis_info
