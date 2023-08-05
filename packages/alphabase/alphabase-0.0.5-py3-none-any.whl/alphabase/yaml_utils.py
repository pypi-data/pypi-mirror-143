# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev_nbs/yaml_utils.ipynb (unless otherwise specified).

__all__ = ['load_yaml', 'save_yaml']

# Cell
import yaml

def load_yaml(filename)->dict:
    with open(filename) as f:
        settings = yaml.load(f, Loader=yaml.FullLoader)
    return settings

def save_yaml(filename, settings):
    with open(filename, "w") as file:
        yaml.dump(settings, file)