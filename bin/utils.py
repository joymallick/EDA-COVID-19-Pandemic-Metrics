import yaml


def load_config(config_file):
    """The function loads configuration parameters
    stored in config_file (.yaml).

    Args:
        config_file (str): path of the configuration file

    Raises:
        ValueError: when config_file not a  .yaml file

    Returns:
        dict: configuration params
    """
    if ('.yaml' not in config_file):
        message = 'Please provide a .yaml file'
        raise ValueError(message)
    with open(config_file) as file:
        config = yaml.safe_load(file)

    return config