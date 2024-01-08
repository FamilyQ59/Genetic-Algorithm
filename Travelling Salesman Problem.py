# OBJETIVE
# The Traveling Salesman Problem (TSP) involves finding the shortest possible route that visits a set of
# given cities exactly once and returns to the original city.

import random

# Format for the cities and the distances between each one
Distances = {
    "AB": 4, "AD": 6, "AC": 2, "AE": 3, "AG": 8, "AF": 7, "AH": 5, "AI": 6, "AJ": 9,
    "BA": 4, "BC": 5, "BD": 2, "BE": 5, "BF": 9, "BG": 4, "BH": 3, "BI": 5, "BJ": 7,
    "CA": 2, "CB": 5, "CD": 6, "CE": 2, "CF": 6, "CG": 3, "CH": 4, "CI": 7, "CJ": 4,
    "DA": 6, "DB": 2, "DC": 6, "DE": 4, "DF": 5, "DG": 4, "DH": 2, "DI": 8, "DJ": 3,
    "EA": 3, "EB": 5, "EC": 2, "ED": 4, "EF": 8, "EG": 6, "EH": 7, "EI": 4, "EJ": 5,
    "FA": 7, "FB": 9, "FC": 6, "FD": 5, "FE": 8, "FG": 3, "FH": 6, "FI": 3, "FJ": 7,
    "GA": 8, "GB": 4, "GC": 3, "GD": 4, "GE": 6, "GF": 3, "GH": 5, "GI": 6, "GJ": 4,
    "HA": 5, "HB": 3, "HC": 4, "HD": 2, "HE": 7, "HF": 6, "HG": 5, "HI": 2, "HJ": 3,
    "IA": 6, "IB": 5, "IC": 7, "ID": 8, "IE": 4, "IF": 3, "IG": 6, "IH": 2, "IJ": 4,
    "JA": 9, "JB": 7, "JC": 4, "JD": 3, "JE": 5, "JF": 7, "JG": 4, "JH": 3, "JI": 4,
}

Population_Size = 100
Genes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def Create_Traveller():
    # Create a list with a random order of the cities
    Chromosome = Genes.copy()
    random.shuffle(Chromosome)
    return Chromosome


def Mutation(String):
    # Create a new list where two randomly chosen letters switch place
    ModifiedList = String.copy()
    character1 = random.randint(0, len(String) - 1)
    character2 = random.randint(0, len(String) - 1)
    ModifiedList[character1], ModifiedList[character2] = ModifiedList[character2], ModifiedList[character1]

    return ModifiedList


# Individual
class Traveller:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = self.cal_fitness()

    def cal_fitness(self):
        # Checks which order of cities the Traveller visits according to the self.genes list. Sums all the values, and
        # returns a fitness score

        fitness = 0

        for i in range(len(self.genes)):
            if i != len(self.genes) - 1:
                ChosenRoute = self.genes[i] + self.genes[i + 1]
                fitness += Distances[ChosenRoute]

            elif i == len(self.genes) - 1:
                ChosenRoute = self.genes[i] + self.genes[0]
                fitness += Distances[ChosenRoute]

        return fitness


def main():
    global Population_Size

    generation = 1

    found = False
    population = []

    # Create initial Population
    for _ in range(Population_Size):
        TravellerGenes = Create_Traveller()
        population.append(Traveller(TravellerGenes))

    while not found:  # If answer is unknown, can be left running forever until most optimal value is found

        population = sorted(population, key=lambda x: x.fitness)  # Sort population according to fitness score

        # In case of knowing answer, write it here in order to break the loop once it´s reached
        if population[0].fitness == 28:
            found = True

        # Define variable for new generation
        new_generation = []

        # Elitism: pass to next generation the top 10%
        s = int((10 * Population_Size) / 100)
        new_generation.extend(population[:s])

        # Fills up the remaining 90%, choosing randomly from the top 50% and mutating them.
        s = int((90 * Population_Size) / 100)
        for _ in range(s):
            child_genes = Mutation(random.choice(population[:50]).genes)
            child = Traveller(child_genes)
            new_generation.append(child)

        # Replace old generation with new generation
        population = new_generation

        # Print Results
        print("Generation: {}\tString: {}\tFitness: {}".
              format(generation,
                     "".join(population[0].genes),
                     population[0].fitness))

        generation += 1

    # Print Final Results
    print("Generation: {}\tString: {}\tFitness: {}".
          format(generation,
                 "".join(population[0].genes),
                 population[0].fitness))


main()
