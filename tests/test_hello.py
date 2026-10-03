import subprocess
import sys


def test_hello_prints_dokima_ok(record_property):
    record_property("proves", "27.1")
    result = subprocess.run(
        [sys.executable, "-m", "dokima.hello"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == "dokima ok\n"
