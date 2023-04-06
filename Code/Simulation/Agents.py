import mesa
import random
import json
import operator
import numpy as np


def get_vision(pos, dire, dist):
    fov = []
    dif = tuple(map(operator.sub, dire, pos))

    rev = dif[::-1]
    for i in range(dist):
        pos = tuple(map(operator.add, pos, dif))
        fov.append(pos)
        if dif[0] == 0 or dif[1] == 0:
            for j in range(1, i + 1):
                y = tuple([k * j for k in rev])
                fov.append(tuple(map(operator.sub, pos, y)))
                fov.append(tuple(map(operator.add, pos, y)))
        else:
            for j in reversed(range(1, i + 1)):
                fov.append((pos[0] - dif[0] * j, pos[1]))
                fov.append((pos[0], pos[1] - dif[1] * j))

    return fov


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
        self.pos_matriz_pesos = []
        # print("hollla")
        # print(type(self.specie))
        # print(self.specie)
        # try:
        #     if isinstance(self.specie, IntelligentAgentPrey):
        #         self.intelligence = IntelligentAgentPrey
        #     if isinstance(self.specie, IntelligentAgentPredator):
        #         self.intelligence = IntelligentAgentPredator
        # except Exception as e:
        #     print(e)
        #     print("neither prey nor predator")

    def individual_cell_evaluation(self, x, y):
        content = self.model.grid.get_cell_list_contents((x, y))
        try:
            t = len(content)
            p = len([agent for agent in content if type(agent.specie) in self.preys])
            d = len([agent for agent in content if type(agent.specie) in self.predators])

            e = self.energy
            evaluation = (p * (1 - e / 100) ** 2 - d*(e / 100) ** 2) / t

        except ZeroDivisionError as zd:
            evaluation = 0

        return evaluation

    def perceive(self):
        cells_number = 9
        features = []
        relative_positions = {0: (-1, 1), 1: (0, 1), 2: (1, 1), 3: (-1, 0), 4: (0, 0), 5: (1, 0), 6: (-1, -1),
                              7: (0, -1), 8: (1, -1)}
        for i in range(cells_number):
            pos_to_evaluate = tuple(map(operator.add, self.pos, relative_positions[i]))
            pos_to_evaluate = map(lambda x: x%10, pos_to_evaluate)
            features.append(self.individual_cell_evaluation(*pos_to_evaluate))
        return features  
    
    def convert_list_weights(self, bool, weight_matrix):
        cells_number = 9
        lista_pos = []
        lista_weights = []
        relative_positions = {0: (-1, 1), 1: (0, 1), 2: (1, 1), 3: (-1, 0), 4: (0, 0), 5: (1, 0), 6: (-1, -1),
                              7: (0, -1), 8: (1, -1)}
        for i in range(cells_number):
            pos_to_evaluate = tuple(map(operator.add, self.pos, relative_positions[i]))
            pos_to_evaluate = map(lambda x: x%10, pos_to_evaluate)
            lista_pos.append(list(pos_to_evaluate))
        self.pos_matriz_pesos = lista_pos

        for i,j in lista_pos:
            lista_weights.append(weight_matrix[i][j])
    
        return lista_weights

    def move(self):

        isPrey = False #False means it is Predator
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        #new_position = self.random.choice(possible_steps)
        #self.model.grid.move_agent(self, new_position)
        features = self.perceive()

        smart_choice = self.specie.make_choice(features, self.pos)
        new_position = smart_choice[0]
        new_sight = smart_choice[1]
        #update weights
        r = self.specie.Get_Reward(features)
        
        if(isinstance(self.specie,IntelligentAgentPrey)):
            isPrey = True
            list_weights = self.convert_list_weights(True, self.model.wmatrix_prey)
            new_list_weights = self.specie.Update_Weight(r, list_weights, self.model.grid.height, self.model.grid.width)
        else:
            isPrey = False
            list_weights = self.convert_list_weights(False,self.model.wmatrix_predator)
            new_list_weights = self.specie.Update_Weight(r, list_weights, self.model.grid.height, self.model.grid.width)

        self.energy -= 1
        self.model.grid.move_agent(self,new_position)
        
        return new_list_weights, isPrey


    def eat(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        enemies = [agent for agent in cellmates if type(agent.specie) in self.preys]
        if len(enemies) >= 1:
            other_agent = self.random.choice(enemies)
            self.model.killed.append(other_agent)
            self.energy = 100

    # TODO
    def reproduce(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        allies = [agent for agent in cellmates if agent.specie == self.specie]
        if len(allies) > 1 and self.energy > 50:
            other_agent = self.random.choice(allies)
            self.model.mating.append((self, other_agent))
            self.energy -= 50

    def step(self):
        alive = True
        contador = 0
        if self.energy > 0:
            # self.specie.choice()
            weights, isPrey= self.move() #aqui se esta devolviendo la matriz de subpesos.
            self.eat()
            self.perceive()
            if (isPrey):
                for i,j in self.pos_matriz_pesos:
                    self.model.wmatrix_prey[i][j] = weights[contador]
                    contador +=1

            else:
                for i,j in self.pos_matriz_pesos:
                    self.model.wmatrix_predator[i][j] = weights[contador]
                    contador +=1
        else:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            alive = False

        log = {"ID": int(self.unique_id),
               "Position": tuple(self.pos),
               "Direction": self.direction,
               "Sprite": self.sprite,
               "Alive": str(alive)}
        print(json.dumps(log), end=", ")


class IntelligentAgentPrey():
    '''
    This class contains the intelligence of the Prey Agent. It has methods that will make the Prey to do what we consider a smart choice.
    '''
    epsilon = 0.8
    perceive_features = []
    s = 0
    q = 0
    discount_factor = 1 #try and error to find out best value
    learning_rate = 0.05
    relative_positions = {0: (-1, 1), 1: (0, 1), 2: (1, 1), 3: (-1, 0), 4: (0, 0), 5: (1, 0), 6: (-1, -1),
                              7: (0, -1), 8: (1, -1)}

    def choice(self):
        return random.randint(0, 8)
    
    def Change_Position(self, x_position, y_position):
        '''
        This method returns the new position the new Prey's position.
        return class: numpy.ndarray
        '''
        r = np.random.rand()

        if r < 1 - self.epsilon:
            wanted_score = int(np.max(np.array(self.perceive_features)))
            x_move,y_move = self.relative_positions[self.perceive_features.index(wanted_score)]
            self.s = wanted_score
        else:
            x_move = (x_position + np.random.randint(-1, 2) )
            y_move = (y_position + np.random.randint(-1, 2) )
            #self.s = np.dot(self.perceive_features, self.weights)
        new_position = (x_move, y_move)
        print(type(new_position))
        return new_position
    
    
    def Change_Sight(self, x_position, y_position):
        '''
        This method returns the new Prey's sight direction.
        return class: numpy.ndarray
        '''

        r = np.random.rand()
        if r < 1 - self.epsilon:
            wanted_score = int(np.max(np.array(self.perceive_features)))
            x_move,y_move = self.relative_positions[self.perceive_features.index(wanted_score)]
            self.s = wanted_score
        else:
            x_move = (x_position + np.random.randint(-1, 2) )
            y_move = (y_position + np.random.randint(-1, 2) )
            #self.s = np.dot(self.perceive_features, self.weights)
        new_position = (x_move, y_move)
        return new_position
    
    def make_choice(self,features, pos):
        '''
        This method calls the two methods above, to obtain Prey's sight, and Prey's next move. It returns both things
        return class: tuple of numpy.ndarray
        '''     
        self.perceive_features=features
        new_position=self.Change_Position(*pos)
        new_sight=self.Change_Sight(*pos)
        return  new_position,new_sight
    
    def Get_Reward(self,features): 
        """
        opponent :number of the other species type within the agent’s Moore
        neighborhood normalized by the number of total
            type is 1 for predator and −1 for prey
        same = {0, 1} for if the opponent is on the same location
        """
        type_animal = 1 #because it is a prey
        #how_many = self.compute_how_many(matrix)
        features = self.perceive_features
        feature_wanted = features[0]
        opponent = feature_wanted
        #same = how_many[2][4]>0
        reward = opponent*type_animal + 2*type_animal

        return reward
    
    
    def Update_Weight(self, reward, list_weights, height, width):

        #con la coordenadas que voy a pasarle, necesito coger la submatriz de self.weights
        #hacer producto escalar entre features y self.weights.
        learning_rate = self.learning_rate
        discount_factor = self.discount_factor
        

        #Compute the Q'-table:
        Q_prime = []

        features = self.perceive_features
        Q_prime.append(self.Get_QFunction(features, list_weights))

        #Update the weights:
        Q_prime_max = max(Q_prime)
        for i in range(0,len(list_weights)):
            if i <3:
                c = 9/(height*width)
            else:
                c = 1/9
                
            w = list_weights[i]
            f = features[i]
            f = np.exp(-0.5*(f-c)**2)

            list_weights[i] = w + learning_rate*(reward +discount_factor*Q_prime_max - self.q)*f
 

        return list_weights
    

    def Get_QFunction(self,features, weights):
       

        Q = 0
        for i in range(len(weights)):
            Q = Q + weights[i]*features[i]

        return Q

class IntelligentAgentPredator():

    '''
    This class contains de intelligence of the Predator Agent. It has methods that will make the Predator to do what we consider a smart choice.
    '''

    epsilon = 0.8
    perceive_features = []
    s = 0
    q = 0

    discount_factor = 1 #try and error to find out best value
    learning_rate = 0.05

    relative_positions = {0: (-1, 1), 1: (0, 1), 2: (1, 1), 3: (-1, 0), 4: (0, 0), 5: (1, 0), 6: (-1, -1),
                              7: (0, -1), 8: (1, -1)}


    def choice(self):
        return random.randint(0, 8)
    
    def Change_Position(self, x_position, y_position):
        '''
        This method returns the new position the new Predator's position.
        return class: numpy.ndarray
        '''

        r = np.random.rand()

        if r < 1 - self.epsilon:
            wanted_score = int(np.max(np.array(self.perceive_features)))
            x_move,y_move = self.relative_positions[self.perceive_features.index(wanted_score)]
            self.s = wanted_score
        else:
            x_move = (x_position + np.random.randint(-1, 2) )
            y_move = (y_position + np.random.randint(-1, 2) )
            #self.s = np.dot(self.perceive_features, self.weights)
        new_position = (x_move, y_move)
        print(type(new_position))
        return new_position
    
    
    def Change_Sight(self, x_position, y_position):
        '''
        This method returns the new Predator's sight direction.
        return class: numpy.ndarray
        '''

        r = np.random.rand()
        if r < 1 - self.epsilon:
            wanted_score = int(np.max(np.array(self.perceive_features)))
            x_move,y_move = self.relative_positions[self.perceive_features.index(wanted_score)]
            #self.s = wanted_score
        else:
            x_move = (x_position + np.random.randint(-1, 2) )
            y_move = (y_position + np.random.randint(-1, 2) )
            #self.s = np.dot(self.perceive_features, self.weights)
        new_position = (x_move, y_move)
        return new_position
    
    
    def make_choice(self,features, pos):
        '''
        This method calls the two methods above, to obtain Predator's sight, and Predator's next move. It returns both things
        return class: tuple of numpy.ndarray
        '''     
        self.perceive_features=features
        new_position=self.Change_Position(*pos)
        new_sight=self.Change_Sight(*pos)
  
        return  new_position,new_sight
    

    def Get_Reward(self,features): 
        """
        opponent :number of the other species type within the agent’s Moore
        neighborhood normalized by the number of total
            type is 1 for predator and −1 for prey
        same = {0, 1} for if the opponent is on the same location
        """
        type_animal = -1 #because it is a predator
        #how_many = self.compute_how_many(matrix)
        features = self.perceive_features
        feature_wanted = features[0]
        opponent = feature_wanted
        #same = how_many[2][4]>0
        reward = opponent*type_animal + 2*type_animal

        return reward
    

    def Update_Weight(self, reward, list_weights, height, width):

        #con la coordenadas que voy a pasarle, necesito coger la submatriz de self.weights
        #hacer producto escalar entre features y self.weights.
        learning_rate = self.learning_rate
        discount_factor = self.discount_factor
        

        #Compute the Q'-table:
        Q_prime = []

        features = self.perceive_features
        Q_prime.append(self.Get_QFunction(features, list_weights))

        #Update the weights:
        Q_prime_max = max(Q_prime)
        for i in range(0,len(list_weights)):
            if i <3:
                c = 9/(height*width)
            else:
                c = 1/9
                
            w = list_weights[i]
            f = features[i]
            f = np.exp(-0.5*(f-c)**2)

            list_weights[i] = w + learning_rate*(reward +discount_factor*Q_prime_max - self.q)*f
 

        return list_weights
    

    def Get_QFunction(self,features, weights):

        Q = 0
        for i in range(len(weights)):
            Q = Q + weights[i]*features[i]

        return Q

