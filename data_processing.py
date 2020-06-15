import os
import json
import matplotlib.pyplot as plt
import statistics
import re
import itertools
import numpy as np


#SET NUMBER OF TOURNAMENTS
number_of_tournaments = 2260

#SET POPULATION NUM
num_pop = 30

SRC_DIR = "Data"
DEST_DIR = "Graphs"

RENDER_FUZZINESS_AND_CONVERGENCE = True
RENDER_SMELL_SIGNATURE_IMAGE = True

peak_fitnesses = [0] * number_of_tournaments
mean_robot_fitnesses = [0] * number_of_tournaments
mean_environment_fitnesses = [0] * number_of_tournaments
peak_population_robot_fitnesses = [0] * number_of_tournaments
peak_population_environment_fitnesses = [0] * number_of_tournaments
total_thing_amount = [0] * number_of_tournaments
total_energy_amount = [0] * number_of_tournaments
total_trap_amount = [0] * number_of_tournaments
total_sensor_amount = [0] * number_of_tournaments
sensor_energy_snr = [0] * number_of_tournaments
sensor_trap_snr = [0] * number_of_tournaments
sensor_discriminability = [0] * number_of_tournaments
mean_sensor_fuzziness = np.array([None] * number_of_tournaments).astype(np.double)
mean_robot_smell_convergence = np.array([None] * number_of_tournaments).astype(np.double)
mean_environment_food_smell_convergence = np.array([None] * number_of_tournaments).astype(np.double)
mean_environment_water_smell_convergence = np.array([None] * number_of_tournaments).astype(np.double)
mean_environment_trap_smell_convergence = np.array([None] * number_of_tournaments).astype(np.double)
smell_image = np.zeros((620, number_of_tournaments * 2, 3))

winner_num_of_water_genes = [0] * number_of_tournaments
loser_num_of_water_genes = [0] * number_of_tournaments
winner_num_of_trap_genes = [0] * number_of_tournaments
loser_num_of_trap_genes = [0] * number_of_tournaments
winner_num_of_food_genes = [0] * number_of_tournaments
loser_num_of_food_genes = [0] * number_of_tournaments
winner_num_of_sensors = [0] * number_of_tournaments
loser_num_of_sensors = [0] * number_of_tournaments

