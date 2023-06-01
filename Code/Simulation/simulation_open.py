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
    

############################# VISUALIZACIÓN CON EL SERVIDOR DE MESA#############################
# grid = mesa.visualization.CanvasGrid(agent_portrayal, SIZE, SIZE, 500, 500)
# server = mesa.visualization.ModularServer(
#     Ecosistem, [grid], "Ecosistem", {"agent_dict":agent_dict, "size": SIZE,"basic_food_info":basic_food_info}
# )
# server.port = 8525  # The default
# server.verbose = False
# server.launch()
PICKLE_FILENAME="model.pickle"

def cargar_modelo(ruta):
    file=open(ruta+PICKLE_FILENAME,"rb")
    loaded_model=pickle.load(file)
    file.close()
    return loaded_model

## Supongo que la carpeta está creada
def guardar_modelo(modelo,ruta):
    file = open(ruta+PICKLE_FILENAME, 'wb')
    pickle.dump(modelo,file)
    file.close()


############################ SERVIDOR PROPIO #########################
model=cargar_modelo(sys.argv[1])
for i in range(data["ecosistem"]["iters"]):
    model.step()
guardar_modelo(model,sys.argv[1])

