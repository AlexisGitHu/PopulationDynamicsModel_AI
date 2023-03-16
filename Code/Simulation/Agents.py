import mesa
import random
import json

class Agent(mesa.Agent):
    def __init__(self, unique_id, model, specie, preys, predators, direction, color, sprite):
        super().__init__(unique_id, model)
        self.energy = 100
        self.specie = specie
        self.preys = preys
        self.predators = predators
        self.direction = direction
        self.color = color
        self.sprite = sprite

    def individual_cell_evaluation(self, x, y):
        content = self.model.grid.get_cell_list_contents([(x,y)])
        t = len(content)
        p = len([agent for agent in content if type(agent.specie) in self.preys])
        d = len([agent for agent in content if type(agent.specie) in self.predators])

        e = self.energy

        evaluation = (p*(1-e/100)**2-d(e/100)**2)/t




    def percieve(self):
        pass

    def get_vision(self):
        pass


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
        alive = True
        if self.energy > 0:
            self.specie.choice()
            self.move()
            self.eat()
            self.percieve()
            
        else:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            alive = False
        log = { "ID":self.unique_id,
                "Position":tuple(self.pos),
                "Direction": self.direction,
                "Sprite":self.sprite,
                "Alive":str(alive)}
        #print(json.dumps(log), end=", ")

class IntelligentAgentA():
    def choice(self):
        return random.randint(0,8)

class IntelligentAgentB():
    def choice(self):
        return random.randint(0,8)