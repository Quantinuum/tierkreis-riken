from sys import modules
from unittest.mock import Mock


def mock_pyqir() -> None:
    """Mock any pyqir modules we run into.

    We don't need pyqir and it doesn't have an installation candidate on some platforms.
    """

    modules["pyqir"] = Mock()
    modules["pytket.qir"] = Mock()
    modules["pytket.qir.conversion"] = Mock()
    modules["pytket.qir.conversion.api"] = Mock()
    modules["pytket.qir.conversion.qirgenerator"] = Mock()
