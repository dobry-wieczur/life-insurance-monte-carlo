# Mortality data

## Source

Statistics Poland (GUS), [*Trwanie życia w 2025 r.*, Table A](https://stat.gov.pl/obszary-tematyczne/ludnosc/trwanie-zycia/trwanie-zycia-w-2025-r-%2C2%2C20.html).

- **Reference year:** 2025
- **Published:** 27 July 2026
- **Obtained for this project:** 19 October 2026
- **Worksheet:** `Ogółem mężczyźni` (men in Poland, urban and rural combined)
- **Source file:** [`source/gus_table_a_2025.xlsx`](source/gus_table_a_2025.xlsx)
- **Workbook SHA-256:** `5dfcaa6b785770ec9c8bc09e26d406222c7f87d7d92af5f1b414d0352ac0fbf8`

## Extract

The file [`mortality_2025.csv`](mortality_2025.csv) contains three annual death probabilities from the `qx` column of the worksheet:

| Age | $q_x$ | XLSX cell |
| ---: | ---: | :--- |
| 30 | 0.00117 | B37 |
| 45 | 0.00346 | B52 |
| 60 | 0.01313 | B67 |

Here, $q_x$ is the probability of death before age $x+1$, conditional on reaching age $x$. The values were taken directly from the published table without rescaling or interpolation. The CSV also records sex and source-cell references.

To regenerate the CSV from the included workbook, run from the repository root:

```bash
uv run --locked python scripts/extract_mortality.py
```

The notebook reads the CSV directly. The mortality probabilities describe the general male population, while the portfolio sizes and insured benefits are hypothetical.

## Reuse

The mortality CSV is an extract of data published by Statistics Poland (GUS). The source, publication and acquisition dates, and extraction method are documented above.

The data are reused under the [GUS public-sector information reuse conditions](https://bip.stat.gov.pl/kontakt/ponowne-wykorzystywanie-informacji-sektora-publicznego/). GUS is not responsible for the results of subsequent processing.

The MIT license covers the project's original code and documentation. It does not apply to the GUS source data.
