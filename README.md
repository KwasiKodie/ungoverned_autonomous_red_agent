# Ungoverned Autonomous Red Agent

## Overview

This repository contains the implementation and experimental artifacts for the study:

**“Towards Reliable Autonomous Red Teaming: A Quantitative Analysis of Behavioural Failures in LLM-Based Agents”**

The project presents an empirical analysis of behavioral failure modes in ungoverned LLM-based autonomous penetration testing agents operating in controlled laboratory environments.

---

# Research Objective

The objective of this study is to analyze how autonomous penetration testing agents behave when operating without governance or deterministic safety controls.

The experiments evaluate:

* Autonomous decision generation
* Tool invocation behavior
* Failure propagation
* Exploration patterns
* Repetitive reasoning behavior

The study does **not** evaluate offensive effectiveness or real-world exploitation capability.

---

# Repository Structure

```text
.
├── experiments/
├── models/
├── tools/
├── logs/
├── config/
├── utils/
├── files/
├── main.py
├── requirements.txt
└── README.md
```

---

# Experimental Environment

All experiments were conducted within an isolated VirtualBox laboratory environment.

## Host-Only Network Configuration

```text
Host Adapter: 192.168.56.1/24
```

Example VM assignments:

```text
Kali Linux:        192.168.56.20
Metasploitable2:   192.168.56.10
DVWA:              DHCP Assigned
DC-1:              DHCP Assigned
```

---

# Vulnerable Machines Used

The following intentionally vulnerable machines were used during experimentation:

* Metasploitable2
* DVWA
* DC-1

These machines were deployed strictly for academic research purposes in isolated non-production environments.

---

# Models Evaluated

The experiments compare multiple language models:

* GPT-4o-mini
* Claude Opus 4.5

Model abstraction is implemented through modular client interfaces.

---

# Tools Used by the Agent

The autonomous agent can invoke the following tools:

* SQLMap
* Commix
* Metasploit
* Nuclei
* Curl
* Searchsploit

The system intentionally excludes governance and deterministic validation controls.

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/KwasiKodie/ungoverned_autonomous_red_agent.git
cd ungoverned_autonomous_red_agent
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Python Requirements

```bash
pip install -r requirements.txt
```

---

## 4. Install External Security Tools

The following tools must be installed separately:

```text
sqlmap
commix
nuclei
metasploit-framework
curl
searchsploit
```

Example (Kali Linux):

```bash
sudo apt install sqlmap curl exploitdb
```

---

# Environment Variables

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=<key>
CLAUDE_API_KEY=<key>
```

---

# Configuring Experiments

Experimental configuration is managed through:

```text
config/experiment_config.py
```

---

## Configuring Number of Runs

```python
RUNS = 5
```

Defines how many times each experiment is repeated per model and target.

Example:

```text
RUNS = 5
```

means the experiment will execute five independent runs for each configured target.

---

## Configuring Targets

```python
TARGETS = [
    "metasploitable2",
    "dvwa",
    "dc1"
]
```

Defines the vulnerable machines included in the experiment.

---

## Registering New Vulnerable Machines

When adding a new target to `TARGETS`, its corresponding IP address must also be added to:

```text
files/urls.json
```

Example:

```json
{
    "metasploitable2": "http://192.168.56.10",
    "dvwa": "http://192.168.56.30",
    "dc1": "http://192.168.56.40"
}
```

The key in `TARGETS` must exactly match the key in `urls.json`.

Failure to register the target in `urls.json` will prevent the experiment runner from resolving the machine address.

---

## Configuring Maximum Autonomous Steps

Maximum reasoning/execution iterations are configured in:

```text
main.py
```

Example:

```python
experiment = UngovernedExperiment(
    max_steps=10,
    provider="openai",
    model_name="gpt-4o-mini"
)
```

Where:

```text
max_steps = 10
```

limits the agent to ten autonomous decision cycles per run.

Increasing the number of runs or maximum steps may significantly increase runtime, API usage, and token consumption.

---

# Running Experiments

## Run Full Experiment Suite

```bash
python main.py
```

---

## Run Single Experiment

```bash
python experiments/scenario_1_ungoverned.py
```

---

# Experimental Outputs

The system automatically generates the following artifacts.

---

## Trace Logs

```text
logs/traces/
```

Contains step-by-step autonomous agent decisions and execution results.

---

## Metrics

```text
logs/metrics/
```

Contains computed evaluation metrics.

---

## Plots

```text
logs/plots/
```

Contains generated graphs used in analysis and reporting.

---

# Evaluation Metrics

The evaluator computes the following metrics:

* avg_tool_misuse_rate
* avg_invalid_execution_rate
* avg_repeated_action_ratio
* avg_null_action_rate
* avg_unique_tools
* avg_unique_targets

These metrics are used to analyze behavioral failure modes across experimental runs.

---

# Reproducing Results

To reproduce the experiments:

1. Configure the Host-Only network in VirtualBox
2. Deploy the vulnerable VMs
3. Confirm VM connectivity using `nmap`
4. Configure API keys
5. Configure experimental targets and runs
6. Execute `python main.py`
7. Run evaluation and plotting scripts

---

# Ethical Notice

This repository is provided strictly for academic and defensive cybersecurity research.

All experiments were conducted within isolated, intentionally vulnerable environments with explicit authorization.

The system must not be used against unauthorized targets.

---

# Limitations

This implementation intentionally excludes governance, validation, and deterministic policy enforcement mechanisms in order to study ungoverned autonomous behavior.

The experiments focus on behavioral analysis rather than exploitation success.

---

# Citation

If you use this repository in academic work, please cite the associated manuscript.

