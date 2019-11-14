#!/usr/bin/env python2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model
import itertools
import numpy as np 

#developers.google.com/optimization/cp/cp_solver
def perm(vec):
    indx = [i for i,v in enumerate(vec) if v =='1']
    prm = ["".join(seq) for seq in itertools.product("01",repeat=len(indx))]
    prm_num = len(prm)
    vec_len = len(vec)
    prm_z_v =['0'*vec_len for i in range(prm_num)]
    for prm_i in range(prm_num):
        temp = list(prm_z_v[prm_i])
        for j,bit_loc in enumerate(indx):
            temp [bit_loc] = list(prm[prm_i])[j]
            prm_z_v[prm_i]=int("".join(temp),2)

    return prm_z_v 

def SimpleSatProgram():
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    devices_num = 4
    function_num = 4
    device_cap=np.array( [[1,0,1,0],
                          [1,0,0,1],
                          [0,1,1,0],
                          [1,0,1,1]])

    # to save the index of functions in the flat devicces_var list                      
    func_wise_var = [ [] for f in range(function_num)] 
    devices_var = []
    for d in range(devices_num):
        for f in range(function_num):
            if device_cap[d][f]:
                devices_var.append(model.NewIntVar(0,1,'x_'+str(d)+str(f)))
                func_wise_var[f].append( len(devices_var)-1 )
    print(func_wise_var)                
    
    # Creates the constraints.
        # 1- binary constraints, don't use x00 with x13 
    model.Add(devices_var[0]+devices_var[3]<=1)
        # 2- triple constraints, don't use d0 with d1, if d2 is used (only work with binary var)
    # model.Add(devices_var[0]+devices_var[1]<=1).OnlyEnforceIf(devices_var[2])
    w = np.array( [[1,0,1,0], 
                   [0,0,1,1]])

    # constraint to select the minimum number of devices that are enough to satisfy the workflows
        # total functions req in the workflow
    wf = list(w.sum(axis=0))
    for idx_f,num_f in enumerate(wf):    
        model.Add( sum( [devices_var[i] for i in func_wise_var[idx_f] ] ) <= num_f)

#    model.Add(devices_var[0]+devices_var[2]+devices_var[6]<=1 )
#    model.Add(devices_var[4]<=0 )
#    model.Add(devices_var[1]+devices_var[5]+devices_var[7]<=2 )
#    model.Add(devices_var[3]+devices_var[8]<=1 )

    #optimization 
        # secure score
    icvss=[4,6,3,2,2,3,4,2,1]
    assert len(icvss)==len(devices_var), "CVSS should be for all devices functions"

    model.Maximize( sum([v*c for v,c in zip(devices_var,icvss)]) ) 

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL: # cp_model.FEASIBLE:
        print(w)
        for v in devices_var:
            print(v.Name(),solver.Value(v))
        print(solver.ObjectiveValue())
    


SimpleSatProgram()    

# limitations
# 1- each device can only used once for each function at a time. Still it can perform multiple different functions
# 2- The model will produce partial solution if no feasible solution due to the minimum devices selection constraint. 
