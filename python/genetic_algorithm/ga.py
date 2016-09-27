'''
Created on 21 de set de 2016

@author: edielson
'''
import numpy as np

class genetic_algorithm(object):
    '''
    classdocs
    '''

    def __init__(self, problem):
        '''
        Constructor
        '''
        self.problem = problem
    
    def __mutation(self,individual):
        
        if self.__mutationTest():
            randomPosition = int(np.random.uniform(0,self.problem.getIndividualSize()-1))
            print('Mutation at position: %d' %randomPosition)
            #get a random value for changing in the individual position selected before
            randomValue = int(np.random.uniform(1,self.problem.getMaxSymbol()))
            print('New value: %d' %randomValue)
            
            individual[randomPosition]=randomValue
        return individual
    
    def __mutationTest(self):
        a=[0, 1]
        p=[0.90, 0.10]
        #Get the cumulative sum of the probabilities.
        cumSumP = np.cumsum(p)
        #Get our random numbers - one for each column.
        randomNumber = np.random.rand()
        #Get the values from A.
        #If the random number is less than the cumulative probability then
        #that's the number to use from A.
        for i, total in enumerate(cumSumP):
            if randomNumber < total:
                break
        test=a[i]
        if test == 1:
            print('Mutation!')
        return test
    
    def __bestFitness(self):
     
        pop_fit = self.problem.fitness(self.population)
#         print(pop_fit)
        best_fit=pop_fit[0]
        best_individual=0
        for i in range(1,len(pop_fit)):
            if(pop_fit[i] > best_fit):
                best_fit = pop_fit[i]    
                best_individual=i
         
        return best_fit,best_individual        

    
    def __crossover3(self,individual_x,individual_y):
        
        n=self.problem.getIndividualSize()
        
        c = np.random.uniform(1,n)
        d = np.random.uniform(1,n)    
        # concatenate the two fathers in the C element chosen randomly
        new_individual_x=[individual_x[1:c], individual_y[c+1:d], individual_x[d+1:n]]
        new_individual_y=[individual_y[1:c], individual_x[c+1:d], individual_y[d+1:n]]
        print("crossing point 1: %d" %c)
        print("crossing point 2: %d" %d)
        print("New individuals generated: %s and %s" %(new_individual_x,new_individual_y));
        
        return new_individual_x,new_individual_y
    
    def __crossover(self,individual_x,individual_y):
        
        
        n=self.problem.getIndividualSize()
        
        c = int(np.random.uniform(0,n-1))
        print("crossing point: %d" %c)
        
        new_individual_x=[]
        new_individual_y=[]
        
        # concatenate the two fathers in the C element chosen randomly
        for gene in range(c):
            new_individual_x.append(individual_x[gene])
            new_individual_y.append(individual_y[gene])
        for gene in range(c,n):    
            new_individual_x.append(individual_y[gene])
            new_individual_y.append(individual_x[gene])
        
        return new_individual_x,new_individual_y
    
    
    def __selection(self):
    
        sorted_population = sorted(self.population,key=self.problem.getFitness, reverse=True)        
        pop_fit = self.problem.fitness(sorted_population)
#         print(pop_fit)
        
        prob_fit = []
        for individual in pop_fit:
            prob_fit.append(1.0*individual/np.sum(pop_fit))
#         print(prob_fit)
        
        #Get the cumulative sum of the probabilities.
        cumSumP = np.cumsum(prob_fit)
        #Get our random numbers - one for each column.
        randomNumber = np.random.rand()
        #Get the values from A.
        #If the random number is less than the cumulative probability then
        #that's the number to use from A.
#         print(randomNumber)
#         print(cumSumP)
        for i, total in enumerate(cumSumP):
            if randomNumber < total:
                break
        self.population = sorted_population
        selected = self.population[i]
        #Display it. Uncomment for log.
        print("Selected individual %d = %s" %(i,selected))
        return selected
        
    def __newPopulation(self,population_size):
        
        new_population = []
        for i in range(0,population_size,2):
            #Selection
            x = self.__selection()
            y = self.__selection()
            
            #Crossover
            new_individual_x,new_individual_y = self.__crossover(x,y)
            
            #Mutation
            new_individual_x = self.__mutation(new_individual_x)
            new_individual_y = self.__mutation(new_individual_y)
            
            print('New individual x: %s'%new_individual_x)
            print('New individual y: %s'%new_individual_y)
            
            new_population.append(new_individual_x)
            new_population.append(new_individual_y)
        return new_population
    
    def search(self, population_size, max_generation, target):
        
        generation = 0
        fit_historical=[]
        
        self.population = self.problem.initPopulation(population_size)
        print(self.population)
        
        best_fit,best_individual = self.__bestFitness()
        
        print("Generation: %d" %generation)
        print("Population: %s" %self.population)
        print("Best fit: Individual %d = %d" %(best_individual,best_fit))
            
        while (best_fit < target) and (generation < max_generation):
            
            fit_historical.append(best_fit)
            
            generation=generation+1
    
            self.population=self.__newPopulation(population_size)      
            
            best_fit,best_individual = self.__bestFitness()
    
            print("\r\nGeneration: %d" %generation)
            print("Population: %s" %self.population)
            print("Best fit: Individual[%d] = %d" %(best_individual,best_fit))
        
        return fit_historical,generation    