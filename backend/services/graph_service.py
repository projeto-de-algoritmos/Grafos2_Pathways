import osmnx as ox


class GraphService():

    def __init__(self):
        self.graph

    def get_graph(self, top, bottom, right, left):

        response = []
        self.graph = ox.graph_from_bbox(top, bottom, right, left, retain_all=True)
        nodes = list(self.graph.nodes(data=True))
        edges = list(self.graph.edges(data=True))
        response.append({
            nodes: nodes,
            edges: edges
        })

        return response

