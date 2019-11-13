#!/usr/bin/env python2

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model

#developers.google.com/optimization/cp/cp_solver

def SimpleSatProgram():
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
       # list of variable objects
    devices_var = []
       # creting the variables 
    devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues([0,1,2,3]     ),'d0'))
    devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues([0,4,8,12]    ),'d1'))
    devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues([0,16,32,48]  ),'d2'))
    devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues([0,64,128,192]),'d3'))

    # Creates the constraints.
        # 1- binary constraints, don't use d0 with d1 
    # model.Add(devices_var[0]+devices_var[1]<=1)
        # 2- triple constraints, don't use d0 with d1, if d2 is used (only work with binary var)
    # model.Add(devices_var[0]+devices_var[1]<=1).OnlyEnforceIf(devices_var[2])
    w = [5, 2]
    model.Add(devices_var[0]+devices_var[1]+devices_var[2]+devices_var[3] - w[0]-w[1]<=0)

    #optimization 
        # secure score
    cvss=[4,6,3]

    model.Maximize( sum([v*c for v,c in zip(devices_var,cvss)]) ) 

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL: # cp_model.FEASIBLE:
        for i,v in enumerate(devices_var):
            print('x'+str(i)+'= ',solver.Value(v))
        print(solver.ObjectiveValue())
    


SimpleSatProgram()    

