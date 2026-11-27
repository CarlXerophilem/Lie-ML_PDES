"""Compatibility path for historical standalone experiment scripts."""
from pathlib import Path
import sys

delivery = Path(__file__).resolve().parents[2] / "delivery"
if str(delivery) not in sys.path:
    sys.path.insert(0, str(delivery))
