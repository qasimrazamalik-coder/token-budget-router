
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_demo_contract():
    p=subprocess.run([sys.executable,str(ROOT/'skill/scripts/run.py'),str(ROOT/'examples/input.json'),'--mode','router'],capture_output=True,text=True,check=True)
    out=json.loads(p.stdout); assert isinstance(out,dict) and out
