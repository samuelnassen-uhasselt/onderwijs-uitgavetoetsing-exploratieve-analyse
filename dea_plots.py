import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from scipy.spatial import ConvexHull

def plot_ratio_analysis(X, Y, efficiency, 
                        input_label="Input",
                        output_labels=["Output 1", "Output 2"],
                        title="DEA Ratio Analysis"):
    """
    Plot input/output ratios with efficiency scores
    
    Parameters:
    X: inputs (n_units x 1)
    Y: outputs (n_units x 2)
    efficiency: efficiency scores
    input_label: label for input variable
    output_labels: labels for two output variables
    title: plot title
    school_ids: optional school identifiers
    """
    
    # Calculate ratios
    ratio_1 = Y[:, 0] / X[:, 0]
    ratio_2 = Y[:, 1] / X[:, 0]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Separate frontier
    efficient_mask = efficiency >= 0.97
    
    # Plot inefficient schools
    ax.scatter(ratio_1[~efficient_mask], 
            ratio_2[~efficient_mask],
            c=efficiency[~efficient_mask],
            cmap='RdYlGn',  # Reversed so darker = less efficient
            s=300,
            alpha=0.7,
            edgecolors='black',
            linewidth=2,
            vmin=efficiency.min(),
            vmax=1.0,
            label='Inefficient')
    
    # Plot efficient schools (on frontier)
    ax.scatter(ratio_1[efficient_mask], 
            ratio_2[efficient_mask],
            c='gold',
            s=500,
            alpha=0.9,
            edgecolors='darkgreen',
            linewidth=3,
            marker='*',
            label='Efficient (Frontier)',
            zorder=5)
    
    
    # Add colorbar for inefficient schools
    sm = plt.cm.ScalarMappable(cmap='RdYlGn', 
                               norm=plt.Normalize(vmin=efficiency.min(), vmax=1.0))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Efficiency Score', rotation=270, labelpad=20, fontsize=13)
    
    # Labels with interpretation
    ax.set_xlabel(f'{output_labels[0]}/{input_label}', 
                 fontsize=13, fontweight='bold')
    ax.set_ylabel(f'{output_labels[1]}/{input_label}', 
                 fontsize=13, fontweight='bold')
    ax.set_title(title, fontsize=15, fontweight='bold', pad=20)
    
    
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add text box with interpretation
    textstr = 'Interpretation:\n• Lower left corner = Best performance\n• Gold stars = Efficient frontier\n• Color intensity = Efficiency level'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    
    # Print summary statistics
    print(f"\n{'='*60}")
    print("RATIO ANALYSIS SUMMARY")
    print(f"{'='*60}")
    print(f"\nRatio 1: {input_label}/{output_labels[0]}")
    print(f"  Range: {ratio_1.min():.4f} to {ratio_1.max():.4f}")
    print(f"  Mean: {ratio_1.mean():.4f}")
    print(f"  Efficient schools mean: {ratio_1[efficient_mask].mean():.4f}")
    
    print(f"\nRatio 2: {input_label}/{output_labels[1]}")
    print(f"  Range: {ratio_2.min():.4f} to {ratio_2.max():.4f}")
    print(f"  Mean: {ratio_2.mean():.4f}")
    print(f"  Efficient schools mean: {ratio_2[efficient_mask].mean():.4f}")
    
    print(f"\nEfficiency:")
    print(f"  Efficient schools: {efficient_mask.sum()}/{len(efficiency)}")
    print(f"  Mean efficiency: {efficiency.mean():.4f}")
    print(f"{'='*60}\n")
    
    return fig, ax, ratio_1, ratio_2

