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
    #for i in range(devices_num):
        #devices_var.append (model.NewIntVar(0, num_vals - 1 ,'x' + str(i)) )
    devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues([0,1,2,3]     ),'d0'))
    devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues([0,4,8,12]    ),'d1'))
    devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues([0,16,32,48]  ),'d2'))
    devices_var.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues([0,64,128,192]),'d3'))

    # Creates the constraints.
        # 1- binary constraints, don't use d0 with d1 
   # model.Add(devices_var[0]+devices_var[1]<=1)
        # 2- triple constraints, don't use d0 with d1, if d2 is used (only work with binary var)
#    model.Add(devices_var[0]+devices_var[1]<=1).OnlyEnforceIf(devices_var[2])
    # workflows f0,f1,f2,f3,f4 value 0 not needed value 1 function required
#    w = {'w1': [1,0,1],
#         'w2': [0,1,0]}
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
# devices capabilities f1,f2,f3,f4,f5
   # devices_cap = { devices_var[0]:[2,3,0,1,2],
   #                 devices_var[1]:[1,2,1,3,1],
   #                 devices_var[2]:[2,2,2,1,2],
   #                 devices_var[3]:[3,1,2,2,3],
   #                 devices_var[4]:[2,1,0,1,1]}     
   # # other constraints
    # model.Add(x != y)
    # model.AddAllDifferent(devices_var)      
    # model.Add(sum(devices_var)<= 3)
    
    #print([ [ sum( [ v[f] for k,v in devices_cap.items() if k>0 ] ), sum([v[f] for v in w.values()]) ] for f in range(5)] )
    #model.Add(all( [sum( [ v[f] for k,v in devices_cap.items() if k>0 ] ) >= sum([v[f] for v in w.values()])  for f in range(5)]))
    #model.Add( sum( [sum( [ v[f] for k,v in devices_cap.items() if k>0 ] )  >= sum([v[f] for v in w.values()]) for f in range(5) ])>=5 )
 