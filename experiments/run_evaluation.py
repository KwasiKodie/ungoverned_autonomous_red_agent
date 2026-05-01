from experiments.evaluator import Evaluator


def main():
    evaluator = Evaluator()
    results = evaluator.evaluate_all()

    agg = evaluator.aggregate(results)

    for r in results:
        print("\n--- TRACE ---")
        for k, v in r.items():
            print(f"{k}: {v}")

    print("\n=== AGGREGATED METRICS ===")
    for k, v in agg.items():
        print(f"{k}: {v:.3f}")


if __name__ == "__main__":
    main()