def plot_ratio_analysis_interactive(X, Y, efficiency, 
                                    input_label="Input",
                                    output_labels=["Output 1", "Output 2"],
                                    school_ids=None):
    """Interactive version with hover information"""
    
    # Calculate ratios
    ratio_1 = Y[:, 0] / X[:, 0]
    ratio_2 = Y[:, 1] / X[:, 0]
    
    if school_ids is None:
        school_ids = [f"Unit {i}" for i in range(len(X))]
    
    df_plot = pd.DataFrame({
        'School': school_ids,
        'Ratio_1': ratio_1,
        'Ratio_2': ratio_2,
        'Efficiency': efficiency,
        input_label: X[:, 0],
        output_labels[0]: Y[:, 0],
        output_labels[1]: Y[:, 1],
        'Status': ['Efficient' if e >= 0.97 else 'Inefficient' for e in efficiency]
    })
    
    # Create figure
    fig = px.scatter(df_plot,
                     x='Ratio_1',
                     y='Ratio_2',
                     color='Efficiency',
                     size='Efficiency',
                     hover_data=['School', input_label, output_labels[0], output_labels[1], 'Efficiency'],
                     color_continuous_scale='RdYlGn',
                     title='DEA Ratio Analysis (Interactive)',
                     labels={
                         'Ratio_1': f'{output_labels[0]}/{input_label}',
                         'Ratio_2': f'{output_labels[1]}/{input_label}'
                     })
    
    
    # Highlight efficient frontier
    efficient_df = df_plot[df_plot['Status'] == 'Efficient']
    fig.add_trace(go.Scatter(
        x=efficient_df['Ratio_1'],
        y=efficient_df['Ratio_2'],
        mode='markers',
        marker=dict(size=15, color='gold',
                   line=dict(width=2, color='darkgreen')),
        name='Efficient Frontier',
        showlegend=True
    ))
    
    fig.update_layout(
        width=1100,
        height=800,
        font=dict(size=12),
        hovermode='closest'
    )
    
    return fig

def plot_in_out_analysis_interactive(X, Y, efficiency, 
                                    input_label="Input",
                                    output_label="Output",
                                    school_ids=None):
    
    if school_ids is None:
        school_ids = [f"Unit {i}" for i in range(len(X))]
    
    df_plot = pd.DataFrame({
        'School': school_ids,
        'Efficiency': efficiency,
        input_label: X[:, 0],
        output_label: Y[:, 0],
        'Status': ['Efficient' if e >= 0.97 else 'Inefficient' for e in efficiency]
    })

    x = X.flatten()
    y = Y.flatten()

    # Fit polynomial
    degree = 4
    coefficients = np.polyfit(x, y, degree)
    poly_function = np.poly1d(coefficients)

    # Generate smooth curve for plotting
    x_smooth = np.linspace(x.min(), x.max(), 100)
    y_smooth = poly_function(x_smooth)

    # Convex Hull for Efficiency Frontier
    points = np.column_stack([X, Y])
    border_points = [[X.min(), 0], [X.max(), Y.max()]]
    points = np.vstack([points, border_points])
    hull = ConvexHull(points)

    # Get hull vertices
    hull_vertices = points[hull.vertices]

    # Remove bottom part of hull
    start = 0
    while not np.array_equal(hull_vertices[start],[X.min(), 0]):
        start += 1
    start += 1

    while not np.array_equal(hull_vertices[start],[X.max(), Y.max()]):
        hull_vertices = np.delete(hull_vertices, start, axis=0)

    while not np.array_equal(hull_vertices[0],[X.max(), Y.max()]):
        hull_vertices = np.roll(hull_vertices, 1, axis=0)

    # Create figure
    fig = px.scatter(df_plot,
                     x=input_label,
                     y=output_label,
                     color='Efficiency',
                     hover_data=['School', input_label, output_label, 'Efficiency'],
                     color_continuous_scale='RdYlGn',
                     title='DEA Input/Output Analysis',
                     labels={
                         'Input': f'{input_label}',
                         'Output': f'{output_label}'
                     })

    # Draw polynomial
    fig.add_trace(go.Scatter(
        x=x_smooth,
        y=y_smooth,
        mode='lines',
        name=f'Polynomial Fit (degree {degree})',
        line=dict(color='gray', width=1)
    ))

    # Draw frontier
    fig.add_trace(go.Scatter(
        x=hull_vertices[:, 0],
        y=hull_vertices[:, 1],
        mode='lines',
        name='Efficiency Frontier',
        line=dict(color='blue', width=2),
    ))
    
    fig.update_layout(
        width=1100,
        height=800,
        font=dict(size=12),
        hovermode='closest',
        legend=dict(
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom'
        )
    )
    
    return fig