for filename in os.listdir(SRC_DIR):
    path = os.path.join(SRC_DIR, filename)

    with open(path, "r") as json_file:
        try:
            data = json.load(json_file)
        except:
            continue

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

            sensor_energy_snr[tournament] = 0
            sensor_trap_snr[tournament] = 0
            sensor_discriminability[tournament] = 0
            for _, robot in data["robot_genomes"].items():
                energy_snr_for_robot = 0
                trap_snr_for_robot = 0
                discriminability_for_robot = 0
                for sensor in robot["sensors"]:
                    sum_energy_alignment = 0
                    sum_trap_alignment = 0
                    num_things = 0
                    for _, environment in data["environment_genomes"].items():
                        for energy in itertools.chain(environment["water_genes"], environment["food_genes"]):
                            sum_energy_alignment += np.dot(sensor["smell_signature"], energy["smell_signature"])
                            num_things += 1
                        for trap in environment["trap_genes"]:
                            sum_trap_alignment += np.dot(sensor["smell_signature"], trap["smell_signature"])
                            num_things += 1
                    energy_snr_for_sensor = sum_energy_alignment / sum_trap_alignment
                    trap_snr_for_sensor = 1 / energy_snr_for_sensor
                    energy_snr_for_sensor = abs(energy_snr_for_sensor)
                    trap_snr_for_sensor = abs(trap_snr_for_sensor)
                    energy_snr_for_robot = max(energy_snr_for_robot, energy_snr_for_sensor)
                    trap_snr_for_robot = max(trap_snr_for_robot, trap_snr_for_sensor)
                    discriminability_for_robot = max(discriminability_for_robot, abs(sum_energy_alignment - sum_trap_alignment) / num_things)
                sensor_energy_snr[tournament] += energy_snr_for_robot
                sensor_trap_snr[tournament] += trap_snr_for_robot
                sensor_discriminability[tournament] += discriminability_for_robot
            sensor_energy_snr[tournament] /= len(data["robot_genomes"])
            sensor_trap_snr[tournament] /= len(data["robot_genomes"])
            sensor_discriminability[tournament] /= len(data["robot_genomes"])

            if RENDER_SMELL_SIGNATURE_IMAGE:
                smell_image_row = smell_image.shape[0] // 2 - 4
                for _, robot in data["robot_genomes"].items():
                    for sensor in robot["sensors"]:
                        signature = sensor["smell_signature"]
                        smell_image[smell_image_row, tournament * 2, 0] = signature[0] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2, 1] = signature[1] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2, 2] = signature[2] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2 + 1, 0] = signature[3] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2 + 1, 1] = signature[4] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2 + 1, 2] = signature[4] / 2 + 0.5
                        smell_image_row -= 1
                    smell_image_row -= 3
                smell_image_row = smell_image.shape[0] // 2 + 4
                for _, environment in data["environment_genomes"].items():
                    for thing in itertools.chain(environment["water_genes"], environment["food_genes"], environment["trap_genes"]):
                        signature = thing["smell_signature"]
                        smell_image[smell_image_row, tournament * 2, 0] = signature[0] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2, 1] = signature[1] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2, 2] = signature[2] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2 + 1, 0] = signature[3] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2 + 1, 1] = signature[4] / 2 + 0.5
                        smell_image[smell_image_row, tournament * 2 + 1, 2] = signature[4] / 2 + 0.5
                        smell_image_row += 1
                    smell_image_row += 3

            if RENDER_FUZZINESS_AND_CONVERGENCE and tournament % 50 == 0:
                mean_sensor_fuzziness[tournament] = 0
                for _, robot in data["robot_genomes"].items():
                    sensor_fuzziness_for_robot = 0
                    for _, environment in data["environment_genomes"].items():
                        sensor_fuzziness_for_environment = 0
                        for sensor in robot["sensors"]:
                            mean_square_energy_alignment = 0
                            for energy in itertools.chain(environment["water_genes"], environment["food_genes"]):
                                mean_square_energy_alignment += np.dot(sensor["smell_signature"],
                                                                       energy["smell_signature"]) ** 2
                            mean_square_energy_alignment /= len(environment["water_genes"]) + len(
                                environment["food_genes"])
                            mean_square_trap_alignment = 0
                            for trap in environment["trap_genes"]:
                                mean_square_trap_alignment += np.dot(sensor["smell_signature"],
                                                                     trap["smell_signature"]) ** 2
                            mean_square_trap_alignment /= len(environment["trap_genes"])
                            sensor_fuzziness_for_environment += (
                                                                        mean_square_energy_alignment * mean_square_trap_alignment) / (
                                                                        max(mean_square_trap_alignment,
                                                                            mean_square_energy_alignment) ** 2)
                        sensor_fuzziness_for_environment /= len(robot["sensors"])
                        sensor_fuzziness_for_robot += sensor_fuzziness_for_environment
                    sensor_fuzziness_for_robot /= len(data["environment_genomes"])
                    mean_sensor_fuzziness[tournament] += sensor_fuzziness_for_robot
                mean_sensor_fuzziness[tournament] /= len(data["robot_genomes"])

                mean_environment_water_smell_convergence[tournament] = 0
                mean_environment_food_smell_convergence[tournament] = 0
                mean_environment_trap_smell_convergence[tournament] = 0
                for _, a in data["environment_genomes"].items():
                    water_smell_convergence_for_a = 0
                    food_smell_convergence_for_a = 0
                    trap_smell_convergence_for_a = 0
                    for _, b in data["environment_genomes"].items():
                        water_smell_convergence_for_b = 0
                        for ag in a["water_genes"]:
                            best_alignment = 0
                            for bg in b["water_genes"]:
                                ags = np.array(ag["smell_signature"], dtype=np.double)
                                bgs = np.array(bg["smell_signature"], dtype=np.double)
                                ags /= np.linalg.norm(ags)
                                bgs /= np.linalg.norm(bgs)
                                alignment = ags.dot(bgs) ** 2
                                best_alignment = max(best_alignment, alignment)
                            water_smell_convergence_for_b += best_alignment
                        water_smell_convergence_for_b /= len(a["water_genes"])

                        food_smell_convergence_for_b = 0
                        for ag in a["food_genes"]:
                            best_alignment = 0
                            for bg in b["food_genes"]:
                                ags = np.array(ag["smell_signature"], dtype=np.double)
                                bgs = np.array(bg["smell_signature"], dtype=np.double)
                                ags /= np.linalg.norm(ags)
                                bgs /= np.linalg.norm(bgs)
                                alignment = ags.dot(bgs) ** 2
                                best_alignment = max(best_alignment, alignment)
                            food_smell_convergence_for_b += best_alignment
                        food_smell_convergence_for_b /= len(a["food_genes"])

                        trap_smell_convergence_for_b = 0
                        for ag in a["trap_genes"]:
                            best_alignment = 0
                            for bg in b["trap_genes"]:
                                ags = np.array(ag["smell_signature"], dtype=np.double)
                                bgs = np.array(bg["smell_signature"], dtype=np.double)
                                ags /= np.linalg.norm(ags)
                                bgs /= np.linalg.norm(bgs)
                                alignment = ags.dot(bgs) ** 2
                                best_alignment = max(best_alignment, alignment)
                            trap_smell_convergence_for_b += best_alignment
                        trap_smell_convergence_for_b /= len(a["trap_genes"])

                        water_smell_convergence_for_a += water_smell_convergence_for_b
                        food_smell_convergence_for_a += food_smell_convergence_for_b
                        trap_smell_convergence_for_a += trap_smell_convergence_for_b
                    water_smell_convergence_for_a /= len(data["environment_genomes"])
                    food_smell_convergence_for_a /= len(data["environment_genomes"])
                    trap_smell_convergence_for_a /= len(data["environment_genomes"])
                    mean_environment_water_smell_convergence[tournament] += water_smell_convergence_for_a
                    mean_environment_food_smell_convergence[tournament] += food_smell_convergence_for_a
                    mean_environment_trap_smell_convergence[tournament] += trap_smell_convergence_for_a
                mean_environment_water_smell_convergence[tournament] /= len(data["environment_genomes"])
                mean_environment_food_smell_convergence[tournament] /= len(data["environment_genomes"])
                mean_environment_trap_smell_convergence[tournament] /= len(data["environment_genomes"])

                mean_robot_smell_convergence[tournament] = 0
                for _, a in data["robot_genomes"].items():
                    robot_smell_convergence_for_a = 0
                    for _, b in data["robot_genomes"].items():
                        robot_smell_convergence_for_b = 0
                        for ag in a["sensors"]:
                            best_alignment = 0
                            for bg in b["sensors"]:
                                ags = np.array(ag["smell_signature"])
                                bgs = np.array(bg["smell_signature"])
                                ags /= np.linalg.norm(ags)
                                bgs /= np.linalg.norm(bgs)
                                alignment = ags.dot(bgs) ** 2
                                best_alignment = max(best_alignment, alignment)
                            robot_smell_convergence_for_b += best_alignment
                        robot_smell_convergence_for_b /= len(a["sensors"])
                        robot_smell_convergence_for_a += robot_smell_convergence_for_b
                    robot_smell_convergence_for_a /= len(data["robot_genomes"])
                    mean_robot_smell_convergence[tournament] += robot_smell_convergence_for_a
                mean_robot_smell_convergence[tournament] /= len(data["robot_genomes"])

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
plt.xlabel("number of tournaments")
plt.ylabel("peak_fitness")
plt.title("peak fitness over tournaments")
plt.plot(range(1, number_of_tournaments + 1), peak_fitnesses)
plt.savefig(DEST_DIR + "/peak_fitness_over_tournaments.png")

