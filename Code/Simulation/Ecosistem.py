import random
import mesa
import Agents
import numpy as np
import random

learning_rate = 0.05


class Ecosistem(mesa.Model):
    """A model with some number of agents."""
    learning_rate = 0.1

    def __init__(self, agent_dict, size, basic_food_info, verbose = False):
        # type_animal, grid, exploration_rate, discount_factor, learning_rate,s,q

        self.size = size
        self.verbose = verbose
        self.agent_collection = {}
        self.basic_food_info = basic_food_info
        self.grid = mesa.space.MultiGrid(size, size, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.killed = []
        self.mating = []
        self.reproduce = []
        self.next_agent_id = 0
        self.agent_dict=agent_dict
        self.agentList = []

        for agent in agent_dict:
            self.agent_collection[agent] = []
            for i in range(agent_dict[agent]["amount"]):
                self._copyAgent(agent_dict[agent]["basic_object"])

    def step(self):
        print('{"Step": ' + str(self.schedule.steps) + ', "info":[', end="")
        self.schedule.step()
        print("]}\n")

        for parent in self.reproduce:
            self._copyAgent(parent, pos = parent.pos)
        self.reproduce = []

        for dead_agent in self.killed:
            try:
                self.agent_collection[dead_agent.specie].remove(dead_agent)
                self.grid.remove_agent(dead_agent)
                self.schedule.remove(dead_agent)
            except:
                pass
        self.killed = []
        for agent in self.agent_dict:
            if len(self.agent_collection[agent])==0:
                for i in range(self.agent_dict[agent]["amount"]):
                    self._copyAgent(self.agent_dict[agent]["basic_object"])

        if not len(self.agent_collection[self.basic_food_info["agent"]])> 5:
            self._create_basic_food()
    
    def _copyAgent(self,agent, pos = None):
        new_agent = Agents.Agent(self.next_agent_id, self, agent.specie, agent.preys, agent.predators,
                                  agent.direction, agent.color, agent.sprite, agent.max_energy, isBasic = agent.isBasic)
        self.agent_collection[agent.specie].append(new_agent)
        self.schedule.add(new_agent)
        if not pos:
            pos = ( self.random.randrange(self.size), self.random.randrange(self.size) )
        self.grid.place_agent(new_agent, pos)
        self.next_agent_id += 1
        return new_agent
        
    # def createGrass(self):
    #     preyAgents = [x for x in self.agentList if x[2] == 1]
    #     grassAgents = [x for x in self.agentList if x[2] == 2]

    #     while grassAgents:
    #         randomGrass = random.choice(grassAgents)
    #         grassAgents.remove(randomGrass)

    #         neighbors = self.grid.get_neighborhood(randomGrass[1], False)

    #         while neighbors:
    #             cell = random.choice(neighbors)
    #             neighbors.remove(cell)
    #             if not self.grid.get_cell_list_contents(cell):
    #                 a = Agents.Agent(self.next_agent_id, self, self.grass_behaviour, [], [self.prey_behaviour], [],
    #                                     "grey", "cesped.png", 20, 2)
    #                 self.schedule.add(a)
    #                 self.grid.place_agent(a, cell)
    #                 self.agentList.append([self.next_agent_id, cell, 2])
    #                 self.next_agent_id += 1
    #                 return
                
    def _create_basic_food(self):
        for i in range(self.basic_food_info["regen"]):
            agent = random.choice(self.agent_collection[self.basic_food_info["agent"]])
            new_pos = None
            if random.random() < self.basic_food_info["cluster_prob"]:
                try:
                    new_pos = ((agent.pos[0]+random.randint(-1,1))%self.size,(agent.pos[1]+random.randint(-1,1))%self.size)  
                except:
                    pass
            self._copyAgent(agent, new_pos)
    
    def give_reward(self,agent):
        epsilon=0.1
        reward=0
        if not isinstance(agent.specie,Agents.DumbBehaviour):    
            coeff_modifier_near_enemy=0
            coeff_modifier_near_ally=0
            coeff_modifier_energy=0

            num_allies=0
            num_enemies=0
            num_grass=0

            cellmates=self.grid.get_cell_list_contents([agent.pos])
            prey_type=1
            predator_type=0
            num_total_species=[]
            for agents in self.agent_collection:
                num_total_species.append(len(self.agent_collection[agents]))
            
            num_allies = len([0 for agents in cellmates if agents == agent])
            num_enemies= len([0 for agents in cellmates if agents != agent])
            for num_specie in num_total_species:
                if num_specie==0:
                    num_specie=epsilon
            if agent.specie.type_animal==prey_type:
                if(num_enemies>0):
                    
                    coeff_modifier_near_enemy=-num_enemies/num_total_species[1]
                else:
                    coeff_modifier_near_enemy=1

                if(num_allies>0):
                    coeff_modifier_near_ally=num_allies/num_total_species[0] * 0.3
                else:
                    coeff_modifier_near_ally=-0.3
            elif agent.specie.type_animal==predator_type:
                if(num_enemies>0):
                    coeff_modifier_near_enemy=num_enemies/num_total_species[0]
                else:
                    coeff_modifier_near_enemy=-1
                if(num_allies>0):
                    coeff_modifier_near_ally=num_allies/num_total_species[1] * 0.3
                else:
                    coeff_modifier_near_ally=-0.3
            
            if(agent.energy < agent.max_energy):
                if(agent.energy< 20):
                    coeff_modifier_energy=-4*agent.energy/100
                else:
                    coeff_modifier_energy=-agent.energy/100
            else:
                coeff_modifier_energy=agent.energy/100
            reward = (coeff_modifier_near_ally+coeff_modifier_near_enemy+coeff_modifier_energy)/3
        return reward


    