try:
    from . import project_xml
    from .project_xml import ET, findall
except:
    import project_xml
    from project_xml import ET, findall



def get_ICs(file_name):
    with open(file_name, 'rt', encoding = 'utf8') as f:
        root = ET.parse(f).getroot()

    return tuple(IC(ic) for ic in findall(root, 'IC'))



class _Element(project_xml._Element):

    def __init__(self, element, parent):
        self._ele = element
        self.parent = parent


    def _get_attr(self, attr):
        return self._ele.get(attr)


    @property
    def pins(self):
        return {l.pin: l for l in self._links}


    @property
    def links(self):
        links = {l.id: {'in': [], 'out': []} for l in self._links}

        for l in self._links:
            links[l.id][l.direction].append((l.parent.name, l.parent.location))

        return links



class Link(_Element):

    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.pin = self._get_pin_name(self._get_attr('pin'))
        self.id = self._get_attr('link')
        self.direction = self._get_attr('dir')

        self._ele = None


    @staticmethod
    def _get_pin_name(name):
        return '_'.join(name.split('_')[1:-1])



class Cell(_Element):
    ATTRIBUTES = ['cell']


    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.name = self._get_attr('cell')
        self.location = self._get_location(self._get_attr('location'))
        self._links = tuple(Link(ele, self) for ele in self.findall('Link'))

        self._ele = None


    @staticmethod
    def _get_location(location):
        # location= '{X=1103, Y=49.83075} '
        return tuple(float(e.split('=')[-1]) for e in location.replace('{', '').replace('}', '').split(','))



class IC(_Element):

    def __init__(self, element, parent = None):
        super().__init__(element, parent)

        a = self.findall('Algorithm')
        c = Cell(a[0], self)
        self._cells = tuple(Cell(ele, self) for ele in self.findall('Algorithm'))
        self._links = tuple(link for cell in self._cells for link in cell._links)
        self._ele = None


    @property
    def cells(self):
        return {c.name: c for c in self._cells}


    @property
    def _nodes(self):
        return set(c.name for c in self._cells)


    @property
    def _positions(self):
        return {c.name: (c.location[0], -c.location[1]) for c in self._cells}


    @property
    def _edges(self):
        return tuple((out_ele[0], in_ele[0])
                     for l in self.links.values()
                     for in_ele in l['in']
                     for out_ele in l['out'])


    def draw_graph(self, node_size = 120, node_color = 'blue', node_alpha = 0.5,
                   label_font_size = 10, label_font_family = 'sans-serif',
                   edge_width = 2, edge_color = 'green', edge_alpha = 0.5, edge_arrowstyle = '->', edge_arrowsize = 10,
                   connectionstyle = 'arc3, rad=0.2'):
        import networkx as nx

        G = nx.MultiDiGraph()
        G.add_nodes_from(self._nodes)
        G.add_edges_from(self._edges)
        graph_pos = self._positions

        nx.draw_networkx_nodes(G, graph_pos, node_size = node_size, node_color = node_color, alpha = node_alpha)
        nx.draw_networkx_labels(G, graph_pos, font_size = label_font_size, font_family = label_font_family)
        nx.draw_networkx_edges(G, graph_pos, edgelist = self._edges, width = edge_width, edge_color = edge_color,
                               alpha = edge_alpha, arrowstyle = edge_arrowstyle, arrowsize = edge_arrowsize,
                               connectionstyle = connectionstyle)
