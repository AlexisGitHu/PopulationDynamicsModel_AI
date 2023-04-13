import mesa
from Ecosistem import Ecosistem
import Agents

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": agent.color,
        "r": 1,
    }
    return portrayal

WIDTH = 20
HEIGHT=20
LEARNING_RATE = 0.05

NUMBER_OF_PREYS = 5
NUMBER_OF_PREDATORS = 5
NUMBER_OF_GRASS = 5

prey_behaviour = Agents.IntelligentBehaviour(1, (WIDTH, HEIGHT), 0.08, 1, LEARNING_RATE, 0, 0)
predator_behaviour = Agents.IntelligentBehaviour(0, (WIDTH, HEIGHT), 0.08, 1, LEARNING_RATE, 0, 0)
grass_behaviour = Agents.DumbBehaviour()

basic_predator_agent = Agents.Agent(None, None, predator_behaviour, [prey_behaviour], [], "N", "red","lobo.png", 100, 0)
basic_prey_agent = Agents.Agent(None, None, prey_behaviour, [grass_behaviour], [predator_behaviour], "N", "green", "conejo.png", 100, 1)
basic_grass_agent =  Agents.Agent(None, None, grass_behaviour, [], [prey_behaviour], [], "grey","cesped.png", 20, 2)

agent_dict = {
    prey_behaviour:{"amount":NUMBER_OF_PREYS, "basic_object":basic_prey_agent},
    predator_behaviour:{"amount":NUMBER_OF_PREDATORS, "basic_object":basic_predator_agent},
    grass_behaviour:{"amount":NUMBER_OF_GRASS, "basic_object":basic_grass_agent}
}

grid = mesa.visualization.CanvasGrid(agent_portrayal, WIDTH, HEIGHT, 500, 500)
server = mesa.visualization.ModularServer(
    Ecosistem, [grid], "Ecosistem", {"agent_dict":agent_dict, "width": WIDTH, "height": HEIGHT}
)
server.port = 8524  # The default
server.verbose = False
server.launch()

# model = Ecosistem(agent_dict, WIDTH, HEIGHT)
# for i in range(70):
#     model.step()
