import mesa
from Ecosistem import Ecosistem
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": agent.color,
        "r": 1,
    }
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = mesa.visualization.ModularServer(
    Ecosistem, [grid], "Ecosistem", {"N": 100, "width": 10, "height": 10}
)
server.port = 8522  # The default
server.verbose = False
server.launch()

model = Ecosistem(3, 2, 2)
for i in range(70):
    # print("Hola")
    model.step()