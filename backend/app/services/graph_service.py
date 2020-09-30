import osmnx as ox


class GraphService():

    def get_graph(self, top, bottom, right, left) -> dict:
        top = float(top)
        bottom = float(bottom)
        right = float(right)
        left = float(left)

        map_data = self.get_graph_from_ox(top, bottom, right, left)


        nodes = self.mount_nodes(map_data)
        edges = self.mount_edges(map_data)


        print(nodes, edges)

        return {
            "nodes": nodes,
            "edges": edges
        }

    def get_graph_from_ox(self, top, bottom, right, left):
        return ox.graph_from_bbox(top, bottom, right, left, retain_all=True)

    def mount_nodes(self, map_data):
        raw_nodes_list = list(map_data.nodes(data=True))

        filtered_nodes_list = [ self.clean_node_data(node) for node in raw_nodes_list ]

        return filtered_nodes_list


    def clean_node_data(self, node):
        return {
            "id": node[0],
            "x": node[1]['x'],
            "y": node[1]['y'],
        }

    def mount_edges(self, map_data):
        raw_edges_list = list(map_data.edges(data=True))

        filtered_edges_list = [ self.clean_edge_data(edge) for edge in raw_edges_list ]

        return filtered_edges_list

    def clean_edge_data(self, edge):
        return {
            "from": edge[0],
            "to": edge[1],
            "length": edge[2].get('length') or 0,
            "name": edge[2].get('name') or False,
            "ref": edge[2].get('ref') or False,
            "oneway": edge[2].get('oneway') or False,
        } 