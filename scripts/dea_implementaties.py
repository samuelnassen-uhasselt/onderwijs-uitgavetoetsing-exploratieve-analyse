import numpy as np
import pandas as pd
from scipy.optimize import linprog
from pystoned import CNLS, StoNED
from pystoned.constant import CET_MULT, FUN_COST, RTS_VRS, RED_MOM, OPT_LOCAL

def stoned(input, output):
    # build and optimize the CNLS model
    model = CNLS.CNLS(output, input, z=None, cet=CET_MULT, fun=FUN_COST, rts=RTS_VRS)
    model.optimize('samuel.nassen@uhasselt.be')

    # calculate and print the StoNED frontier
    rd = StoNED.StoNED(model)
    rd.get_technical_inefficiency()
    return rd.get_technical_inefficiency()

def dea_input_oriented_crs(X, Y):
    """
    Input-oriented DEA with Constant Returns to Scale (CRS)
    X: inputs (n_units x n_inputs) - numpy array
    Y: outputs (n_units x n_outputs) - numpy array
    Returns: efficiency scores (array)
    """
    n_units = X.shape[0]
    n_inputs = X.shape[1]
    n_outputs = Y.shape[1]
    
    efficiency = np.zeros(n_units)
    
    for unit in range(n_units):
        # Variables: [theta, lambda_1, lambda_2, ..., lambda_n]
        # Objective: minimize theta
        c = [1] + [0] * n_units
        
        # Inequality constraints (A_ub @ x <= b_ub)
        A_ub = []
        b_ub = []
        
        # Input constraints: theta * X[unit, i] >= sum(lambda_j * X[j, i])
        # Rewritten as: -theta * X[unit, i] + sum(lambda_j * X[j, i]) <= 0
        for i in range(n_inputs):
            constraint = [-X[unit, i]] + list(X[:, i])
            A_ub.append(constraint)
            b_ub.append(0)
        
        # Output constraints: sum(lambda_j * Y[j, k]) >= Y[unit, k]
        # Rewritten as: -sum(lambda_j * Y[j, k]) <= -Y[unit, k]
        for k in range(n_outputs):
            constraint = [0] + list(-Y[:, k])
            A_ub.append(constraint)
            b_ub.append(-Y[unit, k])
        
        # NO equality constraint for CRS
        # In CRS, lambdas can sum to any non-negative value
        
        # Bounds: theta >= 0, lambda >= 0
        bounds = [(0, None)] + [(0, None)] * n_units
        
        # Solve (no A_eq and b_eq parameters)
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, 
                        bounds=bounds, method='highs')
        
        if result.success:
            efficiency[unit] = result.x[0]
        else:
            efficiency[unit] = np.nan
            print(f"Warning: Optimization failed for unit {unit}")
    
    return efficiency


def dea_input_oriented_vrs(X, Y):
    """
    Input-oriented DEA with Variable Returns to Scale
    X: inputs (n_units x n_inputs) - numpy array
    Y: outputs (n_units x n_outputs) - numpy array
    Returns: efficiency scores (array)
    """
    n_units = X.shape[0]
    n_inputs = X.shape[1]
    n_outputs = Y.shape[1]
    
    efficiency = np.zeros(n_units)
    
    for unit in range(n_units):
        # Variables: [theta, lambda_1, lambda_2, ..., lambda_n]
        # Objective: minimize theta
        c = [1] + [0] * n_units
        
        # Inequality constraints (A_ub @ x <= b_ub)
        A_ub = []
        b_ub = []
        
        # Input constraints: theta * X[unit, i] >= sum(lambda_j * X[j, i])
        # Rewritten as: -theta * X[unit, i] + sum(lambda_j * X[j, i]) <= 0
        for i in range(n_inputs):
            constraint = [-X[unit, i]] + list(X[:, i])
            A_ub.append(constraint)
            b_ub.append(0)
        
        # Output constraints: sum(lambda_j * Y[j, k]) >= Y[unit, k]
        # Rewritten as: -sum(lambda_j * Y[j, k]) <= -Y[unit, k]
        for k in range(n_outputs):
            constraint = [0] + list(-Y[:, k])
            A_ub.append(constraint)
            b_ub.append(-Y[unit, k])
        
        # Equality constraint for VRS: sum(lambda) = 1
        A_eq = [[0] + [1] * n_units]
        b_eq = [1]
        
        # Bounds: theta >= 0, lambda >= 0
        bounds = [(0, None)] + [(0, None)] * n_units
        
        # Solve
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, 
                        A_eq=A_eq, b_eq=b_eq,
                        bounds=bounds, method='highs')
        
        if result.success:
            efficiency[unit] = result.x[0]
        else:
            efficiency[unit] = np.nan
            print(f"Warning: Optimization failed for unit {unit}")
    
    return efficiency


def dea_input_oriented_vrs_sample(X, Y, sample_indices):
    """
    Run DEA on a subset of units
    
    Parameters:
    X, Y: full data matrices
    sample_indices: indices of units to use as reference set
    
    Returns:
    efficiency scores for ALL units relative to the sample
    """
    n_units = X.shape[0]
    n_inputs = X.shape[1]
    n_outputs = Y.shape[1]
    n_sample = len(sample_indices)
    
    # Extract sample data
    X_sample = X[sample_indices]
    Y_sample = Y[sample_indices]
    
    efficiency = np.zeros(n_units)
    
    for unit in range(n_units):
        # Objective: minimize theta
        c = [1] + [0] * n_sample
        
        A_ub = []
        b_ub = []
        
        # Input constraints: theta * X[unit] >= X_sample * lambda
        for i in range(n_inputs):
            constraint = [-X[unit, i]] + list(X_sample[:, i])
            A_ub.append(constraint)
            b_ub.append(0)
        
        # Output constraints: Y_sample * lambda >= Y[unit]
        for k in range(n_outputs):
            constraint = [0] + list(-Y_sample[:, k])
            A_ub.append(constraint)
            b_ub.append(-Y[unit, k])
        
        # VRS constraint: sum(lambda) = 1
        A_eq = [[0] + [1] * n_sample]
        b_eq = [1]
        
        # Bounds
        bounds = [(0, None)] + [(0, None)] * n_sample
        
        # Solve
        result = linprog(c, A_ub=A_ub, b_ub=b_ub, 
                        A_eq=A_eq, b_eq=b_eq,
                        bounds=bounds, method='highs')
        
        if result.success:
            efficiency[unit] = result.x[0]
        else:
            efficiency[unit] = np.nan
    
    return efficiency

