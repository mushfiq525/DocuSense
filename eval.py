"""Run eval_questions.json against a running DocuSense API.
Usage: python eval.py [--url http://localhost:8000]
"""
import argparse
import json
import sys
from pathlib import Path

import requests

FALLBACK = "The provided documentation does not contain sufficient information to answer this question."


def run(url: str, questions_path: Path) -> bool:
    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    results = []

    for item in questions:
        question, expected = item["question"], item["expected_type"]
        try:
            resp = requests.post(f"{url}/api/query", json={"question": question}, timeout=30)
            resp.raise_for_status()
            body = resp.json()
        except requests.RequestException as e:
            results.append((question, expected, "ERROR", False))
            continue

        got_fallback = body["answer"].strip() == FALLBACK
        if expected == "fallback":
            passed, actual = got_fallback, "fallback" if got_fallback else "grounded"
        else:
            passed = (not got_fallback) and len(body.get("sources", [])) > 0
            actual = "grounded" if not got_fallback else "fallback"
        results.append((question, expected, actual, passed))

    print(f"\n{'PASS/FAIL':<10}{'EXPECTED':<12}{'ACTUAL':<12}QUESTION")
    print("-" * 100)
    n_pass = 0
    for question, expected, actual, passed in results:
        n_pass += passed
        print(f"{'PASS' if passed else 'FAIL':<10}{expected:<12}{actual:<12}{question[:60]}")
    print("-" * 100)
    print(f"{n_pass}/{len(results)} passed ({100 * n_pass / len(results):.0f}%)")
    return n_pass == len(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--questions", default="eval_questions.json")
    args = parser.parse_args()
    sys.exit(0 if run(args.url, Path(args.questions)) else 1)