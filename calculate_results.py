import json

# Função para calcular o número de acertos e as porcentagens
def calculate_results(answers, answer_key):
    correct_answers = 0
    total_questions = 0

    for question, answer in answers.items():
        total_questions += 1
        if answer == answer_key.get(question):
            correct_answers += 1

    percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    return correct_answers, percentage

# Função principal para processar os JSONs e calcular a nota final
def process_exam_results(your_answers_file, answer_key_file):
    with open(your_answers_file, 'r') as f:
        your_answers = json.load(f)
    with open(answer_key_file, 'r') as f:
        answer_key = json.load(f)

    with open(role_weights_file, 'r') as f:
        role_weights = json.load(f)
    
    # Pesos dos eixos temáticos da prova de conhecimentos específicos
    with open(thematic_weights_file, 'r') as f:
        thematic_weights = json.load(f)
     

    results = {
        'general_knowledge': {},
        'specific_knowledge': {
            'axis_1': {},
            'axis_2': {},
            'axis_3': {},
            'axis_4': {},
            'axis_5': {}
        }
    }

    # Processa a prova 1 (CONHECIMENTOS GERAIS)
    answers = your_answers['exam']['general_knowledge']['answers']
    answer_key_mod = answer_key['exam']['general_knowledge']['answers']
    correct, percentage = calculate_results(answers, answer_key_mod)
    results['general_knowledge'] = {
        'correct_answers': correct,
        'percentage': percentage,
        'score': correct * 5,  # Nota na escala de 100
    }

    # Processa a prova 2 (CONHECIMENTOS ESPECÍFICOS)
    total_weighted_score = 0
    for module, weight in thematic_weights.items():
        answers = your_answers['exam']['specific_knowledge'][module]['questions']
        answer_key_mod = answer_key['exam']['specific_knowledge'][module]['questions']
        correct, percentage = calculate_results(answers, answer_key_mod)
        score = correct * 10 / len(answers)  # Nota do eixo na escala de 100
        weighted_score = score * weight
        results['specific_knowledge'][module] = {
            'correct_answers': correct,
            'percentage': percentage,
            'weighted_score': weighted_score
        }
        total_weighted_score += weighted_score

    # Nota final ponderada
    general_knowledge_weighted_score = results['general_knowledge']['score'] * role_weights['general_knowledge']
    specific_knowledge_weighted_score = total_weighted_score * role_weights['specific_knowledge']

    final_score = general_knowledge_weighted_score + specific_knowledge_weighted_score
    results['final'] = {
        'general_knowledge_weighted_score': general_knowledge_weighted_score,
        'specific_knowledge_weighted_score': specific_knowledge_weighted_score,
        'final_score': final_score
    }

    return results

# Arquivos JSON 
your_answers_file = 'my_answers.json'
answer_key_file = 'correct_answers.json'
thematic_weights_file = 'thematic_weights.json'
role_weights_file = 'role_weights.json'

# Processa os resultados e imprime
results = process_exam_results(your_answers_file, answer_key_file)
print(json.dumps(results, indent=4))
