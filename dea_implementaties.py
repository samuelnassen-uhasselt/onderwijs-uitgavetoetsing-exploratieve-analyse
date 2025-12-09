import numpy as np
import pandas as pd
from scipy.optimize import linprog

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


def order_m_efficiency(X, Y, m, B=200, seed=None):
    """
    Order-m efficiency estimation using Monte Carlo simulation
    
    Parameters:
    X: inputs (n_units x n_inputs)
    Y: outputs (n_units x n_outputs)
    m: number of peers to sample in each iteration
    B: number of bootstrap iterations (default 200)
    seed: random seed for reproducibility
    
    Returns:
    efficiency: array of order-m efficiency scores
    efficiency_std: standard deviation of efficiency estimates
    """
    if seed is not None:
        np.random.seed(seed)
    
    n_units = X.shape[0]
    
    # Store efficiency scores from each iteration
    efficiency_matrix = np.zeros((n_units, B))
    
    for b in range(B):
        if (b + 1) % 50 == 0:
            print(f"  Bootstrap iteration {b + 1}/{B}")
        
        # For each unit, sample m peers (excluding the unit itself)
        for unit in range(n_units):
            # Available peers (all except current unit)
            available_peers = [i for i in range(n_units) if i != unit]
            
            # Sample m peers
            if len(available_peers) < m:
                # If not enough peers, use all available
                sample_indices = available_peers
            else:
                sample_indices = np.random.choice(available_peers, size=m, replace=False)
            
            # Run DEA for this unit against sampled peers
            eff = dea_input_oriented_vrs_sample(
                X[unit:unit+1], 
                Y[unit:unit+1], 
                sample_indices
            )
            efficiency_matrix[unit, b] = eff[0]
    
    # Average across bootstrap iterations
    efficiency = np.mean(efficiency_matrix, axis=1)
    efficiency_std = np.std(efficiency_matrix, axis=1)
    
    return efficiency, efficiency_std, efficiency_matrix
