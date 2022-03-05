import os
import sys


try:
    from .sigma_studio.project.project_xml import get_ICs

except:
    from project_xml import get_ICs



class Factory:
    TEMP_PATH = 'temp'


    def __init__(self, project_xml_file_url = None, class_files_root_url = None, dsp = None):

        self.project_xml_file_url = project_xml_file_url
        self.class_files_root_url = class_files_root_url
        self.dsp = dsp

        if Factory.TEMP_PATH not in sys.path:
            sys.path.append(Factory.TEMP_PATH)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()


    def __del__(self):
        self._classes_dict = None
        self.dsp = None


    # XML related ==========================
    def get_ic(self, ic_idx = 0):
        assert self.project_xml_file_url is not None, \
            "Need 'project_xml_file_url': project's XML file."

        cls_numeric = self.dsp.DspNumber if self.dsp is not None else None

        return get_ICs(self.project_xml_file_url, cls_numeric = cls_numeric)[ic_idx]


    # Toolbox Cell related ==========================
    def get_cells(self, ic_idx = 0):

        ic = self.get_ic(ic_idx)
        cells = {}

        for module in ic.modules.values():
            cell_object = self._get_cell(module, self._classes_dict)
            cells[module.name] = cell_object

        return cells


    def get_cell_by_name(self, cell_name, ic_idx = 0):

        ic = self.get_ic(ic_idx)
        xml_module = ic.modules[cell_name]

        return self._get_cell(xml_module, self._classes_dict)


    def get_cells_manifest(self, ic_idx = 0):

        def trim(cell_name):
            return cell_name.lower().replace(' ', '_').replace('-', '_')


        return sorted([f"{trim(cell.name)} = cells['{cell.name}']  # {cell.description}"
                       for cell in self.get_cells(ic_idx).values()])


    def show_methods(self, ic_idx = 0, print_out = True):
        import json

        methods = {cell.name: json.loads(cell.show_methods(print_out = False))
                   for cell in self.get_cells(ic_idx).values()}

        json_str = json.dumps(methods, indent = 4, sort_keys = False)

        if print_out:
            print(json_str)
        else:
            return json_str


    @property
    def class_files_root_url(self):
        return self._class_files_root_url


    @class_files_root_url.setter
    def class_files_root_url(self, url):
        self._class_files_root_url = url

        if Factory.TEMP_PATH not in os.listdir():
            os.mkdir(Factory.TEMP_PATH)

        if url is not None:
            self._copy_files()

        self._classes_dict = self._get_classes_dict()


    def get_classes_df(self):
        import pandas as pd

        df = pd.DataFrame(self._get_classes_list(self._class_files_root_url or Factory.TEMP_PATH),
                          columns = ('class_name', 'file_name', 'path')).drop_duplicates()
        df.sort_values(by = ['class_name'], inplace = True)
        df.index = range(len(df))

        df_duplicated_classes = df[df['class_name'].duplicated(keep = False)]

        df_files = df.drop(columns = ['class_name']).drop_duplicates()
        df_duplicated_files = df_files[df_files['file_name'].duplicated(keep = False)]

        return df, df_duplicated_classes, df_duplicated_files


    # private functions ==================================

    def _get_cell(self, xml_module, classes_dict):  # module: project_xml.Module

        class_name = xml_module.algorithm_name
        py_module_name = classes_dict[class_name]['file_name'].replace('.py', '')

        cls = getattr(__import__(f'{py_module_name}'), class_name)
        cell_object = cls(module = xml_module, dsp = self.dsp)

        return cell_object


    @classmethod
    def _get_classes_dict(cls):
        classes = cls._get_classes_list(Factory.TEMP_PATH)

        return {class_name: {'file_name': file_name, 'path': path}
                for (class_name, file_name, path) in classes}


    @classmethod
    def _get_classes_list(cls, files_root_url):

        class_names = []

        for path in cls._get_all_files(files_root_url):
            file_name = path.split(os.sep)[-1]

            with open(path, 'tr') as f:
                for line in f.readlines():
                    class_name = cls._get_class_name(line)
                    if class_name is not None:
                        class_names.append((class_name, file_name, path))

        return class_names


    @staticmethod
    def _get_class_name(line):
        line = line.strip()

        if line.startswith('class '):
            line = line[len('class'):]
            end = line.find('(') or line.find(':')
            return line[:end].strip()


    def _copy_files(self):

        for _, file_name, path in self._get_classes_list(self._class_files_root_url):
            if file_name.endswith('.py'):
                self._copy_file(path, os.sep.join([Factory.TEMP_PATH, file_name]))


    @staticmethod
    def _copy_file(source_path, target_path):
        if source_path != target_path:
            with open(source_path, 'rt') as source:
                with open(target_path, 'wt') as target:
                    target.writelines(source.readlines())


    @classmethod
    def _get_all_files(cls, path):
        files_list = []

        for item in os.listdir(path):
            item_url = os.sep.join((path, item))

            if os.path.isdir(item_url):
                files_list.extend(cls._get_all_files(item_url))

            elif os.path.isfile(item_url) and item_url.lower().endswith('.py'):
                files_list.append(item_url)

        return files_list
