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


def diagnose(diseases):
    if not diseases:
        print('No disease data available. Add diseases first.')
        return

    all_symptoms = []

    for syms in diseases.values():
        for s in syms:
            if s not in all_symptoms:
                all_symptoms.append(s)

    print('Please answer the following questions with y (yes) or n (no).')

    positive = set()
    negative = set()
    candidates = set(diseases.keys())

    try:
        for symptom in all_symptoms:

            prev_candidates = set(candidates)

            ans = input(f'Do you have "{symptom}"? (y/n): ').strip().lower()

            while ans not in ('y', 'n', 'yes', 'no'):
                ans = input('Please enter y or n: ').strip().lower()

            if ans.startswith('y'):
                positive.add(symptom)
                candidates = {
                    d for d in candidates if symptom in diseases[d]
                }
            else:
                negative.add(symptom)
                candidates = {
                    d for d in candidates if symptom not in diseases[d]
                }

            ruled_out = sorted(prev_candidates - candidates)

            if ruled_out:
                print(f'  Ruled out: {", ".join(ruled_out)}')

            print(f'  Remaining candidates: {len(candidates)}')

            # Early stopping if only one candidate remains
            if len(candidates) == 1:
                print(
                    f'\nDiagnosis: {next(iter(candidates))} '
                    '(only one candidate left)'
                )
                return

            # No candidates left
            if not candidates:
                print(
                    '\nNo matching disease found based on your answers. '
                    'Stopping early.'
                )
                return

    except (KeyboardInterrupt, EOFError):
        print('\nInput cancelled.')
        return

    scores = []

    for name in candidates:
        syms = diseases[name]
        syms_set = set(syms)

        matched = len(syms_set & positive)

        score = matched / len(syms) if syms else 0

        scores.append((score, matched, name, syms))

    if not scores:
        print('No matching disease found based on the answers.')
        return

    scores.sort(reverse=True)

    best_score, matched, best_name, best_syms = scores[0]

    if best_score == 0:
        print('No matching disease found based on the answers.')
        return

    top = [s for s in scores if s[0] == best_score]

    print('\nPossible diagnosis:')

    for score, matched, name, syms in top:

        percent = int(score * 100)

        common = list(set(syms) & positive)

        print(f'- {name} ({percent}% match — {matched} matching symptoms)')

        if common:
            print(f'  Matching symptoms: {", ".join(common)}')

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

