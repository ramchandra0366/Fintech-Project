
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
SPARK_FOLDER = ROOT / "Spark"

STAGES = [
    "bronze_ingestion.py",
    "silver_transformation.py",
    "gold_transformation.py",
    "data_quality_checks.py",
]

print("\nStarting NovaBank Data Pipeline...\n", flush=True)

start_time = time.time()

for stage in STAGES:
    print(f"\nRunning: {stage}", flush=True)

    result = subprocess.run(
        [sys.executable, str(SPARK_FOLDER / stage)],
        cwd=ROOT,
        check=False,
    )

    if result.returncode != 0:
        print(f"\nPIPELINE FAILED at {stage}", flush=True)
        sys.exit(result.returncode)

    print(f"COMPLETED: {stage}", flush=True)

duration = time.time() - start_time

print("\nALL NOVABANK PIPELINE STAGES COMPLETED!")
print(f"Total execution time: {duration:.1f} seconds")
