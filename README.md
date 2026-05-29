# Sleep Dataset EDA

This repository contains a Python script for environment configuration, data cleaning, and exploratory data analysis (EDA) on a sleep dataset loaded from `dataset_2191_sleep.csv`.

## Contents

- `main.py` - the main script that loads, cleans, analyzes, and visualizes the dataset.
- `dataset_2191_sleep.csv` - the raw sleep dataset.
- `requirements.txt` - Python package requirements.
- `eda_outputs/` - generated output files from EDA (`data_summary.csv`, plots, etc.).

## Requirements

- Python 3.10 or newer
- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the analysis from the repository root:

```bash
python main.py
```

The script will:

1. Load `dataset_2191_sleep.csv`
2. Clean numeric columns and handle missing values
3. Drop duplicate rows
4. Generate summary statistics
5. Save EDA outputs to `eda_outputs/`

## Output files

After running the script, the following files will be created in `eda_outputs/`:

- `data_summary.csv` - summary statistics for all dataset columns
- `histograms.png` - histograms for numeric columns
- `correlation_matrix.png` - correlation heatmap
- `pairplot.png` - pairwise relationships between numeric features

## Project details

`main.py` performs the following steps:

- prints environment configuration information
- loads the dataset with `pandas`
- converts selected columns to numeric values
- fills missing numeric values with median values
- drops duplicate rows
- generates and saves visualizations using `seaborn`

## Notes

- If the dataset file is missing, the script raises a `FileNotFoundError`.
- The output directory `eda_outputs/` is created automatically if it does not exist.
- If any required package is missing, the script prints the missing package and exits.

## GitHub setup

If you want to upload this repository to GitHub, make sure your local Git configuration has valid authentication. For GitHub pushes, use either:

- HTTPS with a personal access token, or
- SSH with a registered SSH key.

Example push command once auth is configured:

```bash
git push ragini main
```
