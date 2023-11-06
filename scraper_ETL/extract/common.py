"""

    Returns:

    """

import yaml

__config = None


def config():
    """

    Returns:

    """

    # Get access to global variable

    # If we don't get the config yet...
    if not __config:
        with open(
            "config.yaml",
            mode="r",
            encoding="utf-8",
        ) as f:
            config_1 = yaml.safe_load(f)

    return config_1
