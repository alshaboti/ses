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
    functions_num = 8
       # list of variable objects
    devices_var = []
       # creting the variables
    devices_cap = { 0:'00000011',
                    1:'00001100',
                    2:'00110000',
                    3:'11000100'}
    for i in range(devices_num):
        x = perm(devices_cap[i])
        print(x)
        devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues(x),'d'+str(i)))
    # Creates the constraints.
        # 1- binary constraints, don't use d0 with d1 
    model.Add(devices_var[0]+devices_var[1]<=1)
        # 2- triple constraints, don't use d0 with d1, if d2 is used (only work with binary var)
    # model.Add(devices_var[0]+devices_var[1]<=1).OnlyEnforceIf(devices_var[2])
    w = [5, 2]

    model.Add(devices_var[0]+devices_var[1]+devices_var[2]+devices_var[3] <= w[0]+w[1])
    #optimization 
        # secure score
    cvss=[4,6,3,2]
    assert len(cvss)==devices_num, "CVSS should be for al devices"

    model.Maximize( sum([v*c for v,c in zip(devices_var,cvss)]) ) 

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL: # cp_model.FEASIBLE:
        for i,v in enumerate(devices_var):
            print('x'+str(i)+'= ',solver.Value(v))
        print(solver.ObjectiveValue())
    


SimpleSatProgram()    

# limitation
# 1- each device can only used once for each function at a time. It can perform multiple diff. functions
# 2- The model will produce partial solution if no feasible solution due to the <= constraint. 
