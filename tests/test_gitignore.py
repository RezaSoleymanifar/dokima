import subprocess


def test_no_cache_files_tracked(record_property):
    record_property("proves", "30.1")
    files = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout.splitlines()
    bad = [f for f in files if "__pycache__" in f or f.endswith((".pyc", ".pyo"))]
    assert bad == []


def test_gitignore_covers_python_cache(record_property):
    record_property("proves", "30.1")
    out = subprocess.run(
        ["git", "check-ignore", "dokima/__pycache__/x.cpython-312.pyc"],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0
