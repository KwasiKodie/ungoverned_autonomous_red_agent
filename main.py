import importlib
from utils.helpers import get_url_by_key
from config.experiment_config import EXPERIMENTS, TARGETS, RUNS
from experiments.plot_results import main as plot_main


def load_experiment(class_name):
    module = importlib.import_module("experiments.scenario_1_ungoverned")
    return getattr(module, class_name)


def main():

    exp_config = EXPERIMENTS["ungoverned"]
    ExperimentClass = load_experiment(exp_config["class"])

    for target_key in TARGETS:

        target = get_url_by_key(target_key)
        print(f"\n=== TARGET: {target_key} ({target}) ===")

        for run_id in range(RUNS):

            print(f"\n--- RUN {run_id + 1} ---")

            experiment = ExperimentClass(
                max_steps=exp_config["max_steps"]
            )

            result = experiment.run(target)

            print("[RESULT]:", result)

    print("\n=== GENERATING PLOTS ===")
    plot_main()


if __name__ == "__main__":
    main()