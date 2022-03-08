import os

from sigma.sigma_studio.project.project_xml import get_ICs, trim_xml


project_xml_file_url = os.sep.join(['..', '..', '..', 'SigmaStudio projects', 'projects', 'demo', 'demo.xml'])
ic = get_ICs(project_xml_file_url)[0]

# ================================================
ba1 = ic.parameter_bytes
ba2 = ic.registers['Param'].bytes
print('ba2 == ba1', ba2 == ba1)

print(len(ic._parameters))
print(len(ic.parameters.items()))

for m in ic.modules.values():
    for p in m.parameters.values():
        print(m.name, '\t', p.short_name, '\t', p.parent.name, '\t\t', p.name)

print(ic.registers['Param'].bytes)

print(ic.df)

trim_xml(project_xml_file_url)
