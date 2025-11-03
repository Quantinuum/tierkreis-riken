import qnexus as qnx
from tierkreis.exceptions import TierkreisError


def qnexus_quantinuum_device_by_name(device_name: str) -> qnx.models.Device:
    devices = list(
        filter(
            lambda d: d.device_name == device_name,
            qnx.devices.get_all([qnx.models.IssuerEnum.QUANTINUUM]),
        )
    )
    if len(devices) != 1:
        raise TierkreisError(f"Could not find device '{device_name}'")
    return devices[0]
