from ..controllers.graph_controller import GraphController


class GraphRoute():
    def __init__(self):
        self.graph_controller = GraphController()

    def configure_routes(self, app):

        @app.get("/graph/")
        def get_graph(top, bottom, right, left):
            return self.graph_controller.get_graph(top, bottom, right, left)
