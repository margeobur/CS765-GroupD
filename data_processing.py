import os
import json
import matplotlib.pyplot as plt
import statistics

#SET NUMBER OF TOURNAMENTS
number_of_tournaments = 10
peak_fitnesses = [0] * number_of_tournaments
mean_robot_fitnesses = [0] * number_of_tournaments
mean_environment_fitnesses = [0] * number_of_tournaments
peak_population_robot_fitnesses = [0] * number_of_tournaments
peak_population_environment_fitnesses = [0] * number_of_tournaments

for filename in os.listdir("Data"):
    path = os.path.join("Data", filename)
    with open(path, "r") as json_file:
        data = json.load(json_file)

    if "population_data" in filename:
        environment_genomes = data["environment_genomes"]
        robot_genomes = data["robot_genomes"]

    elif "tournament_data" in filename:
        tournament = data["tournament"]
        peak_fitness = data["peak_fitness"]
        winner_genome = data["winner_genome"]
        loser_genome = data["loser_genome"]
        robot_fitnesses = data["robot_fitnesses"]
        environment_fitnesses = data["environment_fitnesses"]

        peak_fitnesses[tournament - 1] = peak_fitness
        mean_robot_fitness = statistics.mean(robot_fitnesses)
        mean_environment_fitness = statistics.mean(environment_fitnesses)
        mean_robot_fitnesses[tournament - 1] = mean_robot_fitness
        mean_environment_fitnesses[tournament - 1] = mean_environment_fitness
        peak_population_robot_fitnesses[tournament - 1] = max(robot_fitnesses)
        peak_population_environment_fitnesses[tournament - 1] = max(environment_fitnesses)


#graph peak fitness over tournaments
plt.figure(0)
plt.xlabel("number of tournaments")
plt.ylabel("peak_fitness")
plt.title("peak fitness over tournaments")
plt.plot(range(1, number_of_tournaments + 1), peak_fitnesses)
plt.savefig("Graphs/peak_fitness_over_tournaments.png")

#graph robot fitnesses for each tournament
plt.figure(1)
plt.xlabel("mean robot fitness for the population")
plt.ylabel("tournament")
plt.title("mean robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), mean_robot_fitnesses)
plt.savefig("Graphs/mean_robot_fitness.png")

#graph of peak robot fitness for the population for each tournament
plt.figure(2)
plt.xlabel("peak robot fitness for the population")
plt.ylabel("tournament")
plt.title("peak robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), peak_population_robot_fitnesses)
plt.savefig("Graphs/peak_robot_fitness_for_population.png")

#graph of peak environment fitness for the population fitness for each tournament
plt.figure(3)
plt.xlabel("peak robot fitness for the population")
plt.ylabel("tournament")
plt.title("peak robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), peak_population_environment_fitnesses)
plt.savefig("Graphs/peak_environment_fitness_for_population.png")

#graph of mean environment fitness for each tournament
plt.figure(4)
plt.xlabel("peak environment fitness")
plt.ylabel("tournament")
plt.title("mean environment fitness for each tournament")
plt.plot(range(1, number_of_tournaments + 1), mean_environment_fitnesses)
plt.savefig("Graphs/mean_environment_fitness_for_each_tournament.png")




