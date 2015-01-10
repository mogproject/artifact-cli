import sys
from settings import Settings


def main():
    """
    Main function
    """
    settings = Settings().parse_args(sys.argv).load_config()
    return settings.configure_logging().operation.run(settings.repo)
