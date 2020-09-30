from ..services.graph_service import GraphService
from fastapi import HTTPException
from typing import List

class GraphController():
    def __init__(self):
        self.graph_service = GraphService()
    
    def get_graph(self, top, bottom, right, left):
        try:
            return self.graph_service.get_graph(top, bottom, right, left)
        except Exception:
            raise HTTPException(status_code=404, detail=Exception)

    