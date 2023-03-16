
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 21:18:38 2017
 
@author: andrea
"""
#For predator modified f3
#Changed the features in preceive 
#Removed log in reward
#Added exp in features 

from builtins import map

import numpy as np
from GrassAgent import Grass
 
class Prey :

        ptype = -1 #1 if predator, -1 for prey
        age = 0
        epsilon = 0.2
 
        def __init__(self, x_position, y_position, ID, lastMeal, father,
                    weights, learning_rate,discount_factor,compute_how_many_func,perceive_func,cells_evaluation_func):
 
            self.x_position = x_position
            self.y_position = y_position
            self.ID = ID
            self.lastMeal = lastMeal ##LastAte
            self.father = father ##Random
            self.reproduction_age = np.random.randint(3,18) ##Estático
            self.death_rate = np.random.rand() ##Estático
            self.reproduction_rate = np.random.rand()##Estático
            self.weights = weights ## Matriz de pesos inicial
            self.learning_rate = learning_rate ## Prueba y error - Probar a cambiar cuando instancies la clase
            self.discount_factor = discount_factor ## Prueba y error - Probar a cambiar instancies la clase
            self.hunger_minimum = np.random.randint(3,10)
            self.compute_how_many_func=compute_how_many_func
            self.perceive_func=perceive_func
            self.cells_evaluation_func=cells_evaluation_func
            self.perceive_features=[]
            self.relative_positions={0:(-1,1),1:(0,1),2:(1,1),3:(-1,0),4:(0,0),5:(1,0),6:(-1,-1),7:(0,-1),8:(1,-1)}
            self.q = 0
            self.s = 0
        
        def set_learning_rate(self,rate):
            self.learning_rate=rate
            return
        def set_discount_factor(self,factor):
            self.discount_factor=factor
            return      
        ## Visión del agente - Trabajo de Álvaro, maldito sea
        def compute_how_many(self,matrix):
            return self.compute_how_many_func(matrix)  

        def Change_Position(self, matrix):
            """
            Perform action (i.e. movement) of the agent depending on its evaluations
            """
            r = np.random.rand()

            if r < 1 - self.epsilon:
                wanted_score = np.max(np.array(self.perceive_features))
                x_move,y_move = self.relative_positions[self.perceive_features.index(wanted_score)]
                self.s = wanted_score
            else:
                x_move = (self.x_position + np.random.randint(-1, 2) )
                y_move = (self.y_position + np.random.randint(-1, 2) )
                self.s = np.dot(self.perceive_features, self.weights)
            new_position = np.array([x_move, y_move])
            return new_position

        def Change_Sight(self,matrix):
            r = np.random.rand()

            if r < 1 - self.epsilon:
                wanted_score = np.max(np.array(self.perceive_features))
                x_move,y_move = self.relative_positions[self.perceive_features.index(wanted_score)]
                self.s = wanted_score
            else:
                x_move = (self.x_position + np.random.randint(-1, 2) )
                y_move = (self.y_position + np.random.randint(-1, 2) )
                self.s = np.dot(self.perceive_features, self.weights)
            new_position = np.array([x_move, y_move])
            return new_position
        
        def make_choice(self,features):
            self.perceive_features=features
            new_position=self.Change_Position(features)
            new_sight=self.Change_Sight(features)
            return  new_position,new_sight ##devuelve posiciones relativas
         
        def Aging(self, i):
            self.age += 1
            self.epsilon = 1 / i
            if i <= 501:
                self.learning_rate = 0.05 - 0.0001 * (i - 1)
            else:
                self.learning_rate = 0
            self.lastMeal += 1
            return
 
#---------------------------Learning part-------------------------------#
        def Get_Reward(self,matrix): 
            """
            opponent :number of the other species type within the agent’s Moore
            neighborhood normalized by the number of total
             type is 1 for predator and −1 for prey
            same = {0, 1} for if the opponent is on the same location
            """
            type_animal = self.ptype
            how_many = self.compute_how_many(matrix)
            x = self.x_position
            y = self.y_position
            features = self.perceive_features
            feature_wanted = features[0]
            opponent = feature_wanted
            same = how_many[2][4]>0
            reward = opponent*type_animal + 2*same*type_animal
 
            return reward
        ## Este features es el ya cambiado en función de la visión, no el features sin modificar
        def Get_QFunction(self,features):
            weights = self.weights
 
            Q = 0
            for i in range(len(weights)):
                Q = Q + weights[i]*features[i]
 
            return Q
        ## No se puede variar la tabla Q del agente, tiene que ser la misma para no romper el algoritmo
        ## Pensar detenidamente...
        def Update_Weight(self, reward, matrix, Q_value):
            weights = self.weights
            learning_rate = self.learning_rate
            discount_factor = self.discount_factor
 
            #Compute the Q'-table:
            Q_prime = []
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    x_target = (self.x_position+i)%matrix.xDim
                    y_target = (self.y_position+j)%matrix.yDim
                    features = self.perceive(x_target,y_target,matrix)
                    Q_prime.append(self.Get_QFunction(features))
 
            #Update the weights:
            Q_prime_max = max(Q_prime)
            for i in range(0,len(weights)):
                if i <3:
                    c = 9/(matrix.xDim*matrix.yDim)
                else:
                    c = 1/9
                    
                w = weights[i]
                f = features[i]
                f = np.exp(-0.5*(f-c)**2)
 
                weights[i] = w + learning_rate*(reward +discount_factor*Q_prime_max - Q_value)*f
 
            self.weights= weights
            return

        def Eat(self, agentListAtMatrixPos):
            for agent in agentListAtMatrixPos: #Not selected randomly at the moment, just eats the first prey in the list
                if type(agent) is Grass:
                    killFoodSource = agent.consume()
                    self.lastMeal = 0
                    if killFoodSource == 0:
                        return agent.ID
            return -1

        def Starve(self):
            if self.lastMeal > self.hunger_minimum:
                pdeath = self.lastMeal*self.death_rate
                r = np.random.rand()
                if r < pdeath:
                    return self.ID
            return -1

        def Reproduce(self):
            offspring = 0
            if self.age >= self.reproduction_age:
                r = np.random.rand()
                if r < self.reproduction_rate:
                    offspring = Prey(self.x_position, self.y_position, -1, 0, self.ID, self.reproduction_age,
                                     self.death_rate, self.reproduction_rate, self.weights, self.learning_rate,
                                     self.discount_factor, self.hunger_minimum) #ID is changed in Grid.update()
            return offspring

class Predator:
 
        ptype = 1 #1 if predator, -1 for prey
        age = 0
        epsilon = 0.2
 
        def __init__(self, x_position, y_position, ID, lastMeal, father,
                      weights, learning_rate,discount_factor, hunger_minimum,compute_how_many_func,perceive_func,cells_evaluation_func):
 
            self.x_position = x_position
            self.y_position = y_position
            self.ID = ID
            self.lastMeal = lastMeal ##LastAte
            self.father = father ##Random
            self.reproduction_age = np.random.randint(3,18) ##Estático
            self.death_rate = np.random.rand() ##Estático
            self.reproduction_rate = np.random.rand()##Estático
            self.weights = weights ## Matriz de pesos inicial
            self.learning_rate = learning_rate ## Prueba y error - Probar a cambiar cuando instancies la clase
            self.discount_factor = discount_factor ## Prueba y error - Probar a cambiar instancies la clase
            self.hunger_minimum = np.random.randint(3,10)
            self.compute_how_many_func=compute_how_many_func
            self.perceive_func=perceive_func
            self.cells_evaluation_func=cells_evaluation_func
            self.q = 0
            self.s = 0

        def compute_how_many(self,matrix):
            """
            Computes how many of what type of agent or objetct are in the nearby cells
            """
            return self.compute_how_many_func(matrix)    
 
        def perceive(self,x,y,matrix): 
            """
            Returns the features for a position (x,y) as a matrix decided by the method compute_how_many
            """
            return self.perceive_func(x,y,matrix)
           
 
        def Cells_Evaluation(self,matrix):
            """
            Evaluate the neighbooring cells
            """
            return self.cells_evaluation_func(matrix)
 
        def Change_Position(self, matrix):
            """
            Perform action (i.e. movement) of the agent depending on its evaluations
            """
            r = np.random.rand()

            if r < 1 - self.epsilon:
                wanted_score = np.max(np.array(self.perceive_features))
                x_move,y_move = self.relative_positions[self.perceive_features.index(wanted_score)]
                self.s = wanted_score
            else:
                x_move = (self.x_position + np.random.randint(-1, 2) )
                y_move = (self.y_position + np.random.randint(-1, 2) )
                self.s = np.dot(self.perceive_features, self.weights)
            new_position = np.array([x_move, y_move])
            return new_position

        def Change_Sight(self,matrix):
            r = np.random.rand()

            if r < 1 - self.epsilon:
                wanted_score = np.max(np.array(self.perceive_features))
                x_move,y_move = self.relative_positions[self.perceive_features.index(wanted_score)]
                self.s = wanted_score
            else:
                x_move = (self.x_position + np.random.randint(-1, 2) )
                y_move = (self.y_position + np.random.randint(-1, 2) )
                self.s = np.dot(self.perceive_features, self.weights)
            new_position = np.array([x_move, y_move])
            return new_position
        
        def make_choice(self,features):
            self.perceive_features=features
            new_position=self.Change_Position(features)
            new_sight=self.Change_Sight(features)
            return  new_position,new_sight
        
        def Aging(self, i):
 
            self.age +=1
            self.epsilon = 1/i
            if i <= 501:
                self.learning_rate = 0.05 - 0.0001*(i - 1)
            else:
                self.learning_rate = 0
            self.lastMeal +=1
 
            return
#---------------------------Learning part-------------------------------#
        def Get_Reward(self,matrix):
            """
            opponent :number of the other species type within the agent’s Moore
            neighborhood normalized by the number of total
            type is 1 for predator and −1 for prey
            same = {0, 1} for if the opponent is on the same location
            """
            type_animal = self.ptype
            how_many = self.compute_how_many(matrix)
            x = self.x_position
            y = self.y_position
            features = self.perceive(x,y,matrix)
            feature_wanted = features[0]
            opponent = feature_wanted
            same = how_many[1][4]>0
            reward = opponent*type_animal + 2*same*type_animal
            return reward
 
        def Get_QFunction(self,features):
            weights = self.weights
 
            Q = 0
            for i in range(len(weights)):
                Q = Q + weights[i]*features[i]
 
            return Q
 
        def Update_Weight(self, reward, matrix, Q_value):
            weights = self.weights
            learning_rate = self.learning_rate
            discount_factor = self.discount_factor
 
            #Compute the Q'-table:
            Q_prime = []
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    x_target = (self.x_position+i)%matrix.xDim
                    y_target = (self.y_position+j)%matrix.yDim
 
                    features = self.perceive(x_target,y_target,matrix)
                    Q_prime.append(self.Get_QFunction(features))
 
            #Update the weights:
            Q_prime_max = max(Q_prime)
            for i in range(0,len(weights)):
                if i<3:
                    c = 9/(matrix.xDim*matrix.yDim)
                else:
                    c=1/9
                    
                w = weights[i]
                f = features[i]
                f = np.exp(-0.5*(f-c)**2)
                weights[i] = w + learning_rate*(reward +discount_factor*Q_prime_max - Q_value)*f
 
            self.weights= weights
            return

        def Eat(self, agentListAtMatrixPos):
            for agent in agentListAtMatrixPos:
                if type(agent) is Prey: #Not selected randomly at the moment, just eats the first prey in the list
                    self.lastMeal = 0
                    return agent.ID
            return -1

        def Starve(self):
            if self.lastMeal > self.hunger_minimum:
                pdeath = self.lastMeal*self.death_rate
                r = np.random.rand()
                if r < pdeath:
                    return self.ID
            return -1

        def Reproduce(self):
            offspring = 0
            if self.age >= self.reproduction_age:
                r = np.random.rand()
                if r < self.reproduction_rate:
                    offspring = Predator(self.x_position, self.y_position, -1, 0, self.ID, self.reproduction_age,
                                            self.death_rate, self.reproduction_rate, self.weights, self.learning_rate,
                                            self.discount_factor, self.hunger_minimum) #ID is changed in Grid.update()
            return offspring
