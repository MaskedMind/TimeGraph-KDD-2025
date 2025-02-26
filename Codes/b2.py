# -*- coding: utf-8 -*-
"""B2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wzEKwOazMI4xAYnNvQnSb4tWnwVE5buK
"""

!pip install tigramite

import numpy as np
import pandas as pd
from scipy import stats
from tigramite import plotting as tp
import matplotlib.pyplot as plt
from pathlib import Path

def get_nonlinear_equations_no_u(n_vars, max_lag):
    """Get nonlinear equations without confounder U"""
    if n_vars == 4:
        if max_lag == 2:
            return [
                "X4[t] = 0.25 * X1[t-2]^2 - 0.1 * X1[t-2]^3 + e4",
                "X3[t] = 0.35 * X4[t]^2 - 0.15 * X4[t]^3 + e3",
                "X2[t] = 0.3 * X3[t-1]^2 - 0.05 * X3[t-1]^3 + e2",
                "X1[t] = 0.4 * X2[t]^2 - 0.2 * X2[t]^3 + e1"
            ]
        elif max_lag == 3:
            return [
                "X4[t] = 0.25 * X1[t-2]^2 - 0.1 * X1[t-2]^3 + e4",
                "X3[t] = 0.35 * X4[t]^2 - 0.15 * X4[t]^3 + 0.2 * X2[t-3]^2 + e3",
                "X2[t] = 0.3 * X3[t-1]^2 - 0.05 * X3[t-1]^3 + e2",
                "X1[t] = 0.4 * X2[t]^2 - 0.2 * X2[t]^3 + e1"
            ]
        elif max_lag == 4:
            return [
                "X4[t] = 0.25 * X1[t-4]^2 - 0.1 * X1[t-4]^3 + e4",
                "X3[t] = 0.35 * X4[t]^2 - 0.15 * X4[t]^3 + 0.2 * X2[t-3]^2 + e3",
                "X2[t] = 0.3 * X3[t-1]^2 - 0.05 * X3[t-1]^3 + e2",
                "X1[t] = 0.4 * X2[t]^2 - 0.2 * X2[t]^3 + e1"
            ]
    elif n_vars == 6:
        base_equations = get_nonlinear_equations_no_u(4, max_lag)
        additional = [
            "X6[t] = 0.45 * X5[t]^2 - 0.15 * X5[t]^3 + e6",
            "X5[t] = 0.3 * X4[t-1]^2 - 0.1 * X4[t-1]^3 + e5"
        ]
        return additional + base_equations
    elif n_vars == 8:
        base_equations = get_nonlinear_equations_no_u(6, max_lag)
        additional = [
            "X8[t] = 0.4 * X7[t]^2 - 0.12 * X7[t]^3 + e8",
            "X7[t] = 0.35 * X6[t-1]^2 - 0.08 * X6[t-1]^3 + e7"
        ]
        return additional + base_equations
    return []

