import copy
import multiprocessing as pool
import os
import random


import matplotlib
import numpy as np
import pandas as pd
import scipy.spatial.distance
import matplotlib.pyplot as plt
import seaborn
# Loading Data
data_frame = pd.read_csv('PCA_Y_result_n2500.csv')
data_frame = data_frame.drop(data_frame.columns[0], axis=1)
data_matrix = data_frame.as_matrix()
# Genetic Parameters
crossover_probability = 0.8
mutation_probability = 0.05
chromosome_number = 50
number_of_crossover = 2 * round((crossover_probability * chromosome_number) / 2)
number_of_mutation = round(mutation_probability * chromosome_number)
Iteration_Number = 100
cluster_number = 20
# perssure
beta = 300


# Chromosome Definition

class chromosome:
    def __init__(self, cluster_number, data_matrix):
        self.cluster_number = cluster_number
        self.center = data_matrix.shape[1]
        self.data_matrix = data_matrix
        self.fitnessValue = 0
        rand = random.randrange(0, 1)
        if rand == 0:
            rand = -1
        self.chromosome_data = rand * np.random.rand(cluster_number, self.data_matrix.shape[1])

    def fittness(self):
        distance_matrix = scipy.spatial.distance.cdist(self.chromosome_data, self.data_matrix)
        minimum = np.min(distance_matrix, axis=0)
        self.fitnessValue = np.sum(minimum)
        return self.fitnessValue


# Cross over definition
def crossover_function(parent1, parent2, cluster_number):
    a = random.randrange(cluster_number)
    parent1.fittness()
    parent2.fittness()
    child1 = chromosome(cluster_number, data_matrix)
    child2 = chromosome(cluster_number, data_matrix)
    child1.chromosome_data[0:a] = parent1.chromosome_data[0:a]
    child1.chromosome_data[a:cluster_number] = parent2.chromosome_data[a:cluster_number]
    child2.chromosome_data[0:a] = parent2.chromosome_data[0:a]
    child2.chromosome_data[a:cluster_number] = parent1.chromosome_data[a:cluster_number]
    child1.fittness()
    child2.fittness()
    best_choice = [child1, child2, parent1, parent2]
    best_choice = sorted(best_choice, key=lambda x: x.fitnessValue)
    return [best_choice[0], best_choice[1]]


def mutation(mutate, allsample, cluster_number):
    all_mutation = np.array([mutate])
    for i in range(cluster_number):
        random_sample = random.randrange(chromosome_number)
        random_center = random.randrange(cluster_number)
        new_chromosome = copy.deepcopy(mutate)
        new_chromosome.chromosome_data[i] = allsample[random_sample].chromosome_data[random_center]
        new_chromosome.fittness()
        all_mutation = np.append(all_mutation, new_chromosome)
    best_choice = sorted(all_mutation, key=lambda x: x.fitnessValue)
    return best_choice[0]


def Boltzman(Costs):
    Costs.sort()
    worst_cost = Costs[Costs.size - 1]
    P = np.exp(-beta * Costs / worst_cost)
    P = P / np.sum(P)
    return P


def roulette_wheel_selection(P):
    rand = np.random.uniform()
    sum_all = np.cumsum(P)
    return np.where(rand <= sum_all)[0][0]


# Main Algorithm Loop

All_samples = np.array([chromosome(cluster_number, data_matrix) for _ in range(chromosome_number)])
best_answers = np.array([])
for i in range(0, Iteration_Number):
    Costs = np.array([])
    for j in range(chromosome_number):
        Costs = np.append(Costs, All_samples[j].fittness())
    # Cross Over
    P = Boltzman(Costs)
    Cross_over_sample = np.array([])
    for j in range(int(number_of_crossover / 2)):
        random_first_parent = roulette_wheel_selection(P)
        random_second_parent = roulette_wheel_selection(P)
        children = crossover_function(All_samples[random_first_parent], All_samples[random_second_parent],
                                      cluster_number)
        Cross_over_sample = np.append(Cross_over_sample, children)
    # print("Cross Over is Done")
    # Mutation
    Mutation_Sample = np.array([])
    for j in range(int(number_of_mutation)):
        random_mutation = roulette_wheel_selection(P)
        mutated = mutation(All_samples[random_mutation], All_samples, cluster_number)
        Mutation_Sample = np.append(Mutation_Sample, mutated)
    # print("Mutation is done")

    NewAllSamples = np.concatenate((All_samples, Cross_over_sample, Mutation_Sample), axis=0)
    NewAllSamples = sorted(NewAllSamples, key=lambda x: x.fitnessValue)
    All_samples = NewAllSamples[0:chromosome_number]
    best_answers = np.append(best_answers, All_samples[0].fitnessValue)
    # print("This is the iteration number:", i)
    # print("--------------------------")
final_result = pd.DataFrame(All_samples[0].chromosome_data)
plt.plot(range(Iteration_Number), best_answers)
plt.close()

