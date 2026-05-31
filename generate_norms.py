#!/usr/bin/env python3
"""
Generate age‑norm tables by simulating a virtual population.
Run this once before using NUQRO to replace hardcoded defaults.
"""

import json
import random
import math
from pathlib import Path

# Try to use numpy for speed, fallback to pure Python if not installed
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("numpy not installed. Using pure Python (slower but works).")

# Age groups and their assumed underlying population parameters
POPULATION_PARAMS = {
    "IQ": {
        "10-12": {"mean": 35, "sd": 8},
        "13-15": {"mean": 38, "sd": 8},
        "16-18": {"mean": 42, "sd": 8},
        "19-25": {"mean": 45, "sd": 9},
        "26-35": {"mean": 47, "sd": 9},
        "36-50": {"mean": 48, "sd": 9},
        "51+": {"mean": 46, "sd": 10}
    },
    "EQ": {
        "10-12": {"mean": 45, "sd": 10},
        "13-15": {"mean": 48, "sd": 10},
        "16-18": {"mean": 52, "sd": 11},
        "19-25": {"mean": 55, "sd": 11},
        "26-35": {"mean": 58, "sd": 11},
        "36-50": {"mean": 60, "sd": 12},
        "51+": {"mean": 62, "sd": 12}
    },
    "SQ": {
        "10-12": {"mean": 40, "sd": 9},
        "13-15": {"mean": 44, "sd": 9},
        "16-18": {"mean": 48, "sd": 10},
        "19-25": {"mean": 52, "sd": 10},
        "26-35": {"mean": 55, "sd": 10},
        "36-50": {"mean": 57, "sd": 11},
        "51+": {"mean": 58, "sd": 11}
    },
    "AQ": {
        "10-12": {"mean": 42, "sd": 11},
        "13-15": {"mean": 45, "sd": 11},
        "16-18": {"mean": 48, "sd": 11},
        "19-25": {"mean": 52, "sd": 12},
        "26-35": {"mean": 55, "sd": 12},
        "36-50": {"mean": 57, "sd": 12},
        "51+": {"mean": 58, "sd": 13}
    }
}

SAMPLE_SIZE = 1000

def generate_sample(mean, sd, size=SAMPLE_SIZE):
    """Generate random scores (normal distribution) clipped to 0-100."""
    if HAS_NUMPY:
        scores = np.random.normal(mean, sd, size)
    else:
        # Box-Muller transform
        scores = []
        for _ in range(size):
            u = random.random()
            v = random.random()
            z = math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)
            scores.append(mean + z * sd)
    # Clip to 0-100
    return [max(0, min(100, s)) for s in scores]

def compute_norms_from_sample(scores):
    """Return (mean, sd) from a list of scores."""
    n = len(scores)
    if n == 0:
        return (0, 0)
    mean = sum(scores) / n
    variance = sum((x - mean) ** 2 for x in scores) / (n - 1) if n > 1 else 0
    sd = variance ** 0.5
    return (round(mean, 2), round(sd, 2))

def generate_norms():
    norms = {}
    for test_type, groups in POPULATION_PARAMS.items():
        norms[test_type] = {}
        for age_group, params in groups.items():
            scores = generate_sample(params["mean"], params["sd"], SAMPLE_SIZE)
            mean_emp, sd_emp = compute_norms_from_sample(scores)
            norms[test_type][age_group] = {"mean": mean_emp, "sd": sd_emp}
            print(f"  {test_type} {age_group}: mean={mean_emp:.2f} (true={params['mean']}), sd={sd_emp:.2f}")
    return norms

def main():
    print("Generating norm tables from virtual population...")
    norms = generate_norms()
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    norms_file = data_dir / "norms.json"
    with open(norms_file, "w") as f:
        json.dump(norms, f, indent=4)
    print(f"\n✅ Norm tables written to {norms_file}")
    print("You can now run NUQRO (python main.py).")

if __name__ == "__main__":
    main()