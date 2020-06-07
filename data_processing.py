import os
import json
import matplotlib.pyplot as plt

#SET NUMBER OF TOURNAMENTS
number_of_tournaments = 10
peak_fitnesses = [0] * number_of_tournaments

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

plt.xlabel("number of tournaments")
plt.ylabel("peak_fitness")
plt.title("peak fitness over tournaments")
plt.plot(range(1, number_of_tournaments + 1), peak_fitnesses)
plt.show()



