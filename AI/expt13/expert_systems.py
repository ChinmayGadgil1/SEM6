import os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'diseases.txt')


def load_diseases(path=DATA_FILE):
	diseases = {}
	if not os.path.exists(path):
		return diseases
	with open(path, 'r', encoding='utf-8') as f:
		for line in f:
			line = line.strip()
			if not line or line.startswith('#'):
				continue
			if ':' not in line:
				continue
			name, symptoms = line.split(':', 1)
			syms = [s.strip().lower() for s in symptoms.split(',') if s.strip()]
			diseases[name.strip()] = syms
	return diseases

def list_diseases(diseases):
	if not diseases:
		print('No diseases in database.')
		return
	for name, syms in diseases.items():
		print(f"- {name}: {', '.join(syms)}")


def get_discriminating_symptoms(candidates, diseases):
	
	if not candidates:
		return []
	
	symptom_scores = {}
	
	for symptom in set(s for d in candidates for s in diseases[d]):
		have_symptom = sum(1 for d in candidates if symptom in diseases[d])
		dont_have = len(candidates) - have_symptom
		
		if have_symptom > 0 and dont_have > 0:
			balance = min(have_symptom, dont_have) / len(candidates)
			symptom_scores[symptom] = balance
		elif have_symptom > 0:
			symptom_scores[symptom] = 0.01
		elif dont_have > 0:
			symptom_scores[symptom] = 0.01 
	sorted_symptoms = sorted(symptom_scores.items(), key=lambda x: x[1], reverse=True)
	print(f'  → Discriminating symptoms: {[s[0] + ": " + f"{s[1]:.2f}" for s in sorted_symptoms[:5]]}')
 
    
	return [s[0] for s in sorted_symptoms]


def diagnose(diseases):
	if not diseases:
		print('No disease data available. Add diseases first.')
		return


	positive_symptoms = set()
	asked_symptoms = set()
	candidates = set(diseases.keys())
	question_count = 0

	try:
		while candidates:
			discriminating = get_discriminating_symptoms(candidates, diseases)
			
			if not discriminating:
				break
			
			unanswered = [s for s in discriminating if s not in asked_symptoms]
			
			if not unanswered:
				unanswered = [s for s in set(s for d in candidates for s in diseases[d]) if s not in asked_symptoms]
				if not unanswered:
					break
			
			symptom = unanswered[0]
			asked_symptoms.add(symptom)
			question_count += 1
			
			print(f'[Question {question_count}] Do you have "{symptom}"? (y/n): ', end='')
			ans = input().strip().lower()
			
			while ans not in ('y', 'n', 'yes', 'no'):
				print('Please enter y or n: ', end='')
				ans = input().strip().lower()
			
			prev_count = len(candidates)
			
			if ans.startswith('y'):
				positive_symptoms.add(symptom)
				candidates = {d for d in candidates if symptom in diseases[d]}
			else:
				candidates = {d for d in candidates if symptom not in diseases[d]}
			
			if len(candidates) < prev_count:
				ruled_out = prev_count - len(candidates)
				print(f'  → Eliminated {ruled_out} possibilities')
			
			print(f'  → Remaining candidates: {len(candidates)}\n')
			
			if len(candidates) == 1:
				diagnosis = next(iter(candidates))
				print('='*60)
				print(f'DIAGNOSIS: {diagnosis}')
				print(f'(Identified after {question_count} questions)')
				print('='*60)
				return
			
			if not candidates:
				print('\n' + '='*60)
				print('NO MATCHING DISEASE FOUND')
				print('Your symptoms do not match any known disease in the database.')
				print('='*60)
				return
		
	
	# 	if candidates:
	# 		scores = []
	# 		for name in candidates:
	# 			syms_set = set(diseases[name])
	# 			matched = len(syms_set & positive_symptoms)
	# 			score = matched / len(syms_set) if syms_set else 0
	# 			scores.append((score, matched, name, syms_set))
			
	# 		scores.sort(reverse=True, key=lambda x: (x[0], x[1]))
			
	# 		best_score = scores[0][0]
	# 		top_diagnoses = [s for s in scores if s[0] == best_score]
			
	# 		print('='*60)
	# 		print('POSSIBLE DIAGNOSES:')
	# 		print('='*60)
			
	# 		for score, matched, name, syms in top_diagnoses:
	# 			confidence = int(score * 100)
	# 			common = list(syms & positive_symptoms)
	# 			print(f'\n{name}')
	# 			print(f'  Confidence: {confidence}%')
	# 			print(f'  Matching symptoms: {matched}/{len(syms)}')
	# 			if common:
	# 				print(f'  You have: {", ".join(common)}')
			
	# 		print('='*60)
	# 	else:
	# 		print('\n' + '='*60)
	# 		print('NO DIAGNOSIS POSSIBLE')
	# 		print('='*60)
	
	except (KeyboardInterrupt, EOFError):
		print('\n\nDiagnosis cancelled.')
		return

def main():
	while True:
		diseases = load_diseases()
		print('\nExpert System — Simple Disease Diagnoser')
		print('1) Diagnose')
		print('2) List  diseases')
		print('3) Quit')
		choice = input('Choose an option: ').strip()
		if choice == '1':
			diagnose(diseases)
		elif choice == '2':
			list_diseases(diseases)

		elif choice == '3' or choice.lower() in ('q', 'quit', 'exit'):
			print('exiting.')
			break
		else:
			print('Invalid option. Enter 1-3.')


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\nInterrupted. Exiting.')

