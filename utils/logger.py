import json
import os
from datetime import datetime

LOG_DIR = "logs"
TRACE_DIR = os.path.join(LOG_DIR, "traces")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TRACE_DIR, exist_ok=True)


def _write_json(file_path, data):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                existing = json.load(f)
            except:
                existing = []
    else:
        existing = []

    existing.append(data)

    with open(file_path, "w") as f:
        json.dump(existing, f, indent=2)


def log_execution(entry):
    entry["timestamp"] = datetime.utcnow().isoformat()
    _write_json("logs/execution_logs.json", entry)


def log_decision(entry):
    entry["timestamp"] = datetime.utcnow().isoformat()
    _write_json("logs/decisions.json", entry)


def create_trace(trace_id):
    path = f"logs/traces/{trace_id}.json"
    with open(path, "w") as f:
        json.dump([], f)
    return path


def append_trace(trace_path, entry):
    os.makedirs(os.path.dirname(trace_path), exist_ok=True)

    if not os.path.exists(trace_path):
        with open(trace_path, "w") as f:
            json.dump([], f)

    entry["timestamp"] = datetime.utcnow().isoformat()

    with open(trace_path, "r+") as f:
        data = json.load(f)
        data.append(entry)

        # data.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

    with open(trace_path, "w") as f:
        json.dump(data, f, indent=2)