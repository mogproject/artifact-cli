import sys
import os
from .settings import Settings


def main():
    """
    Main function
    """
    settings = Settings().parse_args(sys.argv).load_environ(os.environ).load_config()
    return settings.configure_logging().operation.run(settings.repo)
