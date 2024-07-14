import yaml
import matplotlib.pyplot as plt


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


def set_plot_params(config_file):
    """The function sets the matplotlib parameters
    according to the ones provided in config_file.

    Args:
        config_file (_type_): path of the configuration file
    Returns:
        None
    """
    plot_params = load_config(config_file)
    for param, value in plot_params.items():
        if (param == 'style'):
            plt.style.use(value)
        else:
            plt.rcParams[param] = value