class MixedNonlinearGenerator:
    def __init__(self, noise_mix_ratio=0.5, noise_params={'scale': 0.1}, random_state=None):
        """
        Initialize generator with mixed Gaussian and Laplace noise

        Parameters:
        noise_mix_ratio: float between 0 and 1, proportion of Gaussian noise (1-ratio is Laplace)
        noise_params: dict with 'scale' parameter for both distributions
        random_state: int, random seed
        """
        self.noise_mix_ratio = noise_mix_ratio
        self.noise_params = noise_params
        self.random_state = random_state
        if random_state is not None:
            np.random.seed(random_state)

    def generate_mixed_noise(self, size):
        """Generate mixed Gaussian and Laplace noise"""
        # Generate mask for mixing
        mask = np.random.random(size) < self.noise_mix_ratio

        # Generate both types of noise
        gaussian_noise = np.random.normal(0, self.noise_params['scale'], size=size)
        laplace_noise = np.random.laplace(0, self.noise_params['scale'], size=size)

        # Mix noise based on mask
        return np.where(mask, gaussian_noise, laplace_noise)

    def generate_irregular_timestamps(self, n_points, total_time, min_gap=0.1):
        """Generate irregular sampling times"""
        times = np.zeros(n_points)
        times[0] = np.random.uniform(0, min_gap)

        for i in range(1, n_points):
            gap = np.random.exponential(scale=(total_time-times[i-1])/(n_points-i))
            times[i] = times[i-1] + max(gap, min_gap)

            if times[i] > total_time:
                times = times * (total_time / times[i])

        return times

    def find_nearest_lag_idx(self, timestamps, current_idx, lag_time):
        """Find index of nearest available past observation for given lag"""
        target_time = timestamps[current_idx] - lag_time
        past_timestamps = timestamps[:current_idx]
        if len(past_timestamps) == 0:
            return 0
        return (np.abs(past_timestamps - target_time)).argmin()

    def generate_equations(self, t, X, lag_indices, n_vars, max_lag):
        """Execute nonlinear polynomial equations with irregular sampling"""
        noise = self.generate_mixed_noise(n_vars)
        equations = get_nonlinear_equations_no_u(n_vars, max_lag)
        true_links = extract_coefficients_from_equations(equations)

        # Generate values based on nonlinear relationships
        for i in range(n_vars-1, -1, -1):
            var_name = f'X{i+1}'
            value = 0

            # Add causal influences with polynomial terms
            for (source, lag, target, power), coef in true_links.items():
                if target == var_name:
                    source_idx = int(source[1:]) - 1
                    if lag == 0:
                        value += coef * (X[t, source_idx] ** power)
                    else:
                        lag_idx = lag_indices[abs(lag)-1]
                        value += coef * (X[lag_idx, source_idx] ** power)

            # Add noise term
            X[t, i] = value + noise[i]

    def generate_multivariate_ts(self, n_points, n_vars, max_lag, total_time=100, min_gap=0.1):
        """Generate multivariate time series with irregular sampling"""
        # Initialize arrays
        X = np.zeros((n_points, n_vars))

        # Generate irregular timestamps
        timestamps = self.generate_irregular_timestamps(n_points, total_time, min_gap)

        # Initialize first steps with noise
        for i in range(max_lag):
            X[i] = self.generate_mixed_noise(n_vars)

        # Generate time series
        for t in range(max_lag, n_points):
            mean_diff = np.mean(np.diff(timestamps))
            lag_indices = [self.find_nearest_lag_idx(timestamps, t, i * mean_diff)
                         for i in range(1, max_lag + 1)]

            self.generate_equations(t, X, lag_indices, n_vars, max_lag)

        # Create DataFrame
        columns = [f'X{i+1}' for i in range(n_vars)]
        df = pd.DataFrame(X, columns=columns)
        df['time'] = timestamps

        return df

def extract_coefficients_from_equations(equations):
    """Extract coefficients and relationships from equations"""
    causal_links = {}

    for eq in equations:
        if '=' not in eq:
            continue

        left, right = [side.strip() for side in eq.split('=')]
        if 'e' in right and len(right.split('+')) == 1:
            continue  # Skip pure noise equations

        target = left.split('[')[0]
        terms = [term.strip() for term in right.split('+')]

        for term in terms:
            if '*' not in term or 'X' not in term:
                continue

            parts = term.split('*')
            coeff = float(parts[0].strip())
            var_part = parts[1].strip()
            base_var = var_part.split('^')[0] if '^' in var_part else var_part
            var = base_var.split('[')[0]

            power = 1
            if '^' in var_part:
                power = int(var_part.split('^')[1].split(' ')[0])

            lag_part = base_var.split('[')[1].split(']')[0]
            lag = 0 if lag_part == 't' else -int(lag_part.split('-')[1])

            causal_links[(var, lag, target, power)] = coeff

    return causal_links

def extract_linear_links_for_graph(equations):
    """Extract linear causal links for graph visualization"""
    links = {}

    for eq in equations:
        if '=' in eq:
            left, right = [side.strip() for side in eq.split('=')]
            target = left.split('[')[0]

            terms = [term.strip() for term in right.split('+')]
            for term in terms:
                if '*' in term and 'X' in term:
                    # Get base coefficient (first number from polynomial terms)
                    parts = term.split('*')
                    coeff = float(parts[0].strip())
                    var_part = parts[1].strip()

                    # Get variable name without power terms
                    var = var_part.split('^')[0].split('[')[0]
                    lag_part = var_part.split('[')[1].split(']')[0]

                    lag = 0 if lag_part == 't' else -int(lag_part.split('-')[1])
                    links[(var, lag, target)] = coeff

    return links

