from ..services.graph_service import GraphService
from fastapi import HTTPException
from typing import List
import traceback

class GraphController():
    def __init__(self):
        self.graph_service = GraphService()
    
    def get_graph(self, top, bottom, right, left):
        try:
            return self.graph_service.get_graph(top, bottom, right, left)
        except Exception as e:
            print(traceback.print_exc())
            raise HTTPException(status_code=404, detail=Exception)

    