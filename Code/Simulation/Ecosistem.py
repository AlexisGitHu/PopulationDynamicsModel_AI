import mesa
import Agents
import numpy as np

learning_rate = 0.05

class Ecosistem(mesa.Model):
    """A model with some number of agents."""
    learning_rate = 0.05
    agentList= [] #list of agents. It will contain the id, position and agent type (0 = prey, 1= predator)
    def __init__(self, N, width, height):


       
    
        agentA = Agents.IntelligentAgentPrey()
        agentB = Agents.IntelligentAgentPredator()

        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.killed = []
        self.mating = []


        #initialize prey weight matrix to all zeros
        self.wmatrix_prey = [[0 for i in range(self.grid.height)] for j in range(self.grid.width)]
        self.wmatrix_predator = [[0 for i in range(self.grid.height)] for j in range(self.grid.width)]

        # Create agents
        for i in range(self.num_agents):
            if i % 2 == 0:
                a = Agents.Agent(i, self, agentA, [Agents.IntelligentAgentPredator], [], "N", "red", "lobo.png")
            else:
                a = Agents.Agent(i, self, agentB, [], [Agents.IntelligentAgentPrey], "N", "green", "conejo.png")
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        print(self.wmatrix_predator)
        print(self.wmatrix_prey)
        print('{"Step": ' + str(self.schedule.steps) + ', "info":[', end="")
        self.schedule.step()
        print("]}")
        for x in self.killed:
            try:
                self.grid.remove_agent(x)
                self.schedule.remove(x)
            except:
                pass
        self.killed = []