import mesa
import sys
import json
from Ecosistem import Ecosistem
import Agents

if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
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


prey_behaviour = Agents.IntelligentBehaviour(1, (data["size"], data["size"]), data["prey"]["exploration_rate"], data["prey"]["discount_factor"], data["prey"]["learning_rate"],prey_reward_dict)
predator_behaviour = Agents.IntelligentBehaviour(0, (data["size"], data["size"]), data["predator"]["exploration_rate"], data["predator"]["discount_factor"], data["predator"]["learning_rate"],predator_reward_dict)
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


############################ SERVIDOR PROPIO #########################
model = Ecosistem(agent_dict, data["size"], basic_food_info, verbose=True)
for i in range(data["iters"]):
    model.step()
