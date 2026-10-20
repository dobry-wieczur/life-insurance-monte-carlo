# Validation

The numerical checks are included in [`analysis.ipynb`](analysis.ipynb). The commands below reproduce the mortality-data extract and rerun the notebook from the beginning.

## Reproduce

From the repository root:

```bash
uv sync --locked
uv run --locked python scripts/extract_mortality.py
uv run --locked python scripts/run_notebook.py --offline-check
```

`extract_mortality.py` checks the bundled workbook's SHA-256 hash, worksheet labels and selected mortality values before recreating `data/mortality_2025.csv`.

`run_notebook.py` executes every code cell in a fresh Jupyter kernel and saves the outputs to `analysis.ipynb`. The `--offline-check` option blocks non-local socket connections from the kernel to check that the analysis runs using the bundled data. **Running these commands rewrites the CSV and the notebook.**

## Checks

| Area | Verification |
| --- | --- |
| Inputs | Valid group dimensions, integer policy counts, death probabilities in $[0,1]$ and positive benefits |
| Analytic moments | Mean and variance checked against direct enumeration in a two-person example |
| Monte Carlo | Simulated mean and unbiased variance within six theoretical standard errors of their analytic values; the variance check uses the fourth central moment |
| Random sampling | Reproducible results with fixed seeds; deterministic outcomes for $q=0$ and $q=1$ |
| Tail calculations | Strict `>` thresholds, inverse-CDF quantiles and continuity-corrected normal calculations on the payout grid |
| Portfolio comparisons | Theoretical $N^{-1/2}$ scaling of relative fluctuations; equal expected payouts and tenfold variance in the concentration comparison |

A successful notebook run produces five figures, six CSV tables and `summary.json` in [`outputs/`](outputs/). Dataset provenance and reuse conditions are documented in [`data/README.md`](data/README.md).
