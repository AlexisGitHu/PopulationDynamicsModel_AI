import random
import mesa
import Agents
import numpy as np

learning_rate = 0.05


class Ecosistem(mesa.Model):
    """A model with some number of agents."""
    learning_rate = 0.05

    def __init__(self, agent_dict, width, height):
        # type_animal, grid, exploration_rate, discount_factor, learning_rate,s,q
        

        self.agent_collection = {}
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.killed = []
        self.mating = []
        self.reproduce = []
        self.next_agent_id = 0

        self.agentList = []

        for agent in agent_dict:
            self.agent_collection[agent] = []
            for i in range(agent_dict[agent]["amount"]):
                a = self._copyAgent(agent_dict[agent]["basic_object"],self.next_agent_id)
                self.agent_collection[agent].append(a)
                self.schedule.add(a)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(a, (x, y))
                self.agentList.append([self.next_agent_id, (x, y), a.type]) 
                #a.direction = [x + 1, y]
                self.next_agent_id += 1

            

        # Create agents
        # for i in range(self.num_agents):
        #     if i % 2 == 0:
        #         agent_type = 0
        #         a = Agents.Agent(self.agent_id, self, self.predator_behaviour, [self.prey_behaviour], [], "N", "red",
        #                          "lobo.png", 100, agent_type)
        #     else:
        #         agent_type = 1
        #         a = Agents.Agent(self.agent_id, self, self.prey_behaviour, [self.grass_behaviour], [self.predator_behaviour], "N", "green",
        #                          "conejo.png", 100, agent_type)
        #     self.schedule.add(a)
        #     # Add the agent to a random grid cell
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x, y))
        #     self.agentList.append([self.agent_id, (x, y), agent_type])
        #     a.direction = [x + 1, y]
        #     self.agent_id += 1

        # for i in range(int(self.num_agents / 4)):
        #     a = Agents.Agent(self.agent_id, self, self.grass_behaviour, [], [self.prey_behaviour], [], "grey",
        #                      "cesped.png", 20, 2)
        #     self.schedule.add(a)
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x, y))
        #     self.agentList.append([self.agent_id, (x, y), 2])
        #     self.agent_id += 1

    def step(self):
        print('{"Step": ' + str(self.schedule.steps) + ', "info":[', end="")
        self.schedule.step()
        print("]}\n")

        self.createGrass()

        # for x in self.reproduce:
        #     if x[0] == 0:
        #         a = Agents.Agent(self.next_agent_id, self, self.predator_behaviour, [self.prey_behaviour], [], [], "red",
        #                          "lobo.png", 100, 0)
        #     else:
        #         a = Agents.Agent(self.next_agent_id, self, self.prey_behaviour, [self.grass_behaviour],
        #                          [self.predator_behaviour], [], "green",
        #                          "conejo.png", 100, 1)

        #     self.schedule.add(a)
        #     self.grid.place_agent(a, (x[1][0], x[1][1]))
        #     self.agentList.append([self.next_agent_id, (x[1][0], x[1][1]), x[0]])
        #     self.next_agent_id += 1

        # self.reproduce = []

        for x in self.killed:
            try:
                self.grid.remove_agent(x)
                self.schedule.remove(x)
            except:
                pass
        self.killed = []
    
    def _copyAgent(self,agent, new_id):
        new_agent = Agents.Agent(new_id, self, agent.specie, agent.preys, agent.predators,
                                  agent.direction, agent.color, agent.sprite, agent.energy, agent.type)
        return new_agent
        
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
                        a = Agents.Agent(self.next_agent_id, self, self.grass_behaviour, [], [self.prey_behaviour], [],
                                         "grey", "cesped.png", 20, 2)
                        self.schedule.add(a)
                        self.grid.place_agent(a, cell)
                        self.agentList.append([self.next_agent_id, cell, 2])
                        self.next_agent_id += 1
                        return
