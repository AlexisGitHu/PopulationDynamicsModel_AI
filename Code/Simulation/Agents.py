import mesa
import random

class Agent(mesa.Agent):
    def __init__(self, unique_id, model, specie, preys, direction, color):
        super().__init__(unique_id, model)
        self.energy = 100
        self.specie = specie
        self.preys = preys
        self.direction = direction
        self.color = color

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.energy -=1

    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        enemies = [agent for agent in cellmates if type(agent.specie) in self.preys]
        if len(enemies) > 1:
            other_agent = self.random.choice(enemies)
            self.model.killed.append(other_agent)
            self.energy = 100
    
    def reproduce(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        allies = [agent for agent in cellmates if agent.specie == self.specie]
        if len(allies) > 1 and self.energy > 50:
            other_agent = self.random.choice(allies)
            self.model.mating.append((self,other_agent))
            self.energy -= 50

    def step(self):
        if self.energy > 0:
            self.move()
            self.eat()
            # print("Hola")
            self.specie.choice()
        else:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

class IntelligentAgentA():
    def choice(self):
        return random.randint(0,4)

class IntelligentAgentB():
    def choice(self):
        return random.randint(0,4)