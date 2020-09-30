from ..controllers.graph_controller import GraphController


class GraphRoute():
    def __init__(self):
        self.graph_controller = GraphController()

    def configure_routes(self, app):

        @app.get("/get/graph/{coordinates}")
        def get_graph(coordinates: str):
            """Coordinates must be "top/bottom/right/left" to work"""
            split = coordinates.split("/")
            top, bottom, right, left = split[0], split[1], split[2], split[3]
            
            return self.graph_controller.get_graph(top, bottom, right, left)
