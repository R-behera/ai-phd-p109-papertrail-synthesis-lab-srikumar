# Reproducibility Commands

Run the starter value-add artifact:

```bash
python src/value_add.py --write-report reports/demo_results.json
python -m unittest discover -s tests
```

Expected output:

- JSON metrics printed to stdout.
- Optional report at `reports/demo_results.json`.
- Passing tests for the professor-specific profile and demo pipeline.

## Environment Notes

- Uses Python standard library for the starter demo.
- No third-party package is required for the starter demo or tests.
- Replace `data/value_add_examples.csv` with real public/lab-relevant data before claiming results.
