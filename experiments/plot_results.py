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


def main():
    evaluator = Evaluator()
    results = evaluator.evaluate_all()

    # --- Individual Metrics ---
    plot_metric(results, "tool_misuse_rate", "Tool Misuse Rate per Run")
    plot_metric(results, "invalid_execution_rate", "Invalid Execution Rate per Run")
    plot_metric(results, "repeated_action_ratio", "Repeated Action Ratio per Run")
    plot_metric(results, "null_action_rate", "Null Action Rate per Run")

    # --- Tool Usage ---
    plot_tool_distribution(results)


if __name__ == "__main__":
    main()