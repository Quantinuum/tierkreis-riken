import logging
from pathlib import Path
from shutil import copy

logger = logging.getLogger(__name__)
TOKEN_USED_BY_SQCSUB = Path.home() / ".sqc_rpc_sched" / "jwt.token"
CACHED_TOKEN = Path.home() / ".sqc_rpc_sched" / "jwt-ibm-kobe-dacc.token"


def overwrite_auth_token():
    logger.info(f"Overwriting auth token {CACHED_TOKEN} {TOKEN_USED_BY_SQCSUB}")
    if CACHED_TOKEN.exists() and CACHED_TOKEN.is_file():
        copy(CACHED_TOKEN, TOKEN_USED_BY_SQCSUB)
