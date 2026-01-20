from pathlib import Path
from shutil import copy


TOKEN_USED_BY_SQCSUB = Path.home() / "sqc_rpc_sched" / "jwt.token"


def cached_token(simulate: bool):
    device_name: str = "reimei-simulator" if simulate else "reimei"
    return Path.home() / "sqc_rpc_sched" / f"jwt-{device_name}.token"


def overwrite_auth_token(simulate: bool):
    cache_path = cached_token(simulate)
    if cache_path.exists() and cache_path.is_file():
        copy(cache_path, TOKEN_USED_BY_SQCSUB)
