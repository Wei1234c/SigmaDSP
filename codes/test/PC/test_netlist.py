import os

from sigma.sigma_studio.project.netlist import get_ICs


project_xml_file_url = os.sep.join(['..', '..', '..', 'SigmaStudio projects', 'projects', 'demo', 'demo_NetList.xml'])
ic = get_ICs(project_xml_file_url)[0]
# print(ic)
# ================================================

# print(ic.pins)
print(ic.links)

import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10), dpi=80)

ic.draw_graph(node_size = 120, node_color = 'blue', node_alpha = 0.5,
              label_font_size = 10, label_font_family = 'sans-serif',
              edge_width = 2, edge_color = 'green', edge_alpha = 0.5, edge_arrowstyle = '->', edge_arrowsize = 10,
              connectionstyle = 'arc3, rad=0.2')

plt.show()