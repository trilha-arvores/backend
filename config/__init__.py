import yaml
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(current_dir, ".."))


def absolute_path_from_project(project_path):
    return os.path.join(PROJECT_DIR, project_path)


def read_yaml_file(path: str) -> dict:
    with open(path) as file:
        return yaml.load(file, Loader=yaml.UnsafeLoader)


def load_config() -> dict:
    return read_yaml_file(absolute_path_from_project(f'config/config.yaml'))


config = load_config()
