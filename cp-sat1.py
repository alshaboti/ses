#!/usr/bin/env python2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model
import itertools
import numpy as np 
import time

#developers.google.com/optimization/cp/cp_solver

def NotSimpleSatProgram():
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

    w = np.array( [[1,0,1,1], 
                   [0,1,1,1]])

    # to save the index of functions in the flat devicces_var list                      
    dev_per_fun = [ [] for f in range(function_num)] 
    devices_var = []
    for d in range(devices_num):
        for f in range(function_num):
            if device_cap[d][f]:
                var_d = model.NewIntVar(0,device_cap[d][f],'x_'+str(d)+str(f))
                devices_var.append(var_d)
                dev_per_fun[f].append( len(devices_var)-1 )


    # Creates the constraints.
        # 1- binary constraints, don't use x00 with x13 
    model.Add(devices_var[1]+devices_var[8]<=1)
        # 2- triple constraints, don't use x1 with x2, if x3 is used (only work with binary var)
    model.Add(devices_var[5]+devices_var[7]<=1).OnlyEnforceIf( devices_var[0] )

 
#   for wi in w:
#        # 1- binary constraints, don't use x00 with x13 
#        model.Add(wi[2]*devices_var[1]+wi[3]*devices_var[8]<=1)
#        # 2- triple constraints, don't use x1 with x2, if x3 is used (only work with binary var)
#        if wi[0]:
#            model.Add(wi[2]*devices_var[5]+wi[2]*devices_var[7]<=1).OnlyEnforceIf( devices_var[0]*wi[0] )
#
    # constraint to select the minimum number of devices that are enough to satisfy the workflows
        # total functions req in the workflow
    wf = list(w.sum(axis=0))
    for idx_f,num_f in enumerate(wf):    
        model.Add( sum( [devices_var[i] for i in dev_per_fun[idx_f] ] ) +1 > num_f)

   #optimization 
         # secure score
    icvss=[3,3,1,1,1,1,1,1,1]
    assert len(icvss)==len(devices_var), "CVSS should be for all decision variables"

    model.Maximize( sum([v*c for v,c in zip(devices_var,icvss)]) ) 

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    start = time.time()
    status = solver.Solve(model)
    end = time.time()
    print("Elapsed time: ", end-start)
    if status == cp_model.OPTIMAL: # cp_model.FEASIBLE:
        print(w)
        for v in devices_var:
            print(v.Name(),solver.Value(v))
        print(solver.ObjectiveValue())
    


NotSimpleSatProgram()    

