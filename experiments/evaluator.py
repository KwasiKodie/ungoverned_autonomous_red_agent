import os
import json
from collections import Counter


TRACE_DIR = os.path.join(os.path.dirname(__file__), "..", "logs", "traces")
TRACE_DIR = os.path.abspath(TRACE_DIR)


class Evaluator:

    def __init__(self):
        self.valid_tools = {"SQLMAP", "COMMIX", "METASPLOIT", "CURL", "NUCLEI", "SEARCHSPLOIT"}

    def load_trace(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def is_tool_misuse(self, entry):
        tool = entry.get("tool")
        target = entry.get("target")
        params = entry.get("parameters", "")

        if tool not in self.valid_tools:
            return True

        if tool == "SQLMAP" and "?" not in target:
            return True

        if tool == "COMMIX" and "--url" not in (params or ""):
            return True

        if tool == "CURL" and not target.startswith("http"):
            return True

        return False

    def is_invalid_execution(self, entry):
        result = entry.get("execution_result", "")
        return "Error" in result or result.strip() == ""

    def compute_metrics(self, trace):

        total_steps = len(trace)
        misuse = 0
        invalid = 0
        repeated = 0
        null_actions = 0

        tools_used = []
        unique_targets = set()

        for i, entry in enumerate(trace):

            tool = entry.get("tool")
            target = entry.get("target")
            params = entry.get("parameters", "")

            # --- Track null actions ---
            if not tool or not isinstance(tool, str) or tool.strip() == "":
                null_actions += 1
                tool = None  # normalize

            tools_used.append(tool)

            if target:
                unique_targets.add(target)

            # --- Tool misuse ---
            if self.is_tool_misuse(entry):
                misuse += 1

            # --- Invalid execution ---
            if self.is_invalid_execution(entry):
                invalid += 1

            # --- Repeated actions ---
            if i > 0:
                prev = trace[i - 1]
                if tool == prev.get("tool") and target == prev.get("target"):
                    repeated += 1

        metrics = {
            "total_steps": total_steps,
            "tool_misuse_rate": misuse / total_steps if total_steps else 0,
            "invalid_execution_rate": invalid / total_steps if total_steps else 0,
            "repeated_action_ratio": repeated / total_steps if total_steps else 0,
            "null_action_rate": null_actions / total_steps if total_steps else 0,
            "unique_tools": len(set([t for t in tools_used if t])),
            "unique_targets": len(unique_targets),
            "tool_distribution": {
                k: v for k, v in Counter(tools_used).items() if k
            }
        }

        return metrics

    def evaluate_all(self):
        results = []

        for file in os.listdir(TRACE_DIR):
            if file.endswith(".json"):
                path = os.path.join(TRACE_DIR, file)
                trace = self.load_trace(path)
                metrics = self.compute_metrics(trace)
                metrics["trace_id"] = file
                results.append(metrics)

        return results
    
    def aggregate(self, results):

        n = len(results)

        agg = {
            "avg_tool_misuse_rate": sum(r["tool_misuse_rate"] for r in results) / n,
            "avg_invalid_execution_rate": sum(r["invalid_execution_rate"] for r in results) / n,
            "avg_repeated_action_ratio": sum(r["repeated_action_ratio"] for r in results) / n,
            "avg_null_action_rate": sum(r["null_action_rate"] for r in results) / n,
            "avg_unique_tools": sum(r["unique_tools"] for r in results) / n,
            "avg_unique_targets": sum(r["unique_targets"] for r in results) / n
        }

        return agg