import mesa
import sys
import json
from Ecosistem import Ecosistem
import Agents
import pickle

JSON_NAME_CONFIG="config.json"

if len(sys.argv) > 1:
    with open(sys.argv[1]+JSON_NAME_CONFIG) as f:
        data = json.load(f)
    

prey_reward_dict = {"near_predator_negative":data["prey"]["miedo"],
                    "near_prey_negative":data["prey"]["ignorancia"],
                    "near_allies_negative":data["prey"]["independencia"],
                    "near_predator_positive_modifier":data["prey"]["cobardia"],
                    "near_prey_positive_modifier":data["prey"]["avaricia"],
                    "near_allies_positive_modifier":data["prey"]["colonialismo"],
                    "lowest_energy_modifier":data["prey"]["hambre"]}

predator_reward_dict = {"near_predator_negative":data["predator"]["miedo"],
                    "near_prey_negative":data["predator"]["ignorancia"],
                    "near_allies_negative":data["predator"]["independencia"],
                    "near_predator_positive_modifier":data["predator"]["cobardia"],
                    "near_prey_positive_modifier":data["predator"]["avaricia"],
                    "near_allies_positive_modifier":data["predator"]["colonialismo"],
                    "lowest_energy_modifier":data["predator"]["hambre"]}


prey_behaviour = Agents.IntelligentBehaviour(1, (data["ecosistem"]["size"], data["ecosistem"]["size"]), data["prey"]["exploration_rate"], data["prey"]["discount_factor"], data["prey"]["learning_rate"],prey_reward_dict)
predator_behaviour = Agents.IntelligentBehaviour(0, (data["ecosistem"]["size"], data["ecosistem"]["size"]), data["predator"]["exploration_rate"], data["predator"]["discount_factor"], data["predator"]["learning_rate"],predator_reward_dict)
grass_behaviour = Agents.DumbBehaviour()

basic_predator_agent = Agents.Agent(None, None, predator_behaviour, [prey_behaviour], [], (1,0), "red","lobo.png", data["predator"]["energia"],
                                     repro_min_energy= data["predator"]["energia_min_reproduccion"], repro_cost=data["predator"]["coste_reproduccion"],
                                     move_cost=data["predator"]["coste_movimiento"], eat_recover=data["predator"]["recuperacion_comer"])
basic_prey_agent = Agents.Agent(None, None, prey_behaviour, [grass_behaviour], [predator_behaviour], (1,0), "green", "conejo.png", data["prey"]["energia"],
                                     repro_min_energy= data["prey"]["energia_min_reproduccion"], repro_cost=data["prey"]["coste_reproduccion"],
                                     move_cost=data["prey"]["coste_movimiento"], eat_recover=data["prey"]["recuperacion_comer"])
basic_grass_agent =  Agents.Agent(None, None, grass_behaviour, [], [prey_behaviour], (1,0), "grey","cesped.png", 200, isBasic=True)

agent_dict = {
    prey_behaviour:{"amount":data["ecosistem"]["n_preys"], "basic_object":basic_prey_agent},
    predator_behaviour:{"amount":data["ecosistem"]["n_preds"], "basic_object":basic_predator_agent},
    grass_behaviour:{"amount":data["ecosistem"]["n_grass"], "basic_object":basic_grass_agent}
}

basic_food_info = {
    "agent":grass_behaviour,
    "regen":data["ecosistem"]["food_regen"],
    "cluster_prob":data["ecosistem"]["cluster_prob"]
}


############################# VISUALIZACIÓN CON EL SERVIDOR DE MESA#############################
# grid = mesa.visualization.CanvasGrid(agent_portrayal, SIZE, SIZE, 500, 500)
# server = mesa.visualization.ModularServer(
#     Ecosistem, [grid], "Ecosistem", {"agent_dict":agent_dict, "size": SIZE,"basic_food_info":basic_food_info}
# )
# server.port = 8525  # The default
# server.verbose = False
# server.launch()



## Supongo que la carpeta está creada
def guardar_modelo(modelo,ruta):
    file = open(ruta+"model.pickle", 'wb')
    pickle.dump(modelo,file)
    file.close()


############################ SERVIDOR PROPIO #########################
model = Ecosistem(agent_dict, data["ecosistem"]["size"], basic_food_info, verbose=True)
for i in range(data["ecosistem"]["iters"]):
    model.step()
guardar_modelo(model,sys.argv[1])

