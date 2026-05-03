import os
import matplotlib.pyplot as plt
from experiments.evaluator import Evaluator

# Directory to store plots
PLOT_DIR = "experiments/plots"
os.makedirs(PLOT_DIR, exist_ok=True)


def plot_metric(results, metric_name, title):
    values = [r[metric_name] for r in results]

    plt.figure()
    plt.plot(values, marker='o')
    plt.title(title)
    plt.xlabel("Run Index")
    plt.ylabel(metric_name)
    plt.grid()

    filepath = os.path.join(PLOT_DIR, f"{metric_name}.png")
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()  # 🔥 important


def plot_tool_distribution(results):
    from collections import Counter

    total_counter = Counter()

    for r in results:
        total_counter.update(r["tool_distribution"])

    clean_counter = {
        k: v for k, v in total_counter.items()
        if isinstance(k, str) and k.strip() != ""
    }

    tools = list(clean_counter.keys())
    counts = list(clean_counter.values())

    plt.figure()
    plt.bar(tools, counts)
    plt.title("Tool Usage Distribution")
    plt.xlabel("Tools")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)

    filepath = os.path.join(PLOT_DIR, "tool_distribution.png")
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()  # 🔥 important


def compare_metric(r1, r2, metric, label1, label2):
    v1 = [r[metric] for r in r1]
    v2 = [r[metric] for r in r2]

    plt.figure()
    plt.plot(v1, marker='o', label=label1)
    plt.plot(v2, marker='o', label=label2)
    plt.title(f"{metric} Comparison")
    plt.xlabel("Run Index")
    plt.ylabel(metric)
    plt.legend()
    plt.grid()

    filename = f"{metric}_comparison.png"
    filepath = os.path.join(PLOT_DIR, filename)
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()  # 🔥 important

def plot_model_comparison(aggregated):

    metrics = [
        "avg_tool_misuse_rate",
        "avg_invalid_execution_rate",
        "avg_repeated_action_ratio",
        "avg_null_action_rate"
    ]

    models = list(aggregated.keys())

    for metric in metrics:

        values = [aggregated[m][metric] for m in models]

        plt.figure()
        plt.bar(models, values)
        plt.title(f"{metric} (Model Comparison)")
        plt.xlabel("Model")
        plt.ylabel(metric)
        plt.xticks(rotation=30)
        plt.grid()

        filepath = os.path.join(PLOT_DIR, f"{metric}_comparison.png")
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()


def main():
    evaluator = Evaluator()
    model_results = evaluator.evaluate_by_model()
    aggregated = evaluator.aggregate_by_model(model_results)

    print("\n=== MODEL COMPARISON ===")
    for model, metrics in aggregated.items():
        print(f"\nModel: {model}")
        for k, v in metrics.items():
            print(f"{k}: {v: 3f}" if isinstance(v, float) else f"{k}: {v}")


    plot_model_comparison(aggregated)


if __name__ == "__main__":
    main()