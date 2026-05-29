#!/usr/bin/env python3
"""
Environment configuration, data cleaning, and exploratory data analysis
for the sleep dataset loaded from dataset_2191_sleep.csv.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
except ImportError as exc:
    missing = str(exc).split()[-1].strip("'")
    print("Missing required package:", missing)
    print("Install dependencies with: pip install -r requirements.txt")
    sys.exit(1)

sns.set(style="whitegrid", font_scale=1.1)
DATA_FILE = Path(__file__).resolve().parent / "dataset_2191_sleep.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "eda_outputs"


def configure_environment() -> None:
    print("Environment configuration")
    print("-------------------------")
    print(f"Python version: {sys.version.split()[0]}")
    print("Required packages:")
    print("  - pandas")
    print("  - numpy")
    print("  - matplotlib")
    print("  - seaborn")
    print("Run `pip install -r requirements.txt` if any import fails.")
    print()


def load_dataset(path: Path) -> pd.DataFrame:
    print(f"Loading dataset from {path}")
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, na_values=["?", "NA", "N/A", ""], skipinitialspace=True)
    df.columns = df.columns.str.strip()
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("Cleaning data")
    df = df.copy()

    numeric_columns = [
        "body_weight",
        "brain_weight",
        "max_life_span",
        "gestation_time",
        "predation_index",
        "sleep_exposure_index",
        "danger_index",
        "total_sleep",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    initial_shape = df.shape
    df = df.drop_duplicates(ignore_index=True)
    duplicate_count = initial_shape[0] - df.shape[0]
    if duplicate_count:
        print(f"Dropped {duplicate_count} duplicate rows")

    missing_before = df.isna().sum()
    print("Missing values before cleaning:")
    print(missing_before[missing_before > 0].to_string())

    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median(numeric_only=True))

    if df.isna().sum().sum() > 0:
        print("Remaining missing values after fill: ")
        print(df.isna().sum()[df.isna().sum() > 0].to_string())

    df = df.dropna(axis=0, how="all")

    print("Data types after conversion:")
    print(df.dtypes)
    print(f"Cleaned dataset contains {len(df)} rows")
    print()
    return df


def make_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.describe(include="all").transpose()
    summary = summary.rename(columns={
        "50%": "median",
        "count": "count",
        "mean": "mean",
        "std": "std",
        "min": "min",
        "25%": "25%",
        "75%": "75%",
        "max": "max",
    })
    return summary


def save_summary(summary: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "data_summary.csv"
    summary.to_csv(summary_path)
    print(f"Saved summary statistics to {summary_path}")


def plot_histograms(df: pd.DataFrame, output_dir: Path) -> None:
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 10))
    axes = axes.flatten()

    for ax, col in zip(axes, numeric_columns):
        sns.histplot(df[col], kde=True, ax=ax, color="#4c72b0")
        ax.set_title(col)

    for remaining in axes[len(numeric_columns) :]:
        remaining.axis("off")

    plt.tight_layout()
    path = output_dir / "histograms.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved histograms to {path}")


def plot_correlation(df: pd.DataFrame, output_dir: Path) -> None:
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation matrix")
    plt.tight_layout()
    path = output_dir / "correlation_matrix.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved correlation heatmap to {path}")


def plot_pairwise(df: pd.DataFrame, output_dir: Path) -> None:
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    path = output_dir / "pairplot.png"
    pairplot = sns.pairplot(df[numeric_columns], corner=True, plot_kws={"alpha": 0.7, "s": 40})
    pairplot.fig.suptitle("Pairwise relationships", y=1.02)
    pairplot.savefig(path, dpi=150)
    plt.close(pairplot.fig)
    print(f"Saved pairplot to {path}")


def perform_eda(df: pd.DataFrame, output_dir: Path) -> None:
    print("Performing EDA")
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = make_summary(df)
    save_summary(summary, output_dir)
    plot_histograms(df, output_dir)
    plot_correlation(df, output_dir)
    plot_pairwise(df, output_dir)
    print("EDA complete")


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    configure_environment()
    df = load_dataset(DATA_FILE)
    clean_df = clean_data(df)
    perform_eda(clean_df, OUTPUT_DIR)
    print(f"Generated outputs in {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
