# src/eval/report.py

def print_report(eval_result):
    print("\n=== EVALUATION REPORT ===")
    print(f"Passed: {eval_result['passed']}/{eval_result['total']}")
    print(f"Time: {eval_result['total_time']:.3f}s\n")

    for r in eval_result["results"]:
        status = "PASS" if r["pass"] else "FAIL"

        print(f"{status} | {r['query']}")
        print(f"score: {r['score']:.3f}")
        print(f"diversity: {r['diversity']:.2f}")
        print(f"theme: {r['expected_theme']}")
        print(f"preview: {r['best_match']}")
        print("-" * 40)
