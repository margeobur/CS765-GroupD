import os
import json
import matplotlib.pyplot as plt
import statistics
import re
import itertools


#SET NUMBER OF TOURNAMENTS
number_of_tournaments = 1400

#SET POPULATION NUM
num_pop = 30

peak_fitnesses = [0] * number_of_tournaments
mean_robot_fitnesses = [0] * number_of_tournaments
mean_environment_fitnesses = [0] * number_of_tournaments
peak_population_robot_fitnesses = [0] * number_of_tournaments
peak_population_environment_fitnesses = [0] * number_of_tournaments
total_thing_amount = [0] * number_of_tournaments
total_energy_amount = [0] * number_of_tournaments
total_trap_amount = [0] * number_of_tournaments
total_sensor_amount = [0] * number_of_tournaments

winner_num_of_water_genes = [0] * number_of_tournaments
loser_num_of_water_genes = [0] * number_of_tournaments
winner_num_of_trap_genes = [0] * number_of_tournaments
loser_num_of_trap_genes = [0] * number_of_tournaments
winner_num_of_food_genes = [0] * number_of_tournaments
loser_num_of_food_genes = [0] * number_of_tournaments
winner_num_of_sensors = [0] * number_of_tournaments
loser_num_of_sensors = [0] * number_of_tournaments

for filename in os.listdir("Data"):
    path = os.path.join("Data", filename)
    with open(path, "r") as json_file:
        try:
            data = json.load(json_file)
        except:
            break

    if "population_data" in filename:
        environment_genomes = data["environment_genomes"]
        robot_genomes = data["robot_genomes"]
        tournament = int(re.findall("(\\d+)\\.", filename)[0])
        if tournament < number_of_tournaments:
            total_thing_amount[tournament] = 0
            for _, environment in data["environment_genomes"].items():
                for thing in itertools.chain(environment["water_genes"], environment["food_genes"], environment["trap_genes"]):
                    total_thing_amount[tournament] += thing["amount"]
            total_thing_amount[tournament] /= len(data["environment_genomes"])

            total_energy_amount[tournament] = 0
            for _, environment in data["environment_genomes"].items():
                for thing in itertools.chain(environment["water_genes"], environment["food_genes"]):
                    total_energy_amount[tournament] += thing["amount"]
            total_energy_amount[tournament] /= len(data["environment_genomes"])

            total_trap_amount[tournament] = 0
            for _, environment in data["environment_genomes"].items():
                for thing in environment["trap_genes"]:
                    total_trap_amount[tournament] += thing["amount"]
            total_trap_amount[tournament] /= len(data["environment_genomes"])

            total_sensor_amount[tournament] = 0
            for _, robot in data["robot_genomes"].items():
                total_sensor_amount[tournament] += len(robot["sensors"])
            total_sensor_amount[tournament] /= len(data["robot_genomes"])

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

        winner_num_of_water_genes[tournament - 1] = len(winner_genome["water_genes"]) if "water_genes" in winner_genome else 0
        loser_num_of_water_genes[tournament - 1] = len(loser_genome["water_genes"]) if "water_genes" in loser_genome else 0
        winner_num_of_trap_genes[tournament - 1] = len(winner_genome["trap_genes"]) if "trap_genes" in winner_genome else 0
        loser_num_of_trap_genes[tournament - 1] = len(loser_genome["trap_genes"]) if "trap_genes" in loser_genome else 0
        winner_num_of_food_genes[tournament - 1] = len(winner_genome["food_genes"]) if "food_genes" in winner_genome else 0
        loser_num_of_food_genes[tournament - 1] = len(loser_genome["food_genes"]) if "food_genes" in loser_genome else 0
        winner_num_of_sensors[tournament - 1] = len(winner_genome["sensors"]) if "sensors" in winner_genome else 0
        loser_num_of_sensors[tournament - 1] = len(loser_genome["sensors"]) if "sensors" in loser_genome else 0

#graph peak fitness over tournaments
plt.figure(0)
plt.ylabel("number of tournaments")
plt.xlabel("peak_fitness")
plt.title("peak fitness over tournaments")
plt.plot(range(1, number_of_tournaments + 1), peak_fitnesses)
plt.savefig("Graphs/peak_fitness_over_tournaments.png")

