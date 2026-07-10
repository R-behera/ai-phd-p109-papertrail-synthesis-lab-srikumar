# Professor Outreach Value-Add Packet

## Bottom Line

This repository is currently a **research proposal and execution scaffold**, not a completed result. Use it to show Professor Srikumar that you understand the research area and can contribute a concrete, reproducible artifact.

## Target Professor

- **Professor:** Vivek Srikumar
- **University:** University of Utah
- **Program:** Kahlert School of Computing PhD
- **Research area from CSV:** Machine learning, NLP, structured prediction, neuro-symbolic methods
- **Representative paper from CSV:** OSCaR: Orthogonal Subspace Correction and Rectification of Biases in Word Embeddings; 2021; EMNLP
- **Scholar link:** https://scholar.google.com/scholar?q=OSCaR%3A+Orthogonal+Subspace+Correction+and+Rectification+of+Biases+in+Word+Embeddings

## Proposed Value Add

Build **a citation-faithful RAG and evaluation harness for advisor-domain papers** focused on **NLP**.

### What You Can Contribute

- Build a clean literature ingestion pipeline over the lab's papers and closely related work.
- Create claim-level evaluation examples that test retrieval quality, unsupported claims, and citation faithfulness.
- Turn ambiguous research questions into reproducible benchmark cases with error taxonomies.

## Concrete Starter Project

Implement a small paper-to-claims pipeline, then evaluate BM25, dense retrieval, reranking, and a verified-answer agent on 50-100 domain questions.

## 30/60/90-Day Plan

### First 30 Days

- Re-read 3-5 recent lab papers and write a one-page problem framing memo.
- Build the first dataset or evaluation slice with documented source provenance.
- Reproduce one credible baseline and record exact commands.
- Create a failure bank with at least 20 concrete examples.

### Days 31-60

- Add the proposed method or evaluation contribution.
- Run ablations that isolate the contribution from data scale and model-size effects.
- Add robustness, temporal, domain-shift, or subgroup tests where relevant.
- Write interim results as a short lab-note style report.

### Days 61-90

- Expand the benchmark to 50-100 examples or the equivalent for the domain.
- Run statistical checks, seed variance checks, and cost/runtime analysis.
- Convert results into a paper-style technical report.
- Package the repo so another student can reproduce the main table.

## Deliverables To Offer The Professor

- A reproducible domain paper index with metadata and provenance.
- A 50-100 item expert-reviewable question set.
- Baseline comparison table with faithfulness and citation metrics.
- A failure bank of hallucination, retrieval miss, ambiguity, and contradiction cases.

## Skills This Demonstrates

retrieval systems, LLM evaluation, dataset curation, prompt/protocol design, reproducibility engineering.

## Honest Outreach Framing

Do **not** claim this is finished. The honest claim is:

> I prepared a concrete research scaffold aligned with your work and would like to turn it into a reproducible contribution if it matches your lab's current priorities.

## Sharing Note

This GitHub repository is public. Before emailing, verify the professor's current work, personalize the email, and be ready to explain exactly what is implemented versus planned.
