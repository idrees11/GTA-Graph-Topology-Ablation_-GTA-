# .github/scripts/process_submission.py

from pathlib import Path
import subprocess
import sys
import os

repo_root = Path(__file__).parent.parent.parent.resolve()  # .github/scripts -> repo root

def main(pr_number=None):
    python_exe = sys.executable

    submissions_dir = repo_root / "submissions"
    print(f"DEBUG: Submissions directory: {submissions_dir}")

    if not submissions_dir.exists():
        print("No submissions directory found")
        return

    print("DEBUG: Listing submissions folder contents:")
    for item in submissions_dir.iterdir():
        print(f"  {item.name}")

    print("Decrypting and scoring submissions...")

    # Optional: pass PR number as environment variable if needed
    env = os.environ.copy()
    if pr_number:
        env["PR_NUMBER"] = str(pr_number)
        print(f"DEBUG: Running for PR number {pr_number}")

    # Run update_leaderboard.py
    subprocess.run(
        [python_exe, str(repo_root / "leaderboard/update_leaderboard.py")],
        check=True,
        env=env
    )

    print("Processing complete!")


if __name__ == "__main__":
    # Optionally read PR_NUMBER from environment (set via workflow input)
    pr_number = os.environ.get("PR_NUMBER")
    main(pr_number)
