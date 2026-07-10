#!/usr/bin/env python3
"""Runnable value-add starter for professor outreach.

The data shipped here is a small seed dataset, not a claimed lab result. Replace
`data/value_add_examples.csv` with real lab/public data to turn this scaffold
into a stronger contribution.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "data" / "advisor_profile.json"
EXAMPLES_PATH = ROOT / "data" / "value_add_examples.csv"


def load_profile() -> Dict[str, Any]:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def load_examples() -> List[Dict[str, str]]:
    with EXAMPLES_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def as_float(value: str) -> float:
    return float(str(value).strip())


def round_metric(value: float) -> float:
    return round(float(value), 4)


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def language_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    total = len(rows)
    citation_attempts = [r for r in rows if as_bool(r["answer_has_citation"])]
    correct_citations = [r for r in citation_attempts if r["retrieved_source"] == r["cited_source"]]
    unsupported = [r for r in rows if not as_bool(r["supported"])]
    fully_grounded = [r for r in rows if as_bool(r["supported"]) and r["retrieved_source"] == r["cited_source"]]
    return {
        "artifact": "claim-level citation faithfulness audit",
        "num_cases": total,
        "citation_precision": round_metric(len(correct_citations) / max(len(citation_attempts), 1)),
        "unsupported_claim_rate": round_metric(len(unsupported) / max(total, 1)),
        "fully_grounded_rate": round_metric(len(fully_grounded) / max(total, 1)),
        "failure_ids": [r["case_id"] for r in rows if (not as_bool(r["supported"])) or r["retrieved_source"] != r["cited_source"]],
    }


def vision_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    correct = [as_bool(r["correct"]) for r in rows]
    by_shift: Dict[str, List[bool]] = defaultdict(list)
    calibration_errors = []
    for r in rows:
        is_correct = as_bool(r["correct"])
        by_shift[r["shift_type"]].append(is_correct)
        calibration_errors.append(abs(as_float(r["confidence"]) - (1.0 if is_correct else 0.0)))
    return {
        "artifact": "distribution-shift failure audit",
        "num_cases": len(rows),
        "accuracy": round_metric(mean(float(x) for x in correct)),
        "mean_calibration_gap": round_metric(mean(calibration_errors)),
        "shift_failure_rate": {k: round_metric(1.0 - mean(float(x) for x in vals)) for k, vals in sorted(by_shift.items())},
        "worst_shift": max(by_shift, key=lambda k: 1.0 - mean(float(x) for x in by_shift[k])),
    }


def robotics_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    errors = [abs(as_float(r["predicted_progress"]) - as_float(r["expected_progress"])) for r in rows]
    successes = [as_bool(r["success"]) for r in rows]
    recovery_steps = [as_bool(r["recovery_action"] ) for r in rows]
    return {
        "artifact": "progress-state policy audit",
        "num_steps": len(rows),
        "mean_progress_error": round_metric(mean(errors)),
        "success_rate": round_metric(mean(float(x) for x in successes)),
        "recovery_action_rate": round_metric(mean(float(x) for x in recovery_steps)),
        "high_error_steps": [r["step_id"] for r in rows if abs(as_float(r["predicted_progress"]) - as_float(r["expected_progress"])) >= 0.25],
    }


def trustworthy_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    violations = [as_bool(r["violation_found"]) for r in rows]
    repaired = [as_bool(r["repaired_without_regression"]) for r in rows if as_bool(r["violation_found"])]
    weighted_risk = sum(as_float(r["severity"]) for r in rows if as_bool(r["violation_found"])) / max(sum(as_float(r["severity"]) for r in rows), 1.0)
    return {
        "artifact": "adaptive red-team regression harness",
        "num_cases": len(rows),
        "violation_rate": round_metric(mean(float(x) for x in violations)),
        "severity_weighted_risk": round_metric(weighted_risk),
        "repair_success_rate": round_metric(mean(float(x) for x in repaired)),
        "open_failures": [r["case_id"] for r in rows if as_bool(r["violation_found"]) and not as_bool(r["repaired_without_regression"])],
    }


def graph_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    train_times = [int(r["timestamp"]) for r in rows if r["split"] == "train"]
    test_times = [int(r["timestamp"]) for r in rows if r["split"] == "test"]
    min_test = min(test_times) if test_times else max(train_times or [0])
    leakage = [r for r in rows if r["split"] == "train" and int(r["timestamp"]) > min_test]
    relations: Dict[str, int] = defaultdict(int)
    for r in rows:
        relations[r["relation"]] += 1
    return {
        "artifact": "temporal graph split and constraint audit",
        "num_edges": len(rows),
        "temporal_leakage_count": len(leakage),
        "relation_counts": dict(sorted(relations.items())),
        "constraint_violation_rate": round_metric(mean(float(as_bool(r["constraint_violation"])) for r in rows)),
    }


def science_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    scored = []
    for r in rows:
        acquisition = as_float(r["predicted_score"]) + 0.5 * as_float(r["uncertainty"]) - 0.1 * as_float(r["experiment_cost"])
        scored.append((acquisition, r))
    scored.sort(reverse=True, key=lambda item: item[0])
    return {
        "artifact": "uncertainty-aware active-learning ranker",
        "num_candidates": len(rows),
        "top_candidates": [r["candidate_id"] for _, r in scored[:3]],
        "mean_uncertainty": round_metric(mean(as_float(r["uncertainty"]) for r in rows)),
        "best_acquisition_score": round_metric(scored[0][0] if scored else 0.0),
    }


def optimization_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    by_config: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_config[r["config"]].append(r)
    summaries = {}
    for config, vals in by_config.items():
        final_rows = [r for r in vals if int(r["epoch"]) == max(int(x["epoch"]) for x in vals if x["seed"] == r["seed"])]
        scores = [as_float(r["validation_metric"]) for r in final_rows]
        runtimes = [as_float(r["runtime_seconds"]) for r in final_rows]
        summaries[config] = {
            "mean_final_metric": round_metric(mean(scores)),
            "mean_runtime_seconds": round_metric(mean(runtimes)),
            "efficiency": round_metric(mean(scores) / max(mean(runtimes), 1e-9)),
        }
    best = max(summaries, key=lambda k: summaries[k]["efficiency"])
    return {"artifact": "training-dynamics efficiency audit", "configs": summaries, "best_efficiency_config": best}


def retrieval_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    by_query: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_query[r["query_id"]].append(r)
    ndcgs = []
    controls = set()
    explanation_hits = []
    for query, vals in by_query.items():
        vals = sorted(vals, key=lambda r: int(r["rank"])
        )
        dcg = sum((2 ** as_float(r["relevance"]) - 1) / math.log2(i + 2) for i, r in enumerate(vals[:3]))
        ideal = sorted(vals, key=lambda r: as_float(r["relevance"]), reverse=True)
        idcg = sum((2 ** as_float(r["relevance"]) - 1) / math.log2(i + 2) for i, r in enumerate(ideal[:3]))
        ndcgs.append(dcg / max(idcg, 1e-9))
        controls.update(r["controllable_feature"] for r in vals)
        explanation_hits.extend(as_bool(r["has_evidence"]) for r in vals[:3])
    return {
        "artifact": "transparent ranking evidence audit",
        "num_queries": len(by_query),
        "ndcg_at_3": round_metric(mean(ndcgs)),
        "top3_evidence_coverage": round_metric(mean(float(x) for x in explanation_hits)),
        "control_dimensions": sorted(controls),
    }


def education_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    by_concept: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_concept[r["concept"]].append(r)
    mastery = {concept: round_metric(mean(float(as_bool(r["response_correct"])) for r in vals)) for concept, vals in by_concept.items()}
    misconception_rate = mean(float(bool(r["misconception_label"].strip())) for r in rows)
    return {
        "artifact": "auditable tutoring misconception tracker",
        "num_events": len(rows),
        "concept_mastery_proxy": mastery,
        "misconception_rate": round_metric(misconception_rate),
        "mean_hint_quality": round_metric(mean(as_float(r["hint_quality"]) for r in rows)),
    }


def ml_metrics(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    correct = [int(as_float(r["prediction"]) == as_float(r["label"])) for r in rows]
    brier = mean((as_float(r["confidence"]) - as_float(r["label"])) ** 2 for r in rows)
    by_group: Dict[str, List[int]] = defaultdict(list)
    for r in rows:
        by_group[r["group"]].append(int(as_float(r["prediction"]) == as_float(r["label"])))
    group_acc = {g: round_metric(mean(vals)) for g, vals in by_group.items()}
    gap = max(group_acc.values()) - min(group_acc.values()) if group_acc else 0.0
    return {
        "artifact": "auditable decision-support model card metrics",
        "num_records": len(rows),
        "accuracy": round_metric(mean(correct)),
        "brier_score": round_metric(brier),
        "group_accuracy": group_acc,
        "max_group_accuracy_gap": round_metric(gap),
    }


METRIC_FUNCTIONS = {
    "language": language_metrics,
    "vision": vision_metrics,
    "robotics": robotics_metrics,
    "trustworthy": trustworthy_metrics,
    "graphs": graph_metrics,
    "science": science_metrics,
    "optimization": optimization_metrics,
    "retrieval": retrieval_metrics,
    "education": education_metrics,
    "ml": ml_metrics,
}


def run_demo() -> Dict[str, Any]:
    profile = load_profile()
    rows = load_examples()
    kind = profile["project_family"]
    metrics = METRIC_FUNCTIONS[kind](rows)
    return {
        "professor": profile["professor"],
        "university": profile["university"],
        "research_area": profile["research_area"],
        "project_family": kind,
        "value_add": profile["value_add_artifact"],
        "metrics": metrics,
        "next_step": profile["next_step"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the professor-aligned value-add demo.")
    parser.add_argument("--write-report", type=Path, help="Optional path for JSON output.")
    args = parser.parse_args()
    result = run_demo()
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.write_report:
        args.write_report.parent.mkdir(parents=True, exist_ok=True)
        args.write_report.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
