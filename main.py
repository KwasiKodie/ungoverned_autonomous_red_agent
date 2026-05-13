import importlib
import time
from utils.helpers import get_url_by_key
from config.experiment_config import EXPERIMENTS, TARGETS, RUNS
from experiments.plot_results import main as plot_main
import os
from dotenv import load_dotenv

load_dotenv()

def load_experiment(class_name):
    module = importlib.import_module("experiments.scenario_1_ungoverned")
    return getattr(module, class_name)


def run_experiment_for_model(model_name):
    exp_config = EXPERIMENTS["ungoverned"]
    ExperimentClass = load_experiment(exp_config["class"])

    print(f"\n==============================")
    print(f"RUNNING MODEL: {model_name}")
    print(f"==============================")

    for target_key in TARGETS:

        target = get_url_by_key(target_key)
        print(f"\n=== TARGET: {target_key} ({target}) ===")

        for run_id in range(RUNS):

            print(f"\n--- RUN {run_id + 1} ---")

            if model_name == "gpt-4o-mini":
                experiment = ExperimentClass(
                    max_steps=10,
                    provider="openai",
                    model_name="gpt-4o-mini"
                )

            elif model_name == "claude-opus-4-5-20251101":
                experiment = ExperimentClass(
                    max_steps=10,
                    provider="claude",
                    model_name=os.getenv("CLAUDE_MODEL", "claude-opus-4-5-20251101"),
                )

            else:
                raise ValueError(f"Unsupported model: {model_name}")

            result = experiment.run(target)

            print("[RESULT]:", result)

            time.sleep(5)


def main():

    models = [
        "claude-opus-4-5-20251101",
        "gpt-4o-mini"
    ]

    for model in models:
        run_experiment_for_model(model)

    print("\n=== GENERATING PLOTS ===")
    plot_main()


if __name__ == "__main__":
    main()