import subprocess
import os

SUBMISSION_DIR = "submissions"
PUBLIC_KEY = "encryption/public_key.pem"

ideal_csv = os.path.join(SUBMISSION_DIR, "ideal_submission.csv")
pert_csv = os.path.join(SUBMISSION_DIR, "perturbed_submission.csv")

aes_key = os.path.join(SUBMISSION_DIR, "aes_key.hex")

ideal_enc = os.path.join(SUBMISSION_DIR, "ideal_submission.enc")
pert_enc = os.path.join(SUBMISSION_DIR, "perturbed_submission.enc")

aes_enc = os.path.join(SUBMISSION_DIR, "aes_key.enc")

print("Generating AES key...")
subprocess.run(f"openssl rand -hex 32 > {aes_key}", shell=True)

print("Encrypting ideal submission...")
subprocess.run(
    f"openssl enc -aes-256-cbc -pbkdf2 -in {ideal_csv} -out {ideal_enc} -pass file:{aes_key}",
    shell=True
)

print("Encrypting perturbed submission...")
subprocess.run(
    f"openssl enc -aes-256-cbc -pbkdf2 -in {pert_csv} -out {pert_enc} -pass file:{aes_key}",
    shell=True
)

print("Encrypting AES key with RSA...")
subprocess.run(
    f"openssl pkeyutl -encrypt -pubin -inkey {PUBLIC_KEY} -in {aes_key} -out {aes_enc}",
    shell=True
)

print("Encryption completed.")
