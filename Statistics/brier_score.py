import csv

def brier_score_from_csv(csv_file):
    observed = []
    predicted = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            confidence_probability = float(row[1])
            truth_value = 1 if int(row[0]) > 100 else 0  # Mapping truth values
            observed.append(truth_value)
            predicted.append(confidence_probability)
            print(f"Predicted Probability: {confidence_probability}, Observed: {truth_value}")

    n = len(observed)
    brier_sum = sum((observed[i] - predicted[i])**2 for i in range(n))
    print("Squared Differences:", [(observed[i] - predicted[i])**2 for i in range(n)])
    brier_score = brier_sum / n
    return brier_score

# Example usage:
csv_file = 'Brier.csv'  # Replace 'data.csv' with your CSV file path
print("Brier Score:", brier_score_from_csv(csv_file))