from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from .routes.graph_route import GraphRoute
from .config.Config import Config
from .config.debug import debug_configurations

config = Config().config
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GraphRoute().configure_routes(app)
#Routes().configure_routes(app)
#MovieRoutes().configure_routes(app)

debug_configurations()