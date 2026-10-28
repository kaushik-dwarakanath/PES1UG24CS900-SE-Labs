"""Regenerate final evidence; fail if analysis or regression tests fail."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / 'reports' / 'after'


def main():
    """Execute all required checks using this Python environment."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    checks = [
        ('pylint', ['pylint', '--persistent=n', 'pharmacy_manager.py']),
        ('bandit', ['bandit', '-r', 'pharmacy_manager.py']),
        ('flake8', ['flake8', 'pharmacy_manager.py']),
        ('tests', ['unittest', 'discover', '-v']),
    ]
    failed = False
    for name, arguments in checks:
        result = subprocess.run(
            [sys.executable, '-m', *arguments], cwd=ROOT,
            capture_output=True, text=True, check=False)
        filename = f'{name}_report.txt'
        (REPORTS / filename).write_text(
            result.stdout + result.stderr, encoding='utf-8')
        print(f'{name}: exit {result.returncode}')
        failed = failed or result.returncode != 0
    with tempfile.TemporaryDirectory() as directory:
        result = subprocess.run(
            [sys.executable, str(ROOT / 'pharmacy_manager.py')],
            cwd=directory, capture_output=True, text=True, check=False)
    (REPORTS / 'demo.txt').write_text(
        result.stdout + result.stderr, encoding='utf-8')
    failed = failed or result.returncode != 0
    print(f'demo: exit {result.returncode}')
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
