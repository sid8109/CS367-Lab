from string import ascii_lowercase
from itertools import combinations
import random

print("Enter the number of clauses: ")
m = int(input())
print("Enter the number of variables: ")
n = int(input())
k = 3

def generate_clauses():
    limit = 1
    problems = []
    pos = list(ascii_lowercase)[:n]
    neg = [x.upper() for x in pos]
    total_var = pos + neg
    all_clauses = list(combinations(total_var, k))
    
    for _ in range(limit):
        p = random.sample(all_clauses, m)
        if p not in problems:
            problems.append(p)
    
    return problems, pos

def assign_values(pos):
    values = {}
    for var in pos:
        values[var] = random.choice([True, False])
    return values

def count_satisfied_clauses(problem, assignment):
    return sum(any(assignment[var] if var.islower() else not assignment[var.lower()] for var in clause) for clause in problem)

def weighted_clause_satisfaction(problem, assignment):
    var_frequency = {}
    for clause in problem:
        for var in clause:
            var_frequency[var.lower()] = var_frequency.get(var.lower(), 0) + 1

    score = 0
    for clause in problem:
        if any(assignment[var] if var.islower() else not assignment[var.lower()] for var in clause):
            clause_weight = sum(1 / var_frequency[var.lower()] for var in clause)
            score += clause_weight
    return score

def penetrance(clauses_satisfied, total_clauses):
    return clauses_satisfied / total_clauses

def hill_climbing(problem, pos, heuristic_func):
    current_assignment = assign_values(pos)
    current_score = heuristic_func(problem, current_assignment)
        
    while True:
        neighbors = []
        for var in pos:
            neighbor = current_assignment.copy()
            neighbor[var] = not neighbor[var]
            neighbors.append(neighbor)
            
        next_assignment = max(neighbors, key=lambda x: heuristic_func(problem, x))
        next_score = heuristic_func(problem, next_assignment)        
        if next_score <= current_score:
            break
            
        current_assignment = next_assignment
        current_score = next_score
        
    return current_assignment, current_score

def beam_search(problem, pos, beam_width, heuristic_func):
    current_assignments = [assign_values(pos)]
    current_scores = [heuristic_func(problem, assignment) for assignment in current_assignments]
        
    while True:
        all_neighbors = []
        for assignment in current_assignments:
            for var in pos:
                neighbor = assignment.copy()
                neighbor[var] = not neighbor[var]
                all_neighbors.append(neighbor)
            
        all_neighbors_scores = [(neighbor, heuristic_func(problem, neighbor)) for neighbor in all_neighbors]
        all_neighbors_scores.sort(key=lambda x: x[1], reverse=True)
            
        next_assignments = [neighbor for neighbor, score in all_neighbors_scores[:beam_width]]
        next_scores = [score for neighbor, score in all_neighbors_scores[:beam_width]]
        
        if max(next_scores) <= max(current_scores):
            break
            
        current_assignments = next_assignments
        current_scores = next_scores
        
    best_assignment = current_assignments[current_scores.index(max(current_scores))]
    best_score = max(current_scores)
        
    return best_assignment, best_score

def variable_neighborhood_descent(problem, pos, heuristic_func):
    def neighborhood_1(assignment):
        neighbors = []
        for var in pos:
            neighbor = assignment.copy()
            neighbor[var] = not neighbor[var]
            neighbors.append(neighbor)
        return neighbors

    def neighborhood_2(assignment):
        neighbors = []
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                neighbor = assignment.copy()
                neighbor[pos[i]] = not neighbor[pos[i]]
                neighbor[pos[j]] = not neighbor[pos[j]]
                neighbors.append(neighbor)
        return neighbors

    def neighborhood_3(assignment):
        neighbors = []
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                for k in range(j + 1, len(pos)):
                    neighbor = assignment.copy()
                    neighbor[pos[i]] = not neighbor[pos[i]]
                    neighbor[pos[j]] = not neighbor[pos[j]]
                    neighbor[pos[k]] = not neighbor[pos[k]]
                    neighbors.append(neighbor)
        return neighbors

    neighborhoods = [neighborhood_1, neighborhood_2, neighborhood_3]
    current_assignment = assign_values(pos)
    current_score = heuristic_func(problem, current_assignment)
    
    neighborhood_idx = 0
        
    while neighborhood_idx < len(neighborhoods):
        neighbors = neighborhoods[neighborhood_idx](current_assignment)
        neighbor_scores = [(neighbor, heuristic_func(problem, neighbor)) for neighbor in neighbors]
        next_assignment, next_score = max(neighbor_scores, key=lambda x: x[1])
        
        if next_score <= current_score:
            neighborhood_idx += 1
        else:
            current_assignment = next_assignment
            current_score = next_score
            neighborhood_idx = 0
            
    return current_assignment, current_score

def compare_algorithms(problem, pos):
    heuristics = [count_satisfied_clauses, weighted_clause_satisfaction]

    for heuristic in heuristics:
        print(f"Using heuristic: {heuristic.__name__}")
        
        hc_result, hc_score = hill_climbing(problem, pos, heuristic)
        hc_penetrance = penetrance(hc_score, len(problem))
        print(f"Hill Climbing: Score: {hc_score}, Penetrance: {hc_penetrance}")
        
        bs_result_3, bs_score_3 = beam_search(problem, pos, 3, heuristic)
        bs_penetrance_3 = penetrance(bs_score_3, len(problem))
        print(f"Beam Search (width 3): Score: {bs_score_3}, Penetrance: {bs_penetrance_3}")
        
        bs_result_4, bs_score_4 = beam_search(problem, pos, 4, heuristic)
        bs_penetrance_4 = penetrance(bs_score_4, len(problem))
        print(f"Beam Search (width 4): Score: {bs_score_4}, Penetrance: {bs_penetrance_4}")
        
        vnd_result, vnd_score = variable_neighborhood_descent(problem, pos, heuristic)
        vnd_penetrance = penetrance(vnd_score, len(problem))
        print(f"Variable Neighborhood Descent: Score: {vnd_score}, Penetrance: {vnd_penetrance}")

problems, pos = generate_clauses()
for problem in problems:
    print("Problem: ", problem)
    compare_algorithms(problem, pos)