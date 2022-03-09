import os


try:
    from . import ufactory

except:
    import ufactory



class Factory(ufactory.Factory):
    TEMP_PATH = 'temp'
    CLASSES_DICT_FILE = 'classes_dict.json'


    def __init__(self, project_xml_file_url = None, class_files_root_url = None, dsp = None):
        super().__init__(project_xml_file_url = project_xml_file_url, dsp = dsp)

        self.class_files_root_url = class_files_root_url


    # XML =====================================================

    def save_parameters_to_eeprom(self, ic = None):
        ic = self.get_ic() if ic is None else ic
        self.read_all_parameters(ic)  # refresh values
        self.dsp.control.save_parameters_to_eeprom(ic.parameter_bytes)


    def read_all_parameters(self, ic):
        if self.dsp is not None:
            for param in ic.parameters.values():
                ba = self.dsp.read_parameter(param)
                if ba is not None:
                    param.set_value(ba)


    # Toolbox Cell ============================================

    def show_methods(self, ic = None, print_out = True):
        import json

        ic = self.get_ic() if ic is None else ic
        methods = {cell.name: json.loads(cell.show_methods(print_out = False))
                   for cell in self.get_cells(ic).values()}

        json_str = json.dumps(methods, indent = 4, sort_keys = False)

        if print_out:
            print(json_str)
        else:
            return json_str


    # classes ==========================================

    @property
    def class_files_root_url(self):
        return self._class_files_root_url


    @class_files_root_url.setter
    def class_files_root_url(self, url):
        self._class_files_root_url = url

        if self.TEMP_PATH not in os.listdir():
            os.mkdir(self.TEMP_PATH)

        if url is not None:
            self._copy_classes_files()
            self._gen_classes_dict_json()


    def get_classes_df(self):

        import pandas as pd

        df = pd.DataFrame(self._get_classes_list(self._class_files_root_url or self.TEMP_PATH),
                          columns = ('class_name', 'file_name', 'path')).drop_duplicates()
        df.sort_values(by = ['class_name'], inplace = True)
        df.index = range(len(df))

        df_duplicated_classes = df[df['class_name'].duplicated(keep = False)]

        df_files = df.drop(columns = ['class_name']).drop_duplicates()
        df_duplicated_files = df_files[df_files['file_name'].duplicated(keep = False)]

        return df, df_duplicated_classes, df_duplicated_files


    # private functions ==================================

    # classes =================================

    @classmethod
    def _gen_classes_dict_json(cls):
        import json

        json_str = json.dumps(cls._gen_classes_dict(), indent = 4, sort_keys = False)

        with open(os.sep.join([cls.TEMP_PATH, cls.CLASSES_DICT_FILE]), 'wt') as f:
            f.write(json_str)

        return json_str


    @classmethod
    def _gen_classes_dict(cls):
        classes = cls._get_classes_list(cls.TEMP_PATH)
        classes_dict = {class_name: file_name.replace('.py', '') for (class_name, file_name, _) in classes}

        # return cls._class_file_to_file_classes(classes_dict)
        return classes_dict


    @staticmethod
    def _class_file_to_file_classes(classes_dict):
        file_classes = {file_name: [] for file_name in set(classes_dict.values())}

        for class_name, file_name in classes_dict.items():
            file_classes[file_name].append(class_name)

        return file_classes


    @classmethod
    def _get_classes_list(cls, files_root_url):

        classes = []

        for path in cls._get_all_files(files_root_url):
            file_name = path.split(os.sep)[-1]

            with open(path, 'tr') as f:
                for line in f.readlines():
                    class_name = cls._get_class_name(line)
                    if class_name is not None:
                        classes.append((class_name, file_name, path))

        return classes


    @staticmethod
    def _get_class_name(line):
        line = line.strip()

        if line.startswith('class '):
            line = line[len('class'):]
            end = line.find('(') or line.find(':')
            return line[:end].strip()


    # files =================================

    def _copy_classes_files(self):

        for _, file_name, path in self._get_classes_list(self._class_files_root_url):
            if file_name.endswith('.py'):
                self._copy_file(path, os.sep.join([self.TEMP_PATH, file_name]))


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