#graph robot fitnesses for each tournament
plt.figure(1)
plt.xlabel("tournament")
plt.ylabel("mean robot fitness for the population")
plt.title("mean robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), mean_robot_fitnesses)
plt.savefig("Graphs/mean_robot_fitness.png")

#graph of peak robot fitness for the population for each tournament
plt.figure(2)
plt.xlabel("tournament")
plt.ylabel("peak robot fitness for the population")
plt.title("peak robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), peak_population_robot_fitnesses)
plt.savefig("Graphs/peak_robot_fitness_for_population.png")

#graph of peak environment fitness for the population fitness for each tournament
plt.figure(3)
plt.xlabel("tournament")
plt.ylabel("peak robot fitness for the population")
plt.title("peak robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), peak_population_environment_fitnesses)
plt.savefig("Graphs/peak_environment_fitness_for_population.png")

#graph of mean environment fitness for each tournament
plt.figure(4)
plt.xlabel("tournament")
plt.ylabel("peak environment fitness")
plt.title("mean environment fitness for each tournament")
plt.plot(range(1, number_of_tournaments + 1), mean_environment_fitnesses)
plt.savefig("Graphs/mean_environment_fitness_for_each_tournament.png")

#graph of number of water genes for each tournament
plt.figure(5)
plt.xlabel("tournament")
plt.ylabel("number of water genes")
plt.title("winner vs. loser for the number of water genes for each tournament")
plt.plot(range(1, number_of_tournaments + 1), winner_num_of_water_genes, color='m', label='winner')
plt.plot(range(1, number_of_tournaments + 1), loser_num_of_water_genes, color='r', label='loser')
plt.legend()
plt.savefig("Graphs/winner_vs_loser_water_genes.png")

#graph of number of traps genes for for each tournament
plt.figure(6)
plt.xlabel("tournament")
plt.ylabel("number of trap genes")
plt.title("winner vs. loser for the number of trap genes for each tournament")
plt.plot(range(1, number_of_tournaments + 1), winner_num_of_trap_genes, color='m', label='winner')
plt.plot(range(1, number_of_tournaments + 1), loser_num_of_trap_genes, color='r', label='loser')
plt.legend()
plt.savefig("Graphs/winner_vs_loser_trap_genes.png")

#graph of number of food genes for each tournament
plt.figure(7)
plt.xlabel("tournament")
plt.ylabel("number of food genes")
plt.title("winner vs. loser for the number of food genes for each tournament")
plt.plot(range(1, number_of_tournaments + 1), winner_num_of_food_genes, color='m', label='winner')
plt.plot(range(1, number_of_tournaments + 1), loser_num_of_food_genes, color='r', label='loser')
plt.legend()
plt.savefig("Graphs/winner_vs_loser_food_genes.png")

#graph of number of sensors for each tournament
plt.figure(8)
plt.xlabel("tournament")
plt.ylabel("number of sensors")
plt.title("winner vs. loser for the number of sensors for each tournament")
plt.plot(range(1, number_of_tournaments + 1), winner_num_of_sensors, color='m', label='winner')
plt.plot(range(1, number_of_tournaments + 1), loser_num_of_sensors, color='r', label='loser')
plt.legend()
plt.savefig("Graphs/winner_vs_loser_num_sensors.png")

#graph of number of thinjgs across population for each tournament
plt.figure(9)
plt.ylabel("amount of things")
plt.xlabel("tournament")
plt.title("mean number of things for each tournament")
plt.plot(range(1, number_of_tournaments + 1), total_thing_amount, color='b', label='Food + Water + Traps')
plt.plot(range(1, number_of_tournaments + 1), total_energy_amount, color='g', label='Food + Water')
plt.plot(range(1, number_of_tournaments + 1), total_trap_amount, color='r', label='Traps')
plt.legend()
plt.savefig("Graphs/mean_number_of_things_for_each_tournament.png")

#graph of number of sensors across population for each tournament
plt.figure(10)
plt.ylabel("amount of sensors")
plt.xlabel("tournament")
plt.title("mean number of sensors for each tournament")
plt.plot(range(1, number_of_tournaments + 1), total_sensor_amount)
plt.savefig("Graphs/mean_number_of_sensors_for_each_tournament.png")
