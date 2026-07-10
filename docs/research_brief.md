# Research Brief

## Project Name

PaperTrail Synthesis Lab: NLP for Srikumar-Aligned Research

## Motivation

This project targets the intersection of **Machine learning, NLP, structured prediction, neuro-symbolic methods** and PhD-level research readiness. The goal is to produce a publishable-style artifact with a clear claim, reproducible experiments, and an honest account of failures.

## Hypothesis

A focused system that combines domain-specific inductive bias with rigorous evaluation will outperform generic baselines on reliability, generalization, or interpretability for the advisor-aligned task.

## Core Research Question

Can a citation-faithful agent answer ambiguous scientific questions without inventing unsupported claims?

## Novel Contribution

1. Build a task definition and dataset split that reflects a real weakness in current models.
2. Add one measurable method or evaluation contribution tied to Vivek Srikumar's research area.
3. Report both positive results and failure cases with enough detail for another researcher to reproduce or challenge the claim.

## Data Plan

Semantic Scholar, arXiv metadata, Papers with Code, and an advisor-domain question set.

Advisor-specific slice: **Machine learning, NLP, structured prediction, neuro-symbolic methods**.

## Baselines

BM25 reader, dense retriever, reranker RAG, long-context LLM, and unverified agentic RAG.

## Main Method

Start with the strongest reproducible baseline, then add one explicit contribution: provenance tracking, uncertainty estimation, progress-state modeling, controllable ranking, graph constraints, adaptive stress testing, or domain-prior regularization depending on the final task.

## Evaluation Metrics

faithfulness, citation precision, retrieval recall, unsupported-claim rate, latency, and expert preference.

## Ablations

- Remove the domain-specific component.
- Remove uncertainty, verification, or interpretability module if present.
- Vary training data scale.
- Evaluate in-domain and out-of-domain splits.
- Run at least three seeds when stochastic training materially affects results.

## Failure Analysis

Maintain a failure bank with input, expected behavior, observed behavior, suspected cause, fix attempted, and whether the fix generalized.

## Five-Week Milestones

1. Literature map, exact task definition, dataset access, and baseline target.
2. Dataset pipeline, first baseline, metrics dashboard, and experiment registry.
3. Main method prototype and initial ablations.
4. Robustness, OOD, or counterfactual evaluation with failure taxonomy.
5. Final experiments, paper-style report, reproducibility package, and SOP-ready summary.
