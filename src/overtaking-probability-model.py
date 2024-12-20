import numpy as np
import matplotlib.pyplot as plt

class OvertakingProbabilityModel:
    def __init__(self, config):
        self.car_performance = config.get("car_performance", 1.0)  # Speed differential multiplier
        self.track_difficulty = config.get("track_difficulty", 0.5)  # 0 (easy) to 1 (difficult)
        self.driver_aggressiveness = config.get("driver_aggressiveness", 0.7)  # 0 to 1
        self.driver_defensiveness = config.get("driver_defensiveness", 0.6)  # 0 to 1
        self.weather_condition = config.get("weather_condition", 1.0)  # Multiplier for dry (1.0) to wet (0.7)
        self.simulations = config.get("simulations", 1000)  # Number of Monte Carlo simulations
        self.sections = config.get("sections", 10)  # Number of track sections
        self.overtake_zones = config.get("overtake_zones", [0.2, 0.8])  # Overtake-friendly sections (proportions)

    def simulate_overtaking_probability(self):
        probabilities = []

        for section in range(self.sections):
            section_probabilities = []
            overtake_zone_bonus = 1 if section / self.sections in self.overtake_zones else 0.8

            for _ in range(self.simulations):
                # Calculate performance-based overtaking probability
                performance_factor = np.random.normal(self.car_performance, 0.1)
                track_factor = np.random.uniform(0.5, 1 - self.track_difficulty)
                driver_factor = (self.driver_aggressiveness - self.driver_defensiveness)
                weather_factor = self.weather_condition

                # Combine factors to estimate overtaking likelihood
                overtake_chance = performance_factor * track_factor * driver_factor * weather_factor * overtake_zone_bonus
                overtake_chance = max(0, min(overtake_chance, 1))  # Clamp to [0, 1]

                section_probabilities.append(overtake_chance)

            probabilities.append(np.mean(section_probabilities))

        return probabilities

    def analyse_overtaking_patterns(self):
        results = {
            "average_probabilities": [],
            "success_rates": []
        }

        probabilities = self.simulate_overtaking_probability()
        for prob in probabilities:
            success_rate = prob * 0.85 + np.random.uniform(-0.05, 0.05)  # Add variability to success rates
            results["average_probabilities"].append(prob)
            results["success_rates"].append(max(0, min(success_rate, 1)))

        return results

    def plot_results(self, results):
        sections = range(1, self.sections + 1)

        plt.figure(figsize=(12, 8))

        # Plot overtaking probabilities
        plt.subplot(2, 1, 1)
        plt.bar(sections, results["average_probabilities"], color="skyblue", label="Overtaking Probability")
        plt.title("Overtaking Probability by Track Section")
        plt.xlabel("Track Section")
        plt.ylabel("Probability of Overtaking")
        plt.grid(True)
        plt.legend()

        # Plot success rates
        plt.subplot(2, 1, 2)
        plt.plot(sections, results["success_rates"], color="green", marker="o", label="Success Rate")
        plt.title("Overtaking Success Rate by Track Section")
        plt.xlabel("Track Section")
        plt.ylabel("Success Rate")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    config = {
        "car_performance": 1.2,
        "track_difficulty": 0.6,
        "driver_aggressiveness": 0.8,
        "driver_defensiveness": 0.5,
        "weather_condition": 0.8,
        "simulations": 1000,
        "sections": 10,
        "overtake_zones": [0.2, 0.5, 0.8]
    }

    model = OvertakingProbabilityModel(config)
    results = model.analyse_overtaking_patterns()
    model.plot_results(results)