#graph robot fitnesses for each tournament
plt.figure(1)
plt.xlabel("tournament")
plt.ylabel("mean robot fitness for the population")
plt.title("mean robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), mean_robot_fitnesses)
plt.savefig(DEST_DIR + "/mean_robot_fitness.png")

#graph of peak robot fitness for the population for each tournament
plt.figure(2)
plt.xlabel("tournament")
plt.ylabel("peak robot fitness for the population")
plt.title("peak robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), peak_population_robot_fitnesses)
plt.savefig(DEST_DIR + "/peak_robot_fitness_for_population.png")

#graph of peak environment fitness for the population fitness for each tournament
plt.figure(3)
plt.xlabel("tournament")
plt.ylabel("peak robot fitness for the population")
plt.title("peak robot fitness for the population over each tournament")
plt.plot(range(1, number_of_tournaments + 1), peak_population_environment_fitnesses)
plt.savefig(DEST_DIR + "/peak_environment_fitness_for_population.png")

#graph of mean environment fitness for each tournament
plt.figure(4)
plt.xlabel("tournament")
plt.ylabel("peak environment fitness")
plt.title("mean environment fitness for each tournament")
plt.plot(range(1, number_of_tournaments + 1), mean_environment_fitnesses)
plt.savefig(DEST_DIR + "/mean_environment_fitness_for_each_tournament.png")

#graph of number of water genes for each tournament
plt.figure(5)
plt.xlabel("tournament")
plt.ylabel("number of water genes")
plt.title("winner vs. loser for the number of water genes for each tournament")
plt.plot(range(1, number_of_tournaments + 1), winner_num_of_water_genes, color='m', label='winner')
plt.plot(range(1, number_of_tournaments + 1), loser_num_of_water_genes, color='r', label='loser')
plt.legend()
plt.savefig(DEST_DIR + "/winner_vs_loser_water_genes.png")

#graph of number of traps genes for for each tournament
plt.figure(6)
plt.xlabel("tournament")
plt.ylabel("number of trap genes")
plt.title("winner vs. loser for the number of trap genes for each tournament")
plt.plot(range(1, number_of_tournaments + 1), winner_num_of_trap_genes, color='m', label='winner')
plt.plot(range(1, number_of_tournaments + 1), loser_num_of_trap_genes, color='r', label='loser')
plt.legend()
plt.savefig(DEST_DIR + "/winner_vs_loser_trap_genes.png")

#graph of number of food genes for each tournament
plt.figure(7)
plt.xlabel("tournament")
plt.ylabel("number of food genes")
plt.title("winner vs. loser for the number of food genes for each tournament")
plt.plot(range(1, number_of_tournaments + 1), winner_num_of_food_genes, color='m', label='winner')
plt.plot(range(1, number_of_tournaments + 1), loser_num_of_food_genes, color='r', label='loser')
plt.legend()
plt.savefig(DEST_DIR + "/winner_vs_loser_food_genes.png")

#graph of number of sensors for each tournament
plt.figure(8)
plt.xlabel("tournament")
plt.ylabel("number of sensors")
plt.title("winner vs. loser for the number of sensors for each tournament")
plt.plot(range(1, number_of_tournaments + 1), winner_num_of_sensors, color='m', label='winner')
plt.plot(range(1, number_of_tournaments + 1), loser_num_of_sensors, color='r', label='loser')
plt.legend()
plt.savefig(DEST_DIR + "/winner_vs_loser_num_sensors.png")

#graph of number of thinjgs across population for each tournament
plt.figure(9)
plt.ylabel("amount of things")
plt.xlabel("tournament")
plt.title("mean number of things for each tournament")
plt.plot(range(1, number_of_tournaments + 1), total_thing_amount, color='b', label='Food + Water + Traps')
plt.plot(range(1, number_of_tournaments + 1), total_energy_amount, color='g', label='Food + Water')
plt.plot(range(1, number_of_tournaments + 1), total_trap_amount, color='r', label='Traps')
plt.legend()
plt.savefig(DEST_DIR + "/mean_number_of_things_for_each_tournament.png")

#graph of number of sensors across population for each tournament
plt.figure(10)
plt.ylabel("amount of sensors")
plt.xlabel("tournament")
plt.title("mean number of sensors for each tournament")
plt.plot(range(1, number_of_tournaments + 1), total_sensor_amount)
plt.savefig(DEST_DIR + "/mean_number_of_sensors_for_each_tournament.png")

#graph of SNR across population for each tournament
plt.figure(200)
plt.ylabel("signal to noise ratio")
plt.xlabel("tournament")
plt.yscale("log")
plt.title("mean signal to noise ratio for detecting energy / traps for each tournament")
plt.plot(range(1, number_of_tournaments + 1), sensor_energy_snr, color='b', label='Detecting Food and Water')
plt.plot(range(1, number_of_tournaments + 1), sensor_trap_snr, color='r', label='Detecting Traps')
plt.legend()
plt.savefig(DEST_DIR + "/sensor_signal_to_noise_ratio_for_each_tournament.png")

#graph of discriminability across population for each tournament
plt.figure(300)
plt.ylabel("discriminability")
plt.xlabel("tournament")
plt.title("average discriminability of robot's best sensor for each tournament")
plt.plot(range(1, number_of_tournaments + 1), sensor_discriminability)
plt.savefig(DEST_DIR + "/sensor_discriminability_for_each_tournament.png")

if RENDER_SMELL_SIGNATURE_IMAGE:
    # plot smell signatures over tournaments
    plt.figure(100, figsize=(smell_image.shape[1] / 100 + 2, smell_image.shape[0] / 100 + 2))
    plt.xlabel("tournament")
    plt.title("smell signatures for each tournament")
    plt.imshow(smell_image)
    plt.savefig(DEST_DIR + "/smell_signatures.png")

if RENDER_FUZZINESS_AND_CONVERGENCE:
    #graph of how fuzzy across population for each tournament
    plt.figure(11)
    plt.ylabel("sensor fuzziness")
    plt.xlabel("tournament")
    plt.title("mean sensor fuzziness for each tournament")
    mask = np.isfinite(mean_sensor_fuzziness)
    ys = mean_sensor_fuzziness[mask]
    xs = np.arange(len(mean_sensor_fuzziness))[mask]
    plt.plot(xs, ys)
    plt.savefig(DEST_DIR + "/mean_sensor_fuzziness_for_each_tournament.png")

    #graph of smell signature convergence for each tournament
    plt.figure(12)
    plt.ylabel("smell similarity")
    plt.xlabel("tournament")
    plt.title("smell convergence for each tournament")
    mask = np.isfinite(mean_environment_water_smell_convergence)
    ys = mean_environment_water_smell_convergence[mask]
    xs = np.arange(len(mean_environment_water_smell_convergence))[mask]
    plt.plot(xs, ys, color='b', label='Water')
    mask = np.isfinite(mean_environment_food_smell_convergence)
    ys = mean_environment_food_smell_convergence[mask]
    xs = np.arange(len(mean_environment_food_smell_convergence))[mask]
    plt.plot(xs, ys, color='y', label='Food')
    mask = np.isfinite(mean_environment_trap_smell_convergence)
    ys = mean_environment_trap_smell_convergence[mask]
    xs = np.arange(len(mean_environment_trap_smell_convergence))[mask]
    plt.plot(xs, ys, color='r', label='Traps')
    mask = np.isfinite(mean_robot_smell_convergence)
    ys = mean_robot_smell_convergence[mask]
    xs = np.arange(len(mean_robot_smell_convergence))[mask]
    plt.plot(xs, ys, color='g', label='Robots')
    plt.legend()
    plt.savefig(DEST_DIR + "/mean_smell_convergence_for_each_tournament.png")
