import mesa
import Agents

class Ecosistem(mesa.Model):
    """A model with some number of agents."""
                                         
    def __init__(self, N, width, height):
        agentA = Agents. IntelligentAgentA()
        agentB = Agents. IntelligentAgentB()

        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.killed = []
        self.mating = []
        # Create agents
        for i in range(self.num_agents):
            if i%2==0:
                a = Agents. Agent(i, self, agentA, [Agents.IntelligentAgentB], "N","red")
            else:
                a = Agents. Agent(i, self, agentB, [], "N", "green")
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            
    

    def step(self):
        self.schedule.step()
        for x in self.killed:
            print(x.unique_id)
            try:
                self.grid.remove_agent(x)
                self.schedule.remove(x)
            except: 
                pass
        self.killed = []