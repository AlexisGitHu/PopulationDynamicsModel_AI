import mesa
from Ecosistem import Ecosistem
import Agents

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer":0,
        "text":", ener:" +str(agent.energy),
        "Color": agent.color,
        "r": 1,
    }
    return portrayal

SIZE = 13
LEARNING_RATE = 0.1
DISCOUNT_FACTOR=0.9
NUMBER_OF_PREYS = 5
NUMBER_OF_PREDATORS = 4
NUMBER_OF_GRASS = 15

BASIC_FOOD_REGEN = 1
BASIC_FOOD_CLUSTER_PROB = 0.85

prey_behaviour = Agents.IntelligentBehaviour(1, (SIZE, SIZE), 0.08, DISCOUNT_FACTOR, LEARNING_RATE, 0, 0)
predator_behaviour = Agents.IntelligentBehaviour(0, (SIZE, SIZE), 0.08, DISCOUNT_FACTOR, LEARNING_RATE, 0, 0)
grass_behaviour = Agents.DumbBehaviour()

basic_predator_agent = Agents.Agent(None, None, predator_behaviour, [prey_behaviour], [], "N", "red","lobo.png", 100)
basic_prey_agent = Agents.Agent(None, None, prey_behaviour, [grass_behaviour], [predator_behaviour], "N", "green", "conejo.png", 100)
basic_grass_agent =  Agents.Agent(None, None, grass_behaviour, [], [prey_behaviour], [], "grey","cesped.png", 200, isBasic=True)

agent_dict = {
    prey_behaviour:{"amount":NUMBER_OF_PREYS, "basic_object":basic_prey_agent},
    predator_behaviour:{"amount":NUMBER_OF_PREDATORS, "basic_object":basic_predator_agent},
    grass_behaviour:{"amount":NUMBER_OF_GRASS, "basic_object":basic_grass_agent}
}

basic_food_info = {
    "agent":grass_behaviour,
    "regen":BASIC_FOOD_REGEN,
    "cluster_prob":BASIC_FOOD_CLUSTER_PROB
}


############################# VISUALIZACIÓN CON EL SERVIDOR DE MESA#############################
grid = mesa.visualization.CanvasGrid(agent_portrayal, SIZE, SIZE, 500, 500)
server = mesa.visualization.ModularServer(
    Ecosistem, [grid], "Ecosistem", {"agent_dict":agent_dict, "size": SIZE,"basic_food_info":basic_food_info}
)
server.port = 8525  # The default
server.verbose = False
server.launch()


############################ SERVIDOR PROPIO #########################
# model = Ecosistem(agent_dict, SIZE, basic_food_info, verbose=True)
# for i in range(70):
#     model.step()