def save_dataset_and_graph(df, n_vars, max_lag, sample_size, gaussian_ratio, output_dir="output_mixed"):
    """Save dataset and create causal graph visualization"""
    gaussian_pct = int(gaussian_ratio * 100)
    laplace_pct = 100 - gaussian_pct
    dir_path = f"{output_dir}/gaussian_{gaussian_pct}_laplace_{laplace_pct}"
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    base_filename = f'{dir_path}/mixed_ts_n{sample_size}_vars{n_vars}_lag{max_lag}'

    # Save dataset
    df.to_csv(f'{base_filename}.csv', index=False)

    # Get equations and extract links
    equations = get_nonlinear_equations_no_u(n_vars, max_lag)
    true_links = extract_linear_links_for_graph(equations)

    # Create variable names
    var_names = [f'X{i+1}' for i in range(n_vars)]
    val_matrix = np.zeros((n_vars, n_vars, max_lag + 1))
    graph_matrix = np.zeros((n_vars, n_vars, max_lag + 1), dtype='bool')

    # Fill matrices based on true links
    for (source, lag, target), weight in true_links.items():
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
        link_colorbar_label='Nonlinear Effect Strength',
        node_size=0.05
    )
    plt.title(f'Nonlinear Causal Graph (n={sample_size}, vars={n_vars}, lag={max_lag})\nGaussian: {gaussian_pct}%, Laplace: {laplace_pct}%')
    plt.savefig(f'{base_filename}_graph.png')
    plt.close()

    # Plot time series
    plt.figure(figsize=(15, 10))
    for col in df.columns[:-1]:  # Exclude time
        plt.plot(df['time'], df[col], label=col, alpha=0.7)
    plt.title(f'Time Series (n={sample_size}, vars={n_vars}, lag={max_lag})')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{base_filename}_series.png')
    plt.close()

    # Save causal structure description
    with open(f'{base_filename}_structure.txt', 'w') as f:
        f.write(f"True Nonlinear Causal Structure (Gaussian: {gaussian_pct}%, Laplace: {laplace_pct}%):\n")
        f.write("Format: (source, lag, target) => weight\n")
        for link, weight in true_links.items():
            f.write(f"{link} => {weight}\n")

def analyze_mixed_data(df, title="Mixed Error Time Series Analysis"):
    """Analyze and plot the time series data"""
    print(f"\nAnalyzing {title}")
    print("=" * 50)

    # Time Series Plot
    plt.figure(figsize=(15, 10))
    plt.subplot(2, 1, 1)
    for col in df.columns:
        if col != 'time':
            plt.plot(df['time'], df[col], label=col, alpha=0.7)
    plt.title(f"{title} - Time Series")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)

    # Sampling Intervals
    plt.subplot(2, 1, 2)
    time_diffs = np.diff(df['time'])
    plt.hist(time_diffs, bins=50, density=True)
    plt.title("Distribution of Sampling Intervals")
    plt.xlabel("Time Difference")
    plt.ylabel("Density")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Summary Statistics
    print("\nSummary Statistics:")
    print("-" * 30)
    print(df.drop('time', axis=1).describe())

    # Correlation Analysis
    print("\nCorrelation Matrix:")
    print("-" * 30)
    corr = df.drop('time', axis=1).corr()
    print(corr)

def generate_all_combinations():
    """Generate datasets for all combinations"""
    sample_sizes = [500, 1000, 3000, 5000]
    n_vars_list = [4, 6, 8]
    max_lags = [2, 3, 4]
    mix_ratios = [0.3, 0.5, 0.7]

    for n in sample_sizes:
        for vars in n_vars_list:
            for lag in max_lags:
                for ratio in mix_ratios:
                    gaussian_pct = int(ratio * 100)
                    laplace_pct = 100 - gaussian_pct
                    print(f"\nGenerating dataset: n={n}, vars={vars}, lag={lag}, gaussian={gaussian_pct}%, laplace={laplace_pct}%")

                    generator = MixedNonlinearGenerator(
                        noise_mix_ratio=ratio,
                        noise_params={'scale': 0.1},
                        random_state=42
                    )

                    df = generator.generate_multivariate_ts(
                        n_points=n,
                        n_vars=vars,
                        max_lag=lag,
                        total_time=100,
                        min_gap=0.1
                    )

                    # Save dataset and create visualizations
                    save_dataset_and_graph(
                        df=df,
                        n_vars=vars,
                        max_lag=lag,
                        sample_size=n,
                        gaussian_ratio=ratio
                    )
                    print("Dataset and visualizations saved successfully")

if __name__ == "__main__":
    print("Generating mixed error time series...")

    # # Example case
    # n_points = 1000
    # n_vars = 4
    # max_lag = 2

    # generator = MixedNonlinearGenerator(
    #     noise_mix_ratio=0.7,
    #     noise_params={'scale': 0.1},
    #     random_state=42
    # )

    # df = generator.generate_multivariate_ts(
    #     n_points=n_points,
    #     n_vars=n_vars,
    #     max_lag=max_lag,
    #     total_time=100,
    #     min_gap=0.1
    # )

    # # Save and analyze example case
    # save_dataset_and_graph(
    #     df=df,
    #     n_vars=n_vars,
    #     max_lag=max_lag,
    #     sample_size=n_points,
    #     gaussian_ratio=0.7
    # )

    # analyze_mixed_data(df, "Mixed Gaussian-Laplace Example")

    # Generate all combinations
    # Uncomment the following line to generate all combinations
    generate_all_combinations()

!zip -r /content/output.zip /content/output_mixed

from google.colab import files
files.download('/content/output.zip')