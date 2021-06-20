FILE_NAME = "data.txt"

def read_data(filename: str):
    file = open(filename, "r+")

    alphabet = file.readline().removesuffix("\n").split(' ')    

    n = int(file.readline().removesuffix("\n"))
    final_states = [int(x) for x in file.readline().removesuffix("\n").split(' ')]

    states_count = int(file.readline()) 
    state_transitions = []
    for _ in range(states_count):
        state_transitions.append([int(x) for x in file.readline().removesuffix("\n").split(' ')])
        
    file.close()
        
    return states_count, alphabet, state_transitions, final_states

def visualize_general_data(states_count, alphabet, state_transitions, final_states):
    print(f'States count: {states_count}')
    print(f'Alphabet: {" ".join(alphabet)}')

    print(f'Final States: {" ".join(str(x) for x in final_states)}')
    print("Transitions table")

    print("  " + " ".join(alphabet))
    for i in range(states_count):
        print(f'{i} {" ".join(str(x) for x in state_transitions[i])}')

def hopcroft_step(P: list, L: list, state_transitions: list, alpabet: list):
    C = L[0]
    L.remove(C)

    P1 = P.copy()

    for i in range(len(alpabet)):

        for cls in P:
            states = []
            
            for j in range(len(state_transitions)):
                if state_transitions[j][i] in C and j in cls:
                    states.append(j)

            if len(states) > 0:            
                B2 = states
                B1 = [x for x in cls if x not in B2]

                if cls in P1:
                    P1.remove(cls)

                if len(B1) > 0 and B1 not in P1:
                    P1.append(B1)
                if len(B2) > 0 and B2 not in P1:
                    P1.append(B2)        
                
                if cls in L:
                    L.remove(cls)
                    if len(B1) > 0:
                        L.append(B1)
                    if len(B2) > 0:
                        L.append(B2)
                else:
                    if len(B1) <= len(B2) and len(B1) > 0:
                        L.append(B1)
                    elif len(B1) > len(B2) and len(B2) > 0:
                        L.append(B2)            
     
        P = P1.copy()

    return P1, L

def find_state_index(P: list, transitions: list):
    for i, s in enumerate(P):
        if set(s).union(set(transitions)) == set(s):
            return i

def form_transition_table(P: list, state_transitions: list, alphabet: list):
    table = []

    for state in P:        
        row = []

        for i in range(len(alphabet)):
            transitions = [state_transitions[j][i] for j in state]        
            idx = find_state_index(P, transitions)
            row.append(idx if idx != None else "-")

        table.append(row)

    return table

def update_final_states(P: list, final_states: list):
    states = []

    for i, s in enumerate(P):
        if s[0] in final_states:
            states.append(i)
    
    return states

def hopcroft(states_count, alphabet, state_transitions, final_states):
    P = [[x for x in range(states_count) if x not in final_states], final_states]
    L = []

    if len(P[0]) < len(P[1]):
        L.append(P[0])
    else:
        L.append(P[1])

    counter = 1
    while len(L) > 0:
        P, L = hopcroft_step(P, L, state_transitions, alphabet)
        L.sort(key= lambda x: len(x))
        counter += 1

    print("\nMinimized:")
    print(f'P: {P}')

    new_state_transitions = form_transition_table(P, state_transitions, alphabet)

    return P, new_state_transitions

def main():
    states_count, alphabet, state_transitions, final_states = read_data(FILE_NAME)

    visualize_general_data(states_count, alphabet, state_transitions, final_states)

    P, table = hopcroft(states_count, alphabet, state_transitions, final_states)

    new_final_states = update_final_states(P, final_states)

    visualize_general_data(len(P), alphabet, table, new_final_states)


main()