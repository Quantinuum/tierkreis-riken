from pathlib import Path
from shutil import copy


TOKEN_USED_BY_SQCSUB = Path.home() / "sqc_rpc_sched" / "jwt.token"
CACHED_TOKEN = Path.home() / "sqc_rpc_sched" / "jwt-ibm-kobe-dacc.token"


def overwrite_auth_token():
    if CACHED_TOKEN.exists() and CACHED_TOKEN.is_file():
        copy(CACHED_TOKEN, TOKEN_USED_BY_SQCSUB)
