import random
import mesa
import Agents
import numpy as np

learning_rate = 0.05


class Ecosistem(mesa.Model):
    """A model with some number of agents."""
    learning_rate = 0.05

    def __init__(self, N, width, height):
        # type_animal, grid, exploration_rate, discount_factor, learning_rate,s,q
        self.prey_behaviour = Agents.IntelligentBehaviour(-1, (width, height), 0.08, 1, learning_rate, 0, 0)
        self.predator_behaviour = Agents.IntelligentBehaviour(1, (width, height), 0.08, 1, learning_rate, 0, 0)
        self.grass_behaviour = Agents.DumbBehaviour(1, (width, height), 0.08, 1, learning_rate, 0, 0)

        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.killed = []
        self.mating = []
        self.reproduce = []
        self.agent_id = 0

        self.agentList = []

        # Create agents
        for i in range(self.num_agents):
            if i % 2 == 0:
                agent_type = 0
                a = Agents.Agent(self.agent_id, self, self.predator_behaviour, [self.prey_behaviour], [], "N", "red",
                                 "lobo.png", 100, agent_type)
            else:
                agent_type = 1
                a = Agents.Agent(self.agent_id, self, self.prey_behaviour, [], [self.predator_behaviour], "N", "green",
                                 "conejo.png", 100, agent_type)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.agentList.append([self.agent_id, (x, y), agent_type])
            a.direction = [x + 1, y]
            self.agent_id += 1

        for i in range(int(self.num_agents / 4)):
            a = Agents.Agent(self.agent_id, self, self.grass_behaviour, [], [self.prey_behaviour], [], "grey",
                             "cesped.png", 20, 2)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.agentList.append([self.agent_id, (x, y), 2])
            self.agent_id += 1

    def step(self):
        print('{"Step": ' + str(self.schedule.steps) + ', "info":[', end="")
        self.schedule.step()
        print("]}\n")

        self.createGrass()

        for x in self.reproduce:
            if x[0] == 0:
                a = Agents.Agent(self.agent_id, self, self.predator_behaviour, [self.prey_behaviour], [], [], "red",
                                 "lobo.png", 100, 0)
            else:
                a = Agents.Agent(self.agent_id, self, self.prey_behaviour, [self.grass_behaviour],
                                 [self.predator_behaviour], [], "green",
                                 "conejo.png", 100, 1)

            self.schedule.add(a)
            self.grid.place_agent(a, (x[1][0], x[1][1]))
            self.agentList.append([self.agent_id, (x[1][0], x[1][1]), x[0]])
            self.agent_id += 1

        self.reproduce = []

        for x in self.killed:
            try:
                self.grid.remove_agent(x)
                self.schedule.remove(x)
            except:
                pass
        self.killed = []

    def createGrass(self):
        preyAgents = [x for x in self.agentList if x[2] == 1]
        grassAgents = [x for x in self.agentList if x[2] == 2]

        if len(preyAgents) > len(grassAgents):
            while grassAgents:
                randomGrass = random.choice(grassAgents)
                grassAgents.remove(randomGrass)

                neighbors = self.grid.get_neighborhood(randomGrass[1], False)

                while neighbors:
                    cell = random.choice(neighbors)
                    neighbors.remove(cell)
                    if not self.grid.get_cell_list_contents(cell):
                        a = Agents.Agent(self.agent_id, self, self.grass_behaviour, [], [self.prey_behaviour], [],
                                         "grey", "cesped.png", 20, 2)
                        self.schedule.add(a)
                        self.grid.place_agent(a, cell)
                        self.agentList.append([self.agent_id, cell, 2])
                        self.agent_id += 1
                        return
