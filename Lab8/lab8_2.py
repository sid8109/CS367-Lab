import numpy as np
from scipy.stats import poisson
n = 20
gamma = 0.9

# print("Here")
pr_rent1 = [poisson.pmf(i,3) for i in range(n)]
pr_rent2 = [poisson.pmf(i,4) for i in range(n)]
pr_ret1 = [poisson.pmf(i,3) for i in range(n)]
pr_ret2 = [poisson.pmf(i,2) for i in range(n)]

def transition(s1, s2, action):
    bikes1 = min(n, max(0, s1 - action))
    bikes2 = min(n, max(0, s2 + action))
    next_states = {}
    for rent1, p_rent1 in enumerate(pr_rent1):
        for rent2, p_rent2 in enumerate(pr_rent2):
            rented1 = min(bikes1, rent1)
            rented2 = min(bikes2, rent2)
            remaining1 = bikes1 - rented1
            remaining2 = bikes2 - rented2
            for ret1, p_ret1 in enumerate(pr_ret1):
                for ret2, p_ret2 in enumerate(pr_ret2):
                    bikes_after1 = min(n, remaining1 + ret1)
                    bikes_after2 = min(n, remaining2 + ret2)
                    prob = p_rent1 * p_rent2 * p_ret1 * p_ret2
                    next_state = (bikes_after1, bikes_after2)
                    next_states[next_state] = next_states.get(next_state, 0) + prob
    return next_states

states = [(s1, s2) for s1 in range(n+1) for s2 in range(n+1)]
optimal_policy = {(s1, s2): 0 for s1 in range(n+1) for s2 in range(n+1)}
optimal_value = {(s1, s2): 0 for s1 in range(n+1) for s2 in range(n+1)}

# print(len(states))


# print("Initialization")
for state in states:
    # print(state)
    s1,s2=state
    ac_min = max(-5, max(s2-20,-s1))
    ac_max = min(5, min(20-s1,s2))
    best_value = float('-inf')
    best_action = None
    for action in range(ac_min, ac_max+1):
        next_states = transition(s1, s2, action)
        action_value =0
        for next_state, prob in next_states.items():
            action_value += prob * (10*abs(action) + gamma * optimal_value[next_state])
        if action_value > best_value:
            best_value = action_value
            best_action = action
    optimal_policy[state] = best_action

# print("Training")
it=0
while True:
    # print(f"Iteration {it}")
    it+=1
    while True:
        diff = 0
        new_value = {}
        for state in states:
            s1, s2 = state
            action = optimal_policy[state]
            next_states = transition(s1, s2, action)
            total_value = 0
            for next_state, prob in next_states.items():
                total_value += prob * (10 * abs(action) + gamma * optimal_value[next_state])
            new_value[state] = total_value
            diff = max(diff,abs(new_value[state] - optimal_value[state]))
        optimal_value = new_value
        if diff<(1e-3):
            break

    f = True
    for state in states:
        s1, s2 = state
        best_action = None
        best_value = float('-inf')
        for action in range(-5, 6):
            if not (0 <= s1 - action <= n and 0 <= s2 + action <= n):
                continue
            next_states = transition(s1, s2, action)
            action_value =0
            for next_state, prob in next_states.items():
                action_value += prob * (10*abs(action) + gamma * optimal_value[next_state])
            if action_value > best_value:
                best_value = action_value
                best_action = action
        if optimal_policy[state] != best_action:
            f = False
        optimal_policy[state] = best_action
    if f:
        break


print("Optimal Policy:")
for s1 in range(n+1):
    for s2 in range(n+1):
        print(f"State ({s1}, {s2}): Move {optimal_policy[(s1, s2)]}")
