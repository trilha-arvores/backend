import os


class DirectoryService:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(current_dir, "../..",))

    @classmethod
    def absolute_path_from_project(cls, project_path):
        return os.path.join(cls.PROJECT_DIR, project_path)
