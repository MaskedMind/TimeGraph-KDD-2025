# -*- coding: utf-8 -*-
"""D1C.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1riNDI1kEDhicC02hj-qeUuGnyAxwA8fv
"""

!pip install tigramite

import numpy as np
import pandas as pd
from tigramite import plotting as tp
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats

def get_linear_equations(n_vars, max_lag):
    """Get linear equations with confounder U (max 2 edges from U)"""
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
                "X5[t] = 0.4 * X4[t-1] + e5",
                "X4[t] = 0.25 * X1[t-2] + 0.3 * X5[t-1] + e4",
                "X3[t] = 0.35 * X4[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 3:
            return [
                "X6[t] = 0.85 * X5[t] + 0.4 * U[t] + e6",
                "X5[t] = 0.4 * X4[t-1] + e5",
                "X4[t] = 0.25 * X1[t-2] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 4:
            return [
                "X6[t] = 0.85 * X5[t] + 0.4 * U[t] + e6",
                "X5[t] = 0.4 * X4[t-1] + e5",
                "X4[t] = 0.25 * X1[t-4] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
    elif n_vars == 8:
        if max_lag == 2:
            return [
                "X8[t] = 0.4 * X7[t] + 0.35 * U[t] + e8",
                "X7[t] = 0.35 * X6[t-1] + e7",
                "X6[t] = 0.45 * X5[t] + e6",
                "X5[t] = 0.4 * X4[t-1] + e5",
                "X4[t] = 0.25 * X1[t-2] + 0.3 * X5[t-1] + e4",
                "X3[t] = 0.35 * X4[t] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 3:
            return [
                "X8[t] = 0.4 * X7[t] + 0.35 * U[t] + e8",
                "X7[t] = 0.35 * X6[t-1] + e7",
                "X6[t] = 0.45 * X5[t] + e6",
                "X5[t] = 0.4 * X4[t-1] + e5",
                "X4[t] = 0.25 * X1[t-2] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
        elif max_lag == 4:
            return [
                "X8[t] = 0.4 * X7[t] + 0.35 * U[t] + e8",
                "X7[t] = 0.35 * X6[t-1] + e7",
                "X6[t] = 0.45 * X5[t] + e6",
                "X5[t] = 0.4 * X4[t-1] + e5",
                "X4[t] = 0.25 * X1[t-4] + e4",
                "X3[t] = 0.35 * X4[t] + 0.2 * X2[t-3] + e3",
                "X2[t] = 0.3 * X3[t-1] + e2",
                "X1[t] = 0.4 * X2[t] + 0.5 * U[t] + e1",
                "U[t] = eU"
            ]
    return []

class LinearTimeSeriesGeneratorMCAR:
    def __init__(self, noise_type='gaussian', noise_params={'scale': 0.1, 'df': 3},
                 missing_rate=0.2, random_state=None):
        self.noise_type = noise_type
        self.noise_params = noise_params
        self.missing_rate = missing_rate
        self.random_state = random_state
        if random_state is not None:
            np.random.seed(random_state)

    def generate_noise(self, size):
        if self.noise_type == 'gaussian':
            return np.random.normal(0, self.noise_params['scale'], size=size)
        elif self.noise_type == 'student_t':
            return stats.t.rvs(df=self.noise_params['df'],
                             loc=0,
                             scale=self.noise_params['scale'],
                             size=size)

    def generate_linear_equations(self, t, X, U, n_vars, max_lag):
        """Execute linear equations with confounder"""
        noise = self.generate_noise(n_vars + 1)  # +1 for U
        equations = get_linear_equations(n_vars, max_lag)
        var_values = {}

        # Generate U first (confounder)
        U[t] = noise[-1]
        var_values['U'] = U[t]

        # First pass: process equations that don't depend on current time step values
        for eq in equations:
            if '=' not in eq or eq.startswith('U[t]'):
                continue

            left, right = eq.split('=')
            var_name = left.split('[')[0]
            var_idx = int(var_name[1:]) - 1

            # Skip if equation depends on current time values
            if any('t]' in term for term in right.split('+')):
                continue

            terms = [term.strip() for term in right.split('+')]
            value = 0

            for term in terms:
                if term.startswith('e'):  # Noise term
                    value += noise[var_idx]
                else:
                    coef = float(term.split('*')[0].strip())
                    var = term.split('*')[1].strip()
                    var_name = var.split('[')[0].strip()
                    time_idx = var.split('[')[1].split(']')[0].strip()

                    if var_name == 'U':
                        value += coef * U[t]
                    else:
                        var_idx_source = int(var_name[1:]) - 1
                        lag = int(time_idx.split('-')[1])
                        value += coef * X[t-lag, var_idx_source]

            X[t, var_idx] = value
            var_values[var_name] = value

        # Second pass: process equations that depend on current time step values
        for eq in equations:
            if '=' not in eq or eq.startswith('U[t]'):
                continue

            left, right = eq.split('=')
            var_name = left.split('[')[0]
            var_idx = int(var_name[1:]) - 1

            # Skip if already processed
            if var_name in var_values:
                continue

            terms = [term.strip() for term in right.split('+')]
            value = 0

            for term in terms:
                if term.startswith('e'):  # Noise term
                    value += noise[var_idx]
                else:
                    coef = float(term.split('*')[0].strip())
                    var = term.split('*')[1].strip()
                    var_name_source = var.split('[')[0].strip()
                    time_idx = var.split('[')[1].split(']')[0].strip()

                    if var_name_source == 'U':
                        value += coef * U[t]
                    else:
                        var_idx_source = int(var_name_source[1:]) - 1
                        if time_idx == 't':
                            value += coef * var_values.get(var_name_source, X[t, var_idx_source])
                        else:
                            lag = int(time_idx.split('-')[1])
                            value += coef * X[t-lag, var_idx_source]

            X[t, var_idx] = value
            var_values[var_name] = value

    def apply_mcar(self, X):
        """Apply MCAR missing pattern to the observed variables (not U)"""
        mask = np.random.random(X.shape) < self.missing_rate
        X_missing = X.copy()
        X_missing[mask] = np.nan
        return X_missing

    def generate_multivariate_ts(self, n_points, n_vars, max_lag):
        """Generate multivariate time series with MCAR missing data and confounder"""
        # Initialize arrays
        X = np.zeros((n_points, n_vars))
        U = np.zeros(n_points)  # Array for confounder U

        # Initialize first steps with noise
        for i in range(max_lag):
            X[i] = self.generate_noise(n_vars)
            U[i] = self.generate_noise(1)[0]

        # Generate time series
        for t in range(max_lag, n_points):
            self.generate_linear_equations(t, X, U, n_vars, max_lag)

        # Apply MCAR missing pattern to observed variables
        X_missing = self.apply_mcar(X)

        # Create DataFrame including U (U is fully observed)
        columns = [f'X{i+1}' for i in range(n_vars)]
        df_missing = pd.DataFrame(X_missing, columns=columns)
        df_missing['U'] = U
        df_missing['time'] = np.arange(n_points)

        # Create complete data DataFrame
        df_complete = pd.DataFrame(X, columns=columns)
        df_complete['U'] = U
        df_complete['time'] = np.arange(n_points)

        return df_missing, df_complete

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

def save_dataset_and_graph(df_missing, df_complete, n_vars, max_lag, sample_size,
                         noise_type, missing_rate, output_dir="output_mcar_confounded"):
    """Save dataset and create causal graph visualization"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    base_filename = f'{output_dir}/linear_ts_n{sample_size}_vars{n_vars}_lag{max_lag}_{noise_type}_mcar{int(missing_rate*100)}'

    # Save datasets (both missing and complete)
    df_missing.to_csv(f'{base_filename}_missing.csv', index=False)
    df_complete.to_csv(f'{base_filename}_complete.csv', index=False)

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
    plt.title(f'Linear Causal Graph with Confounder\n(n={sample_size}, vars={n_vars}, lag={max_lag})\n{noise_type}, MCAR {int(missing_rate*100)}%')
    plt.savefig(f'{base_filename}_graph.png')
    plt.close()

    # Plot time series with missing data
    plt.figure(figsize=(15, 10))

    # Plot observed variables
    for col in df_missing.columns[:-2]:  # Exclude U and time
        # Plot complete data as solid line
        plt.plot(df_complete['time'], df_complete[col],
                label=f'{col} (complete)', alpha=0.3)
        # Plot available data points as scatter
        mask = ~df_missing[col].isna()
        plt.scatter(df_missing.loc[mask, 'time'],
                   df_missing.loc[mask, col],
                   label=f'{col} (observed)', alpha=0.7, s=20)

    # Plot confounder U (always fully observed)
    plt.plot(df_missing['time'], df_missing['U'],
            label='U (confounder)', linestyle='--', alpha=0.7)

    plt.title(f'Time Series with MCAR {int(missing_rate*100)}% Missing Data\n(n={sample_size}, vars={n_vars}, lag={max_lag})')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{base_filename}_series.png')
    plt.close()

    # Save missing data pattern visualization
    plt.figure(figsize=(15, 5))
    missing_matrix = df_missing.drop(['time', 'U'], axis=1).isna()
    plt.imshow(missing_matrix.T, aspect='auto', cmap='binary')
    plt.title(f'Missing Data Pattern (black = missing)\nMCAR {int(missing_rate*100)}%')
    plt.xlabel('Time')
    plt.ylabel('Variable')
    plt.yticks(range(n_vars), [f'X{i+1}' for i in range(n_vars)])
    plt.colorbar(label='Missing')
    plt.savefig(f'{base_filename}_missing_pattern.png')
    plt.close()

    # Save causal structure description
    with open(f'{base_filename}_structure.txt', 'w') as f:
        f.write(f"True Linear Causal Structure with Confounder ({noise_type}, MCAR {int(missing_rate*100)}%):\n")
        f.write("Format: (source, lag, target) => coefficient\n")
        f.write("\nEquations:\n")
        for eq in equations:
            f.write(f"{eq}\n")
        f.write("\nCausal Links:\n")
        for (source, lag, target), coef in true_links.items():
            f.write(f"({source}, {lag}, {target}) => {coef}\n")

def analyze_mcar_confounded_data(df_missing, df_complete, title="Linear Time Series Analysis with MCAR and Confounder"):
    """Analyze and plot the time series data with MCAR missing values and confounder"""
    print(f"\nAnalyzing {title}")
    print("=" * 50)

    # Basic statistics
    n_total = df_missing.drop(['time', 'U'], axis=1).size
    n_missing = df_missing.drop(['time', 'U'], axis=1).isna().sum().sum()
    missing_rate = n_missing / n_total

    print(f"\nMissing Data Summary:")
    print(f"Total values: {n_total}")
    print(f"Missing values: {n_missing}")
    print(f"Missing rate: {missing_rate:.2%}")

    # Missing pattern by variable
    print("\nMissing Data by Variable:")
    missing_by_var = df_missing.drop(['time', 'U'], axis=1).isna().sum()
    print(missing_by_var)

    # Statistical comparison between complete and observed data
    print("\nStatistical Comparison (Complete vs. Observed):")
    for col in df_missing.columns[:-2]:  # Exclude U and time
        complete_stats = df_complete[col]
        observed_stats = df_missing[col].dropna()

        print(f"\n{col}:")
        print(f"Complete  - Mean: {np.mean(complete_stats):.3f}, Std: {np.std(complete_stats):.3f}")
        print(f"Observed - Mean: {np.mean(observed_stats):.3f}, Std: {np.std(observed_stats):.3f}")

    # Confounder analysis
    print("\nConfounder (U) Analysis:")
    print(f"U - Mean: {np.mean(df_missing['U']):.3f}, Std: {np.std(df_missing['U']):.3f}")
    print("\nCorrelations with U:")
    correlations = df_missing.drop('time', axis=1).corr()['U'].sort_values(ascending=False)
    print(correlations)

def generate_all_combinations():
    """Generate datasets for all combinations"""
    sample_sizes = [500, 1000, 3000, 5000]
    n_vars_list = [4, 6, 8]
    max_lags = [2, 3, 4]
    noise_types = ['gaussian', 'student_t']
    missing_rates = [0.1, 0.2, 0.3]

    for n in sample_sizes:
        for vars in n_vars_list:
            for lag in max_lags:
                for noise_type in noise_types:
                    for rate in missing_rates:
                        print(f"\nGenerating dataset: n={n}, vars={vars}, lag={lag}, "
                              f"noise={noise_type}, missing={rate:.0%}")

                        noise_params = {'scale': 0.1, 'df': 3} if noise_type == 'student_t' else {'scale': 0.1}
                        generator = LinearTimeSeriesGeneratorMCAR(
                            noise_type=noise_type,
                            noise_params=noise_params,
                            missing_rate=rate,
                            random_state=42
                        )

                        df_missing, df_complete = generator.generate_multivariate_ts(
                            n_points=n,
                            n_vars=vars,
                            max_lag=lag
                        )

                        save_dataset_and_graph(
                            df_missing=df_missing,
                            df_complete=df_complete,
                            n_vars=vars,
                            max_lag=lag,
                            sample_size=n,
                            noise_type=noise_type,
                            missing_rate=rate
                        )
                        print("Dataset and visualizations saved successfully")

if __name__ == "__main__":
    print("Generating linear time series with MCAR missing data and confounder...")

    # # Example case for testing
    # n_points = 1000
    # n_vars = 4
    # max_lag = 2
    # missing_rate = 0.2

    # # Generate example with Gaussian noise
    # generator = LinearTimeSeriesGeneratorMCAR(
    #     noise_type='gaussian',
    #     noise_params={'scale': 0.1},
    #     missing_rate=missing_rate,
    #     random_state=42
    # )

    # df_missing, df_complete = generator.generate_multivariate_ts(
    #     n_points=n_points,
    #     n_vars=n_vars,
    #     max_lag=max_lag
    # )

    # # Save and analyze example case
    # save_dataset_and_graph(
    #     df_missing=df_missing,
    #     df_complete=df_complete,
    #     n_vars=n_vars,
    #     max_lag=max_lag,
    #     sample_size=n_points,
    #     noise_type='gaussian',
    #     missing_rate=missing_rate
    # )

    # analyze_mcar_confounded_data(df_missing, df_complete, "Gaussian Example with MCAR and Confounder")

    # Generate all combinations
    # Uncomment the following line to generate all combinations
    generate_all_combinations()

!zip -r /content/output_D1C.zip /content/output_mcar_confounded

from google.colab import files
files.download('/content/output_D1C.zip')