# Unique Prototype Algorithm

## Algorithm

**SrikumarEvidenceNlpRepairLoop** (`P109-Srikumar-Nlp`)

## Professor Alignment

- Professor: Vivek Srikumar
- Research area: Machine learning, NLP, structured prediction, neuro-symbolic methods
- Focus terms: NLP, structured prediction, neuro symbolic methods

## Core Mechanism

This prototype prioritizes unsupported claims and citation mismatches for advisor-domain literature audits.

## Decision Rule

Rank seed cases by language-specific priority score with Srikumar-aligned focus term 'NLP'.

## What The Code Adds

- A unique algorithm spec in `src/proposed_method.py`.
- A scoring function for the repo's `language` data schema.
- A ranked list of cases that should be reviewed, repaired, reproduced, or expanded first.
- Integration into `src/value_add.py`, so demo output includes the proposed method.

## Honest Status

This is a runnable algorithmic prototype. It is not a validated contribution to Vivek Srikumar's published work until the seed data is replaced with real public/lab-relevant data and the resulting claims are evaluated.

## Run

```bash
python src/proposed_method.py
python src/value_add.py --write-report reports/demo_results.json
python -m unittest discover -s tests
```
