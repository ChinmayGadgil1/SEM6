diseases = {
    "Cold": ["cough", "sneezing", "runny nose"],
    "Flu": ["fever", "cough", "body ache"],
    "Allergy": ["sneezing", "itchy eyes", "runny nose"],
    "Bronchitis": ["cough", "chest pain", "fever"]
}

def get_discriminating_symptoms(candidates, diseases):
    if not candidates:
        return []
    
    symptom_scores = {}
    for symptom in set(s for d in candidates for s in diseases[d]):
        have = sum(1 for d in candidates if symptom in diseases[d])
        dont_have = len(candidates) - have
        
        if have > 0 and dont_have > 0:
            symptom_scores[symptom] = min(have, dont_have) / len(candidates)
    
    return [s[0] for s in sorted(symptom_scores.items(), key=lambda x: x[1], reverse=True)]

def diagnose():
    positive_symptoms = set()
    asked_symptoms = set()
    candidates = set(diseases.keys())
    
    print("\nExpert System - Disease Diagnosis\n")
    
    while candidates:
        print(f"Possible diseases: {candidates}")
        
        discriminating = get_discriminating_symptoms(candidates, diseases)
        
        if not discriminating:
            break
        
        unanswered = [s for s in discriminating if s not in asked_symptoms]
        
        if not unanswered:
            break
        
        symptom = unanswered[0]
        asked_symptoms.add(symptom)
        
        response = input(f"\nDo you have {symptom}? (yes/no): ").lower().strip()
        
        if response == "yes":
            positive_symptoms.add(symptom)
            candidates = {d for d in candidates if symptom in diseases[d]}
        else:
            candidates = {d for d in candidates if symptom not in diseases[d]}
    
    if candidates:
        print(f"\nLikely diagnosis: {list(candidates)[0]}")
    else:
        print("\nNo matching disease found")

diagnose()
