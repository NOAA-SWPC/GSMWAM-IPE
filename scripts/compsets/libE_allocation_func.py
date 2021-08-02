from libensemble.tools.alloc_support import avail_worker_ids, sim_work
#from libensemble.alloc_funcs.support import avail_worker_ids, sim_work
 
def test_alloc(W, H, sim_specs, gen_specs, alloc_specs, persis_info):
     """
     This allocation function gives (in order) entries in alloc_spec['x'] to
     idle workers. It is an example use case where no gen_func is used.
 
     .. seealso::
     `test_fast_alloc.py <https://github.com/Libensemble/libensemble/blob/de    velop/libensemble/tes    ts/regression_tests/test_fast_alloc.py>`_
     """
 
     Work = {}
     if not persis_info:
         persis_info['next_to_give'] = 0
 
     if persis_info['next_to_give'] == len(H):
         persis_info['next_to_give'] = 0
 
     print(persis_info)
 
     for i in avail_worker_ids(W):
         # Give sim work
         sim_work(Work, i, sim_specs['in'], [persis_info['next_to_give']], [])
         persis_info['next_to_give'] += 1
 
     return Work, persis_info
