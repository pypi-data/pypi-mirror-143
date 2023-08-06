# __version__ is placeholder
# It gets set in the build/publish process (publish_with_credentials.sh)
__version__ = "0.5.1-dev202203241648120799"

from jetpack._runtime.client import init
from jetpack._task.interface import function, jet, jetroutine, schedule, workflow
from jetpack.cmd import root
from jetpack.redis import redis


def run() -> None:
    # options can be passed in as env variables with JETPACK prefix
    # e.g. JETPACK_ENTRYPOINT
    root.cli(auto_envvar_prefix="JETPACK")
