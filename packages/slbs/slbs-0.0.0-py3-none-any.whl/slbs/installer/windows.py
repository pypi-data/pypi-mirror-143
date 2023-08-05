from slbs import path
from slbs.installer import _generate_installer_resources
from subprocess import check_call, DEVNULL


def create_installer_windows():
    _generate_installer_resources()
    try:
        check_call(
            ['makensis', 'Installer.nsi'], cwd=path('target/installer'),
            stdout=DEVNULL
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            "slbs could not find executable 'makensis'. Please install NSIS and "
            "add its installation directory to your PATH environment variable."
        ) from None
