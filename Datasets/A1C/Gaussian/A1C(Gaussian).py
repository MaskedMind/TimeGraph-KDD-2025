# -*- coding: utf-8 -*-
"""Untitled55.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xzXH_jKHU_WgOblLr9JKU9sOZxMzzDYQ
"""

!pip install tigramite

import numpy as np
import pandas as pd
from tigramite import plotting as tp
import matplotlib.pyplot as plt
from pathlib import Path

def get_linear_equations(n_vars, max_lag):
    """Get linear equations for specified configuration with confounder"""
    if n_vars == 4:
        if max_lag == 2:
            return [
                "X4[t] = 0.25 * X1[t-2] + e4",
                "X3[t] = 0.35 * X4[t] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 3:
            return [
                "X4[t] = 0.25 * X1[t-2] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 4:
            return [
                "X4[t] = 0.25 * X1[t-4] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
    elif n_vars == 6:
        if max_lag == 2:
            return [
                "X6[t] = 0.85 * X5[t] + 0.4 * U[t] + e6",
                "X5[t] = e5",  # exogenous
                "X4[t] = 0.25 * X1[t-2] + 0.3 * X5[t-1] + e4",
                "X3[t] = 0.35 * X4[t] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 3:
            return [
                "X6[t] = 0.85 * X5[t] + 0.4 * U[t] + e6",
                "X5[t] = e5",  # exogenous
                "X4[t] = 0.25 * X1[t-2] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 4:
            return [
                "X6[t] = 0.85 * X5[t] + 0.4 * U[t] + e6",
                "X5[t] = e5",  # exogenous
                "X4[t] = 0.25 * X1[t-4] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
    elif n_vars == 8:
        if max_lag == 2:
            return [
                "X8[t] = 0.4 * X7[t] + 0.35 * U[t] + e8",
                "X7[t] = 0.35 * X6[t-1] + e7",
                "X6[t] = 0.45 * X5[t] + 0.4 * U[t] + e6",
                "X5[t] = e5",  # exogenous
                "X4[t] = 0.25 * X1[t-2] + 0.3 * X5[t-1] + e4",
                "X3[t] = 0.35 * X4[t] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 3:
            return [
                "X8[t] = 0.4 * X7[t] + 0.35 * U[t] + e8",
                "X7[t] = 0.35 * X6[t-1] + e7",
                "X6[t] = 0.45 * X5[t] + 0.4 * U[t] + e6",
                "X5[t] = e5",  # exogenous
                "X4[t] = 0.25 * X1[t-2] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 4:
            return [
                "X8[t] = 0.4 * X7[t] + 0.35 * U[t] + e8",
                "X7[t] = 0.35 * X6[t-1] + e7",
                "X6[t] = 0.45 * X5[t] + 0.4 * U[t] + e6",
                "X5[t] = e5",  # exogenous
                "X4[t] = 0.25 * X1[t-4] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + 0.3 * U[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
    return []

class LinearTimeSeriesGenerator:
    def __init__(self, noise_scale=0.1, random_state=None):
        self.noise_scale = noise_scale
        self.random_state = random_state
        if random_state is not None:
            np.random.seed(random_state)

    def generate_noise(self, size):
        return np.random.normal(0, self.noise_scale, size=size)

    def generate_linear_equations(self, t, X, U, n_vars, max_lag):
        """Execute linear equations with confounder"""
        noise = self.generate_noise(n_vars + 1)  # +1 for U
        equations = get_linear_equations(n_vars, max_lag)
        var_values = {}

        # Generate U first (confounder)
        U[t] = noise[-1]
        var_values['U'] = U[t]

        # Generate X5 if present (exogenous)
        if n_vars >= 6:
            X[t, 4] = noise[4]  # X5 is exogenous
            var_values['X5'] = X[t, 4]

        # Helper function to evaluate a linear term
        def evaluate_linear_term(term):
            if '*' not in term:
                return 0

            parts = term.split('*')
            coef = float(parts[0].strip())
            var = parts[1].strip()

            # Extract variable name and time index
            var_name = var.split('[')[0].strip()  # e.g., 'X1' or 'U'
            time_idx = var.split('[')[1].split(']')[0].strip()  # e.g., 't' or 't-2'

            if var_name == 'U':
                if time_idx == 't':
                    return coef * U[t]
                else:
                    lag = int(time_idx.split('-')[1])
                    return coef * U[t-lag]
            else:
                # Extract the numeric part of variable name (e.g., '1' from 'X1')
                var_idx = int(var_name[1:]) - 1
                if time_idx == 't':
                    return coef * var_values.get(var_name, X[t, var_idx])
                else:
                    lag = int(time_idx.split('-')[1])
                    return coef * X[t-lag, var_idx]

        # Generate values for each variable
        for eq in equations:
            if '=' not in eq or eq.startswith('U[t]') or (n_vars >= 6 and eq.startswith('X5[t]')):
                continue

            left, right = eq.split('=')
            var_name = left.split('[')[0]
            var_idx = int(var_name[1:]) - 1

            # Split right side into terms
            terms = [term.strip() for term in right.split('+')]
            value = 0

            # Evaluate each term
            for term in terms:
                if term.startswith('e'):  # Noise term
                    value += noise[var_idx]
                else:
                    value += evaluate_linear_term(term)

            X[t, var_idx] = value
            var_values[var_name] = value

    def generate_multivariate_ts(self, n_points, n_vars, max_lag):
        """Generate multivariate time series with regular sampling"""
        X = np.zeros((n_points, n_vars))
        U = np.zeros(n_points)  # Array for the confounder

        # Initialize first steps with noise
        for i in range(max_lag):
            X[i] = self.generate_noise(n_vars)
            U[i] = self.generate_noise(1)[0]

        # Generate time series
        for t in range(max_lag, n_points):
            self.generate_linear_equations(t, X, U, n_vars, max_lag)

        # Create DataFrame
        timestamps = np.arange(n_points)
        columns = [f'X{i+1}' for i in range(n_vars)]
        df = pd.DataFrame(X, columns=columns)
        df['U'] = U
        df['time'] = timestamps

        return df

def extract_linear_links(equations):
    """Extract all linear causal links from the equations"""
    links = {}

    for eq in equations:
        if '=' in eq:
            left, right = [side.strip() for side in eq.split('=')]
            target = left.split('[')[0]

            if target != 'U':  # Skip U's equation
                terms = [term.strip() for term in right.split('+')]
                for term in terms:
                    if '*' in term and ('X' in term or 'U' in term):
                        parts = term.split('*')
                        coeff = float(parts[0].strip())
                        var_part = parts[1].strip()
                        var = var_part.split('[')[0]
                        lag_part = var_part.split('[')[1].split(']')[0]

                        lag = 0 if lag_part == 't' else -int(lag_part.split('-')[1])
                        links[(var, lag, target)] = coeff

    return links

def save_dataset_and_graph(df, n_vars, max_lag, sample_size, output_dir="output"):
    """Save dataset and create causal graph"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Save dataset
    filename = f'{output_dir}/linear_ts_with_confounder_n{sample_size}_vars{n_vars}_lag{max_lag}.csv'
    df.to_csv(filename, index=False)

    # Get equations and extract links
    equations = get_linear_equations(n_vars, max_lag)
    true_links = extract_linear_links(equations)

    # Create matrices for tigramite plotting
    var_names = [f'X{i+1}' for i in range(n_vars)] + ['U']
    n_total_vars = n_vars + 1
    val_matrix = np.zeros((n_total_vars, n_total_vars, max_lag + 1))
    graph_matrix = np.zeros((n_total_vars, n_total_vars, max_lag + 1), dtype='bool')

    # Fill matrices based on true links
    for (source, lag, target), weight in true_links.items():
        if source == 'U':
            source_idx = n_vars
        else:
            source_idx = int(source[1:]) - 1

        if target == 'U':
            target_idx = n_vars
        else:
            target_idx = int(target[1:]) - 1

        lag_idx = abs(lag)

        # Add the link to the matrices
        val_matrix[source_idx, target_idx, lag_idx] = weight
        graph_matrix[source_idx, target_idx, lag_idx] = True

        # For contemporaneous links, make val_matrix symmetric
        if lag == 0:
            val_matrix[target_idx, source_idx, lag_idx] = weight

    # Plot and save causal graph
    plt.figure(figsize=(12, 12))
    tp.plot_time_series_graph(
        val_matrix=val_matrix,
        graph=graph_matrix,
        var_names=var_names,
        link_colorbar_label='Linear Effect Strength',
        node_size=0.05
    )
    plt.title(f'Linear Causal Graph with Confounder (n={sample_size}, vars={n_vars}, lag={max_lag})')
    plt.savefig(f'{output_dir}/linear_causal_graph_with_confounder_n{sample_size}_vars{n_vars}_lag{max_lag}.png')
    plt.close()

    # Plot time series
    plt.figure(figsize=(15, 10))
    for col in df.columns[:-2]:  # Exclude U and time columns
        plt.plot(df['time'], df[col], label=col, alpha=0.7)
    plt.title(f'Linear Time Series (n={sample_size}, vars={n_vars}, lag={max_lag})')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{output_dir}/linear_ts_plot_n{sample_size}_vars{n_vars}_lag{max_lag}.png')
    plt.close()

    # Save causal structure description
    with open(f'{output_dir}/linear_causal_structure_vars{n_vars}_lag{max_lag}.txt', 'w') as f:
        f.write("True Linear Causal Structure with Confounder:\n")
        f.write("Format: (source, lag, target) => coefficient\n")
        f.write("\nEquations:\n")
        for eq in equations:
            f.write(f"{eq}\n")
        f.write("\nCausal Links:\n")
        for (source, lag, target), coef in true_links.items():
            f.write(f"({source}, {lag}, {target}) => {coef}\n")

def generate_all_combinations():
    """Generate datasets for all combinations"""
    n_vars_list = [4, 6, 8]
    max_lags = [2, 3, 4]
    sample_sizes = [500, 1000, 3000, 5000]

    for n in sample_sizes:
        for vars in n_vars_list:
            for lag in max_lags:
                print(f"\nGenerating dataset: n={n}, vars={vars}, lag={lag}")

                # Generate dataset
                generator = LinearTimeSeriesGenerator(noise_scale=0.1, random_state=42)
                df = generator.generate_multivariate_ts(
                    n_points=n,
                    n_vars=vars,
                    max_lag=lag
                )

                # Save dataset and create visualizations
                save_dataset_and_graph(df, vars, lag, n)
                print(f"Dataset and visualizations saved successfully")

if __name__ == "__main__":
    generate_all_combinations()

!zip -r /content/output.zip /content/output

from google.colab import files
files.download('/content/output.zip')