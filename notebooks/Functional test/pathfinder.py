import os
import sys



class Pathfinder:

    def __init__(self, abs_paths = None):
        self.abs_paths = abs_paths


    @property
    def abs_paths(self):
        return self._abs_paths


    @abs_paths.setter
    def abs_paths(self, abs_paths):
        self._abs_paths = abs_paths


    @classmethod
    def relative_paths_from_abs(cls, abs_paths):
        relative_paths = sorted([cls.relative_path_from_abs(p) for p in abs_paths])
        cls._print_relative_paths(relative_paths)

        return relative_paths


    @classmethod
    def append_relative_paths(cls, relative_paths):
        abs_paths = cls.abs_paths_from_relative(relative_paths)
        cls.append_abs_paths(abs_paths)


    @classmethod
    def append_abs_paths(cls, abs_paths):
        for path in abs_paths:
            cls._append_abs_path(path)


    @classmethod
    def abs_paths_from_relative(cls, relative_paths):
        return sorted([cls.abs_path_from_relative(p) for p in relative_paths])


    # =============================

    @staticmethod
    def relative_path_from_abs(abs_path):
        def del_same_parents(target_path, current_path):
            if len(target_path) * len(current_path) > 0:
                if target_path[0] == current_path[0]:
                    target_path.pop(0)
                    current_path.pop(0)
                    del_same_parents(target_path, current_path)


        current_path = os.getcwd().replace('\\', os.sep).split(os.sep)
        abs_path = abs_path.replace('\\', os.sep).split(os.sep)
        del_same_parents(abs_path, current_path)

        return ['..'] * len(current_path) + abs_path


    @staticmethod
    def abs_path_from_relative(relative_path):
        return os.path.abspath(os.sep.join(relative_path))


    @staticmethod
    def _append_abs_path(abs_path):
        if abs_path not in sys.path:
            sys.path.append(abs_path)


    @classmethod
    def _print_relative_paths(cls, relative_paths, header = 'relative_paths = ['):
        print(f'{header}{relative_paths[0]},')

        for path in relative_paths[1:-1]:
            print(f'{" " * len(header)}{path},')

        print(f'{" " * len(header)}{relative_paths[-1]}]')
