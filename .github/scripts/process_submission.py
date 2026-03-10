import subprocess


def main():

    print("Decrypting submission...")
    subprocess.run(["python", "encryption/decrypt.py"])

    print("Scoring submission...")
    subprocess.run(["python", "leaderboard/score_submission.py"])

    print("Updating leaderboard...")
    subprocess.run(["python", "leaderboard/update_leaderboard.py"])


if __name__ == "__main__":
    main()
