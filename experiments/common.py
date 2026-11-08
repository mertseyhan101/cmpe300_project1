import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
sys.path.insert(0, os.path.join(ROOT, "analysis"))
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(FIGURES, exist_ok=True)


def load_program():
    spec = importlib.util.spec_from_file_location("program", os.path.join(ROOT, "src", "2023400213.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
