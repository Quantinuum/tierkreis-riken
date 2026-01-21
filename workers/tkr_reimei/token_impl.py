from os import getenv
from pathlib import Path
import shutil
import subprocess
from typing import Literal
import requests
import json
import re
import logging
import time

from tierkreis.exceptions import TierkreisError


logger = logging.getLogger(__name__)

JWT_URL = "https://idp.qc.r-ccs.riken.jp/cgi-bin/get_qtm_key.cgi"
JWT_MAIL_KEY = "JWT_EMAIL"
JWT_PASSWORD_KEY = "JWT_PASSWORD"
JWT_TOKEN_NAME = "jwt.token"
HEADERS = {"Content-Type": "application/json"}
QPUS = ["reimei", "reimei-simulator", "ibm-kobe-dacc"]
SQC_DIR = Path.home() / ".sqc_rpc_sched"
INSTALL_CMD = "/vol0300/share/ra010014/jhpcq/x86/scripts/install-cert-files.sh"


def _is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[\w\-\.]+$"
    return re.match(pattern, email) is not None


def _get_token(
    raw_username: str, raw_password: str, output_file: Path = Path("~/jwt.token")
) -> None:
    """Taken from /vol0003/share/ra010014/jhpcq/bin/fetch_qtm_jwt.py"""
    username = raw_username.strip()
    password = raw_password.strip()

    # Check email format
    if not _is_valid_email(username):
        msg = f"Email {username}: Invalid email format."
        raise TierkreisError(msg)

    data = {"username": username, "password": password}

    try:
        response = requests.post(JWT_URL, json=data)
        response.raise_for_status()
        result = response.json()

        if result.get("success"):
            token = result.get("access_token")
            if token:
                # make sure file info is upto date
                if output_file.exists():
                    output_file.unlink()
                with open(output_file, "w+", encoding="utf-8") as f:
                    f.write(token)
                logger.info("Access token saved to '%s'", output_file)
            else:
                msg = "Access token not found in response."
                logger.error(msg)
                raise TierkreisError(msg)
        else:
            msg = f"Authentication failed: {result.get('error', 'Unknown error')}"
            logger.error(msg)
            raise TierkreisError(msg)

    except IOError | json.JSONDecodeError | requests.exceptions.RequestException as e:
        raise TierkreisError() from e


def set_up_token(token_dir: Path, qpu: str) -> Path:
    logger.info("Setting up tokens in %s", token_dir)
    token_dir.mkdir(parents=True, exist_ok=True)
    qpu_dir = token_dir / qpu
    if (qpu_dir / JWT_TOKEN_NAME).exists():
        logger.info("Token file exists, checking age...")
        file_age = time.time() - (qpu_dir / JWT_TOKEN_NAME).stat().st_mtime
        if file_age < 86400:  # 24 hours in seconds
            logger.info("Token is fresh, skipping setup")
            shutil.copytree(qpu_dir, SQC_DIR, dirs_exist_ok=True)
            return token_dir
    user_name = getenv(JWT_MAIL_KEY, None)
    password = getenv(JWT_PASSWORD_KEY, None)
    if user_name is None or password is None:
        msg = f"Cannot get JWT token. Make sure ${JWT_MAIL_KEY} and ${JWT_PASSWORD_KEY} are set"
        raise TierkreisError(msg)

    logger.info("Setting up %s in %s", qpu, token_dir)
    if qpu_dir.exists():
        shutil.rmtree(qpu_dir)
    qpu_dir.mkdir(exist_ok=True)

    logger.info("Calling the shell script for %s", qpu)
    process = subprocess.run([INSTALL_CMD, qpu])
    try:
        process.check_returncode()
    except subprocess.CalledProcessError as e:
        msg = f"Error when running {INSTALL_CMD} {qpu}"
        raise TierkreisError() from e
    shutil.copytree(SQC_DIR, qpu_dir, dirs_exist_ok=True)
    _get_token(user_name, password, qpu_dir / JWT_TOKEN_NAME)

    return token_dir


def set_up_tokens(token_dir: Path, qpus: list[str]) -> Path:
    logger.info("Setting up tokens in %s", token_dir)
    token_dir.mkdir(parents=True, exist_ok=True)
    user_name = getenv(JWT_MAIL_KEY, None)
    password = getenv(JWT_PASSWORD_KEY, None)
    if user_name is None or password is None:
        msg = f"Cannot get JWT token. Make sure ${JWT_MAIL_KEY} and ${JWT_PASSWORD_KEY} are set"
        raise TierkreisError(msg)
    for qpu in qpus:
        qpu_dir = token_dir / qpu
        logger.info("Setting up %s in %s", qpu, token_dir)
        if qpu_dir.exists():
            shutil.rmtree(qpu_dir)
        qpu_dir.mkdir(exist_ok=True)

        logger.info("Calling the shell script for %s", qpu)
        process = subprocess.run([INSTALL_CMD, qpu])
        try:
            process.check_returncode()
        except subprocess.CalledProcessError as e:
            msg = f"Error when running {INSTALL_CMD} {qpu}"
            raise TierkreisError() from e
        shutil.copytree(SQC_DIR, qpu_dir, dirs_exist_ok=True)
        _get_token(user_name, password, qpu_dir / JWT_TOKEN_NAME)

    return token_dir


def ensure_token(
    token_dir: Path,
    qpu: Literal["reimei", "reimei-simulator", "ibm-kobe-dacc"] = "reimei",
) -> Path:
    logger.info("Making sure the correct token exists.")
    if not token_dir.exists():
        logger.info("Token directory %s empty, setting up...", token_dir)
        _ = set_up_tokens(token_dir, [qpu])
    qpu_dir = token_dir / qpu
    if not qpu_dir.exists():
        msg = (
            f"Directory {qpu_dir} does not exist after setup."
            "Make sure your credentials are correct."
        )
        raise TierkreisError(msg)
    # Set up sqc dir
    if SQC_DIR.exists():
        shutil.rmtree(SQC_DIR)
    # copy the correct file
    logger.info("Copying %s -> %s", qpu_dir, token_dir)
    shutil.copytree(qpu_dir, SQC_DIR, dirs_exist_ok=True)
    return token_dir


def main() -> None:
    token_dir = Path.home() / ".tkr_tokens"
    _ = set_up_tokens(token_dir, QPUS)
    _ = ensure_token(token_dir, "reimei-simulator")


if __name__ == "__main__":
    # For testing only
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    main()
