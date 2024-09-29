from string import ascii_lowercase
from itertools import combinations
import random

print("Enter the number of clauses: ")
m = int(input())
print("Enter the number of variables: ")
n = int(input())
print("Enter the number of variables in each clause: ")
k = int(input())

def generate_clauses():
    limit = 10 
    problems = []
    pos = list(ascii_lowercase)[:n]
    neg = [x.upper() for x in pos]
    total_var = pos + neg    
    all_clauses = list(combinations(total_var, k))
    
    if len(all_clauses) < m:
        print(f"Error: Not enough unique clauses to generate {m} clauses.")
        return [], pos
    
    for _ in range(limit):
        p = random.sample(all_clauses, m)
        if p not in problems:
            problems.append(p) 
    
    return problems, pos

problems, pos = generate_clauses() 

if problems:
    for i in range(len(problems)):
        print(f"Problem {i + 1}: {problems[i]}")
