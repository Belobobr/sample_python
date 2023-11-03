from config import get_config
from dependencies import provide_dependencies_graph
from server import create_application

config = get_config()
application_dependencies_graph = provide_dependencies_graph(config)
app = create_application(application_dependencies_graph)