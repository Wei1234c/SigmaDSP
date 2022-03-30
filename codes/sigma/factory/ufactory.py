import sys


try:
    from ..sigma_studio.project.project_xml import get_ICs

except:
    from project_xml import get_ICs



class Factory:
    TEMP_FOLDER = '.'
    CLASSES_DICT_FILE = 'classes_dict.json'


    def __init__(self, project_xml_file_url = None, dsp = None, temp_folder = None):
        self.project_xml_file_url = project_xml_file_url
        self.dsp = dsp
        self._temp_folder = self.TEMP_FOLDER if temp_folder is None else temp_folder

        self._classes_dict = None

        if self._temp_folder not in sys.path:
            sys.path.append(self._temp_folder)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()


    def __del__(self):
        self._classes_dict = None
        self.dsp = None


    # XML =====================================================
    def get_ic(self, ic_idx = 0):
        assert self.project_xml_file_url is not None, \
            "Need 'project_xml_file_url': project's XML file."

        cls_numeric = self.dsp.DspNumber if self.dsp is not None else None

        return get_ICs(self.project_xml_file_url, cls_numeric = cls_numeric)[ic_idx]


    # Toolbox Cell ============================================
    def get_cells(self, ic = None):

        ic = self.get_ic() if ic is None else ic
        cells = {}

        for module in ic.modules.values():
            cell_object = self._get_cell(module)
            cells[module.name] = cell_object

        return cells


    def get_cell_by_name(self, cell_name, ic = None):

        ic = self.get_ic() if ic is None else ic
        xml_module = ic.modules[cell_name]

        return self._get_cell(xml_module)


    def get_cells_manifest(self, ic = None):

        ic = self.get_ic() if ic is None else ic


        def trim(cell_name):
            return cell_name.lower().replace(' ', '_').replace('-', '_')


        return sorted([f"{trim(cell.name)} = cells['{cell.name}']  # {cell.description}"
                       for cell in self.get_cells(ic).values()])


    # classes ==========================================

    @property
    def classes_dict(self):
        if self._classes_dict is None:
            self.load_classes_dict()

        return self._classes_dict


    def load_classes_dict(self):
        import json

        classes_dict_file = '/'.join([self._temp_folder, self.CLASSES_DICT_FILE])

        try:
            with open(classes_dict_file, 'rt') as f:
                self._classes_dict = json.load(f)

        except FileNotFoundError as e:
            print('Needs to set "class_files_root_url"')
            raise e


    # private functions ==================================

    # Cell ========================================
    def _get_cell(self, xml_module):  # module: project_xml.Module

        class_name = xml_module.algorithm_name
        py_module_name = self._get_class_file_name(class_name)

        cls = getattr(__import__(f'{py_module_name}'), class_name)
        cell_object = cls(module = xml_module, dsp = self.dsp)

        return cell_object


    def _get_class_file_name(self, class_name):
        # for file_name, classes in self.classes_dict.items():
        #     if class_name in classes:
        #         return file_name

        return self.classes_dict[class_name].replace('.py', '')
