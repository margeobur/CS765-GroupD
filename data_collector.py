import json

class TrialDataCollector:
    def __init__(self, tournament_num):
        self.tournament = tournament_num
        self.outfile = open("tournament_data.json", "w")
        self.json_content = {
            "tournament": self.tournament
        }
        self.fitness_a = 0
        self.fitness_b = 0

    def save_fitness_a(self, fitness):
        self.fitness_a = fitness

    def save_data(self):
        self.outfile.write(json.dumps(self.json_content))
        self.outfile.close()

# class DataCollector:
#     def __init__(self):
#         mean_fitness = []
#         max_fitness = []
