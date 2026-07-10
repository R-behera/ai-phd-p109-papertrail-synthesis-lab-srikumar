#!/usr/bin/env python3
"""Unique prototype method for this professor-aligned repo.

This is a runnable algorithmic variant designed to make the repo more than a
name. It is not a validated research result until the seed data is replaced
with real public/lab-relevant data and evaluated honestly.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_PATH = ROOT / "data" / "value_add_examples.csv"
PROFILE_PATH = ROOT / "data" / "advisor_profile.json"

METHOD_SPEC = {
    "algorithm_id": "P109-Srikumar-Nlp",
    "algorithm_name": "SrikumarEvidenceNlpRepairLoop",
    "project_family": "language",
    "professor": "Vivek Srikumar",
    "focus": "NLP",
    "core_mechanism": "prioritizes unsupported claims and citation mismatches for advisor-domain literature audits",
    "decision_rule": "Rank seed cases by language-specific priority score with Srikumar-aligned focus term 'NLP'.",
    "review_threshold": 0.42,
    "shift_weights": {
        "viewpoint": 0.09,
        "context": 0.12,
        "annotation": 0.08,
        "domain": 0.14
    },
    "temporal_anchor": 2023,
    "temporal_scale": 3
}
COEFFICIENTS = {
    "risk": 0.46,
    "evidence": 0.44,
    "uncertainty": 0.27,
    "focus": 0.18
}
FOCUS_TERMS = [
    "NLP",
    "structured prediction",
    "neuro symbolic methods"
]


def _bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except Exception:
        return default


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def _clip(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def _round(value: float) -> float:
    return round(float(value), 4)


def _focus_overlap(*texts: str) -> float:
    joined = " ".join(texts).lower()
    hits = sum(1 for term in FOCUS_TERMS if term.lower() in joined)
    return hits / max(len(FOCUS_TERMS), 1)


def load_examples(path: Path = EXAMPLES_PATH) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_profile() -> Dict[str, Any]:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def _language_score(row: Dict[str, str]) -> Dict[str, Any]:
    citation_match = row.get("retrieved_source") == row.get("cited_source")
    unsupported_risk = 1.0 - float(_bool(row.get("supported")))
    citation_risk = 1.0 - float(citation_match)
    missing_citation = 1.0 - float(_bool(row.get("answer_has_citation")))
    focus_bonus = _focus_overlap(row.get("question", ""), row.get("claim", ""))
    priority = (
        COEFFICIENTS["risk"] * unsupported_risk
        + COEFFICIENTS["evidence"] * citation_risk
        + COEFFICIENTS["uncertainty"] * missing_citation
        + COEFFICIENTS["focus"] * focus_bonus
    )
    return {
        "case_id": row.get("case_id"),
        "priority_score": _round(priority),
        "action": "audit unsupported/citation-mismatched claim" if priority >= METHOD_SPEC["review_threshold"] else "keep as lower-priority grounded example",
        "signals": {"unsupported_risk": unsupported_risk, "citation_risk": citation_risk, "focus_bonus": _round(focus_bonus)},
    }


def _vision_score(row: Dict[str, str]) -> Dict[str, Any]:
    confidence = _clip(_float(row.get("confidence")))
    correct = _bool(row.get("correct"))
    confidence_error = abs(confidence - (1.0 if correct else 0.0))
    shift_bonus = METHOD_SPEC["shift_weights"].get(row.get("shift_type"), COEFFICIENTS["focus"])
    priority = COEFFICIENTS["risk"] * (1.0 - float(correct)) + COEFFICIENTS["uncertainty"] * confidence_error + shift_bonus
    return {
        "case_id": row.get("case_id"),
        "priority_score": _round(priority),
        "action": "add to professor-facing failure gallery" if priority >= METHOD_SPEC["review_threshold"] else "retain as calibration control",
        "signals": {"shift_type": row.get("shift_type"), "confidence_error": _round(confidence_error), "correct": correct},
    }


def _robotics_score(row: Dict[str, str]) -> Dict[str, Any]:
    progress_error = abs(_float(row.get("predicted_progress")) - _float(row.get("expected_progress")))
    failed = 1.0 - float(_bool(row.get("success")))
    recovery = float(_bool(row.get("recovery_action")))
    focus_bonus = _focus_overlap(row.get("instruction", ""), row.get("subgoal", ""))
    priority = COEFFICIENTS["risk"] * progress_error + COEFFICIENTS["evidence"] * failed + COEFFICIENTS["uncertainty"] * recovery + COEFFICIENTS["focus"] * focus_bonus
    return {
        "case_id": row.get("step_id"),
        "priority_score": _round(priority),
        "action": "inspect subgoal/progress model" if priority >= METHOD_SPEC["review_threshold"] else "use as stable trajectory control",
        "signals": {"progress_error": _round(progress_error), "failed": bool(failed), "recovery": bool(recovery)},
    }


def _trustworthy_score(row: Dict[str, str]) -> Dict[str, Any]:
    violation = float(_bool(row.get("violation_found")))
    unrepaired = violation * (1.0 - float(_bool(row.get("repaired_without_regression"))))
    severity = _float(row.get("severity")) / 5.0
    focus_bonus = _focus_overlap(row.get("category", ""))
    priority = COEFFICIENTS["risk"] * severity * violation + COEFFICIENTS["evidence"] * unrepaired + COEFFICIENTS["focus"] * focus_bonus
    return {
        "case_id": row.get("case_id"),
        "priority_score": _round(priority),
        "action": "open red-team repair task" if priority >= METHOD_SPEC["review_threshold"] else "monitor as regression control",
        "signals": {"severity": _round(severity), "violation": bool(violation), "unrepaired": bool(unrepaired)},
    }


def _graphs_score(row: Dict[str, str]) -> Dict[str, Any]:
    timestamp = _float(row.get("timestamp"))
    test_like = 1.0 if row.get("split") == "test" else 0.0
    constraint = float(_bool(row.get("constraint_violation")))
    relation_focus = _focus_overlap(row.get("relation", ""), row.get("source", ""), row.get("target", ""))
    temporal_pressure = _clip((timestamp - METHOD_SPEC["temporal_anchor"]) / max(METHOD_SPEC["temporal_scale"], 1.0))
    priority = COEFFICIENTS["risk"] * constraint + COEFFICIENTS["uncertainty"] * temporal_pressure + COEFFICIENTS["evidence"] * test_like + COEFFICIENTS["focus"] * relation_focus
    return {
        "case_id": row.get("edge_id"),
        "priority_score": _round(priority),
        "action": "inspect leakage/constraint edge" if priority >= METHOD_SPEC["review_threshold"] else "use as graph context edge",
        "signals": {"constraint": bool(constraint), "temporal_pressure": _round(temporal_pressure), "relation": row.get("relation")},
    }


def _science_score(row: Dict[str, str]) -> Dict[str, Any]:
    predicted = _float(row.get("predicted_score"))
    uncertainty = _float(row.get("uncertainty"))
    cost = _float(row.get("experiment_cost"))
    cost_penalty = cost / max(cost + 1.0, 1e-9)
    acquisition = 0.1 + COEFFICIENTS["evidence"] * predicted + COEFFICIENTS["uncertainty"] * uncertainty - COEFFICIENTS["risk"] * cost_penalty + COEFFICIENTS["focus"] * _focus_overlap(row.get("domain", ""))
    return {
        "case_id": row.get("candidate_id"),
        "priority_score": _round(acquisition),
        "action": "prioritize for simulated expert review" if acquisition >= METHOD_SPEC["review_threshold"] else "defer until uncertainty or cost improves",
        "signals": {"predicted_score": predicted, "uncertainty": uncertainty, "experiment_cost": cost, "cost_penalty": _round(cost_penalty)},
    }


def _optimization_score(row: Dict[str, str]) -> Dict[str, Any]:
    metric = _float(row.get("validation_metric"))
    calibration = _float(row.get("calibration_error"))
    runtime = _float(row.get("runtime_seconds"))
    epoch = _float(row.get("epoch"))
    efficiency = metric / max(runtime, 1e-9)
    priority = COEFFICIENTS["evidence"] * metric + COEFFICIENTS["focus"] * efficiency - COEFFICIENTS["risk"] * calibration + COEFFICIENTS["uncertainty"] * math.log1p(epoch) / 3.0
    return {
        "case_id": row.get("run_id"),
        "priority_score": _round(priority),
        "action": "candidate config for scale-up" if priority >= METHOD_SPEC["review_threshold"] else "keep as diagnostic baseline",
        "signals": {"config": row.get("config"), "efficiency": _round(efficiency), "calibration_error": calibration},
    }


def _retrieval_score(row: Dict[str, str]) -> Dict[str, Any]:
    relevance = _float(row.get("relevance")) / 3.0
    rank_discount = 1.0 / max(_float(row.get("rank")), 1.0)
    evidence = float(_bool(row.get("has_evidence")))
    control_bonus = _focus_overlap(row.get("controllable_feature", ""))
    priority = COEFFICIENTS["evidence"] * relevance * rank_discount + COEFFICIENTS["risk"] * (1.0 - evidence) + COEFFICIENTS["focus"] * control_bonus
    return {
        "case_id": f"{row.get('query_id')}:{row.get('doc_id')}",
        "priority_score": _round(priority),
        "action": "inspect evidence/control mismatch" if priority >= METHOD_SPEC["review_threshold"] else "retain ranking support example",
        "signals": {"relevance": relevance, "rank_discount": _round(rank_discount), "has_evidence": bool(evidence)},
    }


def _education_score(row: Dict[str, str]) -> Dict[str, Any]:
    incorrect = 1.0 - float(_bool(row.get("response_correct")))
    misconception = 1.0 if row.get("misconception_label", "").strip() else 0.0
    hint_gap = 1.0 - _clip(_float(row.get("hint_quality")))
    focus_bonus = _focus_overlap(row.get("concept", ""), row.get("misconception_label", ""))
    priority = COEFFICIENTS["risk"] * incorrect + COEFFICIENTS["evidence"] * misconception + COEFFICIENTS["uncertainty"] * hint_gap + COEFFICIENTS["focus"] * focus_bonus
    return {
        "case_id": row.get("event_id"),
        "priority_score": _round(priority),
        "action": "add to misconception intervention queue" if priority >= METHOD_SPEC["review_threshold"] else "use as mastery control example",
        "signals": {"incorrect": bool(incorrect), "misconception": bool(misconception), "hint_gap": _round(hint_gap)},
    }


def _ml_score(row: Dict[str, str]) -> Dict[str, Any]:
    prediction = _float(row.get("prediction"))
    label = _float(row.get("label"))
    confidence = _clip(_float(row.get("confidence")))
    error = 1.0 if prediction != label else 0.0
    calibration_gap = abs(confidence - label)
    group_focus = _focus_overlap(row.get("group", ""), row.get("split", ""))
    priority = COEFFICIENTS["risk"] * error + COEFFICIENTS["uncertainty"] * calibration_gap + COEFFICIENTS["focus"] * group_focus
    return {
        "case_id": row.get("record_id"),
        "priority_score": _round(priority),
        "action": "inspect subgroup/calibration failure" if priority >= METHOD_SPEC["review_threshold"] else "retain as model-card control row",
        "signals": {"error": bool(error), "calibration_gap": _round(calibration_gap), "group": row.get("group")},
    }


SCORERS = {
    "language": _language_score,
    "vision": _vision_score,
    "robotics": _robotics_score,
    "trustworthy": _trustworthy_score,
    "graphs": _graphs_score,
    "science": _science_score,
    "optimization": _optimization_score,
    "retrieval": _retrieval_score,
    "education": _education_score,
    "ml": _ml_score,
}


def score_case(row: Dict[str, str]) -> Dict[str, Any]:
    scorer = SCORERS[METHOD_SPEC["project_family"]]
    return scorer(row)


def run_method(rows: List[Dict[str, str]] | None = None, top_k: int = 3) -> Dict[str, Any]:
    rows = rows if rows is not None else load_examples()
    scored = [score_case(row) for row in rows]
    scored.sort(key=lambda item: item["priority_score"], reverse=True)
    return {
        "algorithm_id": METHOD_SPEC["algorithm_id"],
        "algorithm_name": METHOD_SPEC["algorithm_name"],
        "project_family": METHOD_SPEC["project_family"],
        "core_mechanism": METHOD_SPEC["core_mechanism"],
        "decision_rule": METHOD_SPEC["decision_rule"],
        "top_cases": scored[:top_k],
        "mean_priority_score": _round(_mean(item["priority_score"] for item in scored)),
    }


if __name__ == "__main__":
    print(json.dumps(run_method(), indent=2, sort_keys=True))
