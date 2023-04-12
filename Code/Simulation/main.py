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


grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = mesa.visualization.ModularServer(
    Ecosistem, [grid], "Ecosistem", {"N": 20, "width": 20, "height": 20}
)
server.port = 8524  # The default
server.verbose = False
server.launch()

# model = Ecosistem(4, 10, 10)
# for i in range(70):
#     # print("Hola")
#     model.step()
