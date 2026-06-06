import random
import queue
import threading

from deap import base, creator, tools

import config
import cities

try:
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
except Exception:
    pass


def two_opt_mutate(individual, indpb=0.1):
    if random.random() < indpb:
        i, j = sorted(random.sample(range(len(individual)), 2))
        individual[i:j + 1] = individual[i:j + 1][::-1]
    return (individual,)


def eval_tour(individual, dist_matrix):
    n = len(individual)
    total = sum(
        dist_matrix[individual[i]][individual[(i + 1) % n]]
        for i in range(n)
    )
    return (total,)


class GAEngine:
    def __init__(self, city_names):
        self.city_names = city_names
        self.n = len(city_names)
        self.dist_matrix = cities.build_distance_matrix(city_names)
        self.result_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = None

        self.toolbox = base.Toolbox()
        self.toolbox.register(
            "indices", random.sample, range(self.n), self.n
        )
        self.toolbox.register(
            "individual", tools.initIterate,
            creator.Individual, self.toolbox.indices
        )
        self.toolbox.register(
            "population", tools.initRepeat, list, self.toolbox.individual
        )
        self.toolbox.register(
            "evaluate", eval_tour, dist_matrix=self.dist_matrix
        )
        self.toolbox.register("mate", tools.cxOrdered)
        self.toolbox.register("mutate", two_opt_mutate, indpb=0.15)
        self.toolbox.register(
            "select", tools.selTournament,
            tournsize=config.TOURNAMENT_SIZE
        )

    def start(self):
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run, daemon=True
        )
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)

    def _run(self):
        pop = self.toolbox.population(n=config.POP_SIZE)

        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        best_per_gen = []

        for gen in range(config.N_GENERATIONS):
            if self._stop_event.is_set():
                break

            offspring = self.toolbox.select(pop, len(pop))
            offspring = list(map(self.toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < config.CX_PROB:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < config.MUT_PROB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            invalid = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = list(map(self.toolbox.evaluate, invalid))
            for ind, fit in zip(invalid, fitnesses):
                ind.fitness.values = fit

            elites = tools.selBest(pop, config.ELITE_SIZE)
            offspring = tools.selBest(
                offspring, len(offspring) - config.ELITE_SIZE
            )
            pop[:] = offspring + list(map(self.toolbox.clone, elites))

            best_ind = tools.selBest(pop, 1)[0]
            best_dist = best_ind.fitness.values[0]
            best_per_gen.append(best_dist)

            if gen % config.UPDATE_EVERY == 0 or gen == config.N_GENERATIONS - 1:
                self.result_queue.put({
                    "gen": gen + 1,
                    "best_dist": best_dist,
                    "best_route": list(best_ind),
                    "history": list(best_per_gen),
                    "done": False,
                })

        best_ind = tools.selBest(pop, 1)[0]
        self.result_queue.put({
            "gen": config.N_GENERATIONS,
            "best_dist": best_ind.fitness.values[0],
            "best_route": list(best_ind),
            "history": best_per_gen,
            "done": True,
        })

    def get_initial_distance(self, city_names):
        n = len(city_names)
        return sum(
            self.dist_matrix[i][(i + 1) % n] for i in range(n)
        )
