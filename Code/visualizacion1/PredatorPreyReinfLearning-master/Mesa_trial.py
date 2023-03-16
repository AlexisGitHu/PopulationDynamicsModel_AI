#!/usr/bin/env python
# coding: utf-8

# In[8]:


import mesa

class MoneyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, specie):
        super().__init__(unique_id, model)
        self.energy = 50
        self.specie = specie

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.energy -=1

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        enemies = [agent for agent in cellmates if agent.specie < self.specie]
        if len(enemies) > 1:
            other_agent = self.random.choice(enemies)
            self.model.killed.append(other_agent)
            self.energy = 50

    def step(self):
        if self.energy > 0:
            self.move()
            self.eat()


class MoneyModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.killed = []
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self, i%2)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()
        for x in self.killed:
            print(x)
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.killed.remove(x)





def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "red",
        "r": (agent.specie+0.5)/2,
    }
    return portrayal


#grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
#server = mesa.visualization.ModularServer(
#    MoneyModel, [grid], "Money Model", {"N": 10, "width": 10, "height": 10}
#)
#server.port = 8522  # The default
#server.launch()

model = MoneyModel(50, 10, 10)
for i in range(20):
    model.step()


