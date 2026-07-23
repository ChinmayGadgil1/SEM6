import json

with open("knowledge.json", "r") as file:
    diseases = json.load(file)

print("=== Medical Expert System ===")

symptoms = {}
all_symptoms = set()

for disease in diseases:
    for symptom in diseases[disease]:
        all_symptoms.add(symptom)

for symptom in all_symptoms:
    ans = input(f"Do you have {symptom}? (yes/no): ").lower()
    symptoms[symptom] = ans

best = ""
max_match = -1

for disease in diseases:
    count = 0
    for symptom in diseases[disease]:
        if symptoms[symptom] == "yes":
            count += 1

    if count > max_match:
        max_match = count
        best = disease

print("\nMost Probable Disease:", best)
print("Matched Symptoms:", max_match)

