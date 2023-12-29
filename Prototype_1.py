import pygame
import random
import math

pygame.init()

GENES = ["up", "down", "right", "left"]
POPULATION_SIZE = 10
clock = pygame.time.Clock()
frame_counter = 0


def Choose_Random_Gene():
    return random.choice(GENES)


def Create_Seeker():
    return [Choose_Random_Gene() for _ in range(5)]


class Environment:
    def __init__(self):
        # Basic
        self.screen = pygame.display.set_mode((600, 600))
        self.run = True

        # Population
        self.population = []
        for _ in range(0, POPULATION_SIZE):
            gnome = Create_Seeker()
            self.population.append(Seeker(gnome))

        # Children
        self.children_population = []

    def draw(self):
        self.screen.fill((0, 0, 0))

        TREAT.draw(self.screen)

        for seeker in self.population:
            seeker.draw(self.screen)

        pygame.display.update()
        clock.tick(60)

    def gameloop(self):
        while self.run:
            # Quit Game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

            # Move
            for seeker in self.population:
                seeker.movement()
                seeker.fitness = seeker.Grade_Fitness()

            global frame_counter
            frame_counter += 1

            if frame_counter % 2 == 0:
                # Evolution
                self.children_population = []

                # Sort according to fitness
                self.population = sorted(self.population, key=lambda x: x.fitness)

                Fitness = [self.population[i].fitness for i in range(len(self.population))]
                print(Fitness)

                # Elitism
                # Get the index for top 10% of population, and pass it down directly
                s = int((10 * POPULATION_SIZE) / 100)
                self.children_population.extend(self.population[:s])

                # Mating using top 50%
                s = int((90 * POPULATION_SIZE) / 100)  # To keep same population size
                for _ in range(s):
                    parent1 = random.choice(self.population[:50])
                    parent2 = random.choice(self.population[:50])
                    child = parent1.Mating(parent2)
                    self.children_population.append(child)

                # Replace old population with new one
                self.population = self.children_population

            self.draw()


class Treat:
    def __init__(self):
        self.position = pygame.math.Vector2(random.randint(10, 590),
                                            random.randint(10, 590))
        self.hitbox = pygame.Rect(self.position.x, self.position.y, 10, 10)

    def draw(self, surface):
        pygame.draw.rect(surface, (238, 210, 2), self.hitbox)


class Seeker:
    def __init__(self, genes):
        # Basic
        self.position = pygame.math.Vector2(300, 300)
        self.genes = genes
        self.fitness = self.Grade_Fitness()
        self.hitbox = pygame.Rect(self.position.x, self.position.y, 10, 10)
        self.moved = False
        self.unique = random.randint(0, 1000)
        
        # Mating
        self.child_genes = []
        self.probability = random.random()

    def movement(self):
        if not self.moved:
            for move in self.genes:
                if move == "up":
                    self.position.y += 10
                if move == "down":
                    self.position.y -= 10
                if move == "left":
                    self.position.x -= 10
                if move == "right":
                    self.position.x += 10
        self.moved = True

    def draw(self, surface):
        self.hitbox = pygame.Rect(self.position.x, self.position.y, 10, 10)
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox)
        
    def Mating(self, MatePartnerGenes):
        for gene1, gene2 in zip(self.genes, MatePartnerGenes.genes):
            if self.probability < 0.45:
                self.child_genes.append(gene1)
                
            elif self.probability < 0.90:
                self.child_genes.append(gene2)
                
            else:
                self.child_genes.append(Choose_Random_Gene())
                
        # Add gene to increase genetic complexity (length of gene list)
        self.child_genes.append(Choose_Random_Gene())
        
        return Seeker(self.child_genes)
    
    def Grade_Fitness(self):
        Fitness = math.sqrt((self.position.x - TREAT.position.x)**2 +
                            (self.position.y - TREAT.position.y)**2)

        return Fitness


TREAT = Treat()

Environment = Environment()
Environment.gameloop()
