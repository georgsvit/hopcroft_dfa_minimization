from manim import *

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



class AlgoScene(Scene):
    def construct(self):
        states_count, alphabet, state_transitions, final_states = read_data(FILE_NAME)

        self.visualize_general_data(states_count, alphabet, state_transitions, final_states, "Input DFA")    
        self.wait(5)        

        P, table = self.hopcroft(states_count, alphabet, state_transitions, final_states)

        new_final_states = update_final_states(P, final_states)

        self.clear()

        self.visualize_general_data(len(P), alphabet, table, new_final_states, "Minimized DFA")
        self.wait(5)        

    def visualize_general_data(self, states_count, alphabet, state_transitions, final_states, title):
        title = Title(title)
        alphabet_tex = Tex(r'Alphabet: ', ' '.join(alphabet)).align_on_border(LEFT).shift(UP * 2)
        states_tex = Tex(r'States count: ', str(states_count)).align_on_border(LEFT).shift(UP * 1.5)
        final_states_tex = Tex(r'Final states: ', ' '.join(str(x) for x in final_states)).align_on_border(LEFT).shift(UP * 1)
        transitions_table_tex = Tex(r'Transitions table:').align_on_border(LEFT).shift(UP * 0.5)

        self.add(title)
        self.play(Create(alphabet_tex))
        self.play(Create(states_tex))
        self.play(Create(final_states_tex))
        self.play(Create(transitions_table_tex))

        table, line = self.construct_custom_table(state_transitions, alphabet)        

    def construct_custom_table(self, data: list, alphabet: list):
        half_length = 0.6 * len(data)
        height = -1.6 + (0.4 * (len(alphabet) - 2))
        transitions = [list(range(len(data)))]

        for i in range(len(alphabet)):
            transitions.append(["-" if x[i] == -1 else x[i] for x in data])

        table = Matrix(transitions).shift(DOWN * 2)
        separate_line = Line((-half_length, height, 0), (half_length, height, 0))

        self.play(Create(table))
        self.play(Create(separate_line))

        return table, separate_line

    def display_step_input(self, m: Mobject, step_number: int):
        if step_number > 1:
            self.add(m)
        else:
            self.play(Create(m))

    def hopcroft_step(self, P: list, L: list, state_transitions: list, alphabet: list, step_number: int):
        C = L[0]
        L.remove(C)
        P1 = P.copy()

        self.clear()

        #       Title displaying
        self.add(Title(f"Step №{step_number}"))

        #       Alphabet displaying
        alphabet_group = VGroup(Tex(r'Alphabet: '))
        for char in alphabet:
            alphabet_group.add(Tex(f'{char}').next_to(alphabet_group[-1], RIGHT))
        alphabet_group.align_on_border(LEFT).shift(UP * 2)
        self.display_step_input(alphabet_group, step_number)

        #       P displaying
        P_group = VGroup(Tex(r'P: '))
        for state in P:
            P_group.add(Tex(f'{state}').next_to(P_group[-1], RIGHT))
        P_group.align_on_border(RIGHT).shift(UP * 2)
        self.play(Create(P_group))

        #       C displaying
        C_group = VGroup(Tex(r'C: '))
        for splitter in C:
            C_group.add(Tex(f'{splitter}').next_to(C_group[-1], RIGHT))
        C_group.align_on_border(LEFT).shift(UP * 1.2)
        self.play(Create(C_group))

        #       L displaying
        L_group = VGroup(Tex(r'L: '))
        if len(L) == 0:
            L_group.add(Tex(r'$\varnothing$').next_to(L_group[-1], RIGHT))
        for splitter in L:
            L_group.add(Tex(f'{splitter}').next_to(L_group[-1], RIGHT))
        L_group.align_on_border(RIGHT).shift(UP * 1.2)
        self.play(Create(L_group))

        #       Found states displaying
        states_group = VGroup(Tex(r'Found States: '))
        states_group.add(Tex(r'$\varnothing$').next_to(states_group[-1], RIGHT))
        states_group.align_on_border(LEFT).shift(UP * 0.4)
        self.play(Create(states_group))

        table, line = self.construct_custom_table(state_transitions, alphabet)

        print("Step start")
        print(f'C: {C}')
        print(f'L: {L}\n')

        #       Create letter frame
        letter_frame = SurroundingRectangle(alphabet_group[1])
        self.play(Create(letter_frame))

        #       Create frame for P Group
        P_frame = SurroundingRectangle(P_group[1])
        self.play(Create(P_frame))

        #       Create frame for table element
        table_frame = SurroundingRectangle(table[0][len(state_transitions)])
        self.play(Create(table_frame))

        for i in range(len(alphabet)):
            print(f'Letter:{alphabet[i]}')
            
            #       Change selected letter
            if i > 0:
                self.play(Transform(letter_frame, SurroundingRectangle(alphabet_group[i + 1])))            

            P_idx = 0
            for cls in P:
                states = []
                print(f'Class: {cls}')
            
                if P_idx > 0:
                    self.play(Transform(P_frame, SurroundingRectangle(P_group[P_idx + 1])))

                for j in range(len(state_transitions)):
                    self.play(Transform(table_frame, SurroundingRectangle(table[0][(i + 1) * len(state_transitions) + j])))
            
                    if state_transitions[j][i] in C and j in cls:
                        states.append(j)

                        self.play(table_frame.animate.set_color(RED))

                        #       Highlight splitter element
                        splitter_state_index = C.index(state_transitions[j][i])
                        splitter_frame = SurroundingRectangle(C_group[splitter_state_index + 1], color=RED)
                        self.play(Create(splitter_frame))

                        #       Change 'Found States Group' content 
                        if len(states) == 1:
                            self.play(Transform(states_group, VGroup(Tex(r'Found States: ')).align_on_border(LEFT).shift(UP * 0.4)))
                        self.play(states_group.animate.add(Tex(f'{j}').next_to(states_group[-1], RIGHT)))
                        
                        #       Disable splitter highlight
                        self.play(FadeOut(splitter_frame))                    
                        self.play(table_frame.animate.set_color(YELLOW))

                print(f'States: {states}')

                if len(states) > 0:            
                    B2 = states
                    B1 = [x for x in cls if x not in B2]

                    if cls in P1:

                        cls_idx = P1.index(cls)
                        P1.remove(cls)

                    if len(B1) > 0 and B1 not in P1:
                        P1.insert(cls_idx, B1)
                    if len(B2) > 0 and B2 not in P1:
                        P1.insert(cls_idx, B2)

                    #       Change P Group content 
                    temp_group = VGroup(Tex(r"P: "))
                    for state in P1:
                        temp_group.add(Tex(f'{state}').next_to(temp_group[-1], RIGHT))
                    temp_group.align_on_border(RIGHT).shift(UP * 2)
                    self.play(Transform(P_group, temp_group))

                    #       Change P frame
                    if len(P1) - len(P) == 1:
                        P_idx += 1

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

                    #       Change 'L Group' content 
                    temp_group = VGroup(Tex(r"L: "))
                    for state in L:
                        temp_group.add(Tex(f'{state}').next_to(temp_group[-1], RIGHT))
                    temp_group.align_on_border(RIGHT).shift(UP * 1.2)
                    self.play(Transform(L_group, temp_group))


                    if len(states) != 0:
                        #       Found states displaying
                        temp_group = VGroup(Tex(r'Found States: '))
                        temp_group.add(Tex(r'$\varnothing$').next_to(temp_group[-1], RIGHT))
                        temp_group.align_on_border(LEFT).shift(UP * 0.4)
                        self.play(Transform(states_group, temp_group))
                    
                P_idx += 1
            P = P1.copy()

            if i + 1 < len(alphabet):
                self.play(Transform(P_frame, SurroundingRectangle(P_group[1])))

            print(f'P1: {P1}')
            print(f'L: {L}\n')            
        print("Step end")
        self.play(FadeOut(table_frame))
        self.play(FadeOut(P_frame))
        self.play(FadeOut(letter_frame))
        
        return P1, L

    def hopcroft(self, states_count, alphabet, state_transitions, final_states):
        P = [[x for x in range(states_count) if x not in final_states], final_states]
        L = []

        if len(P[0]) < len(P[1]):
            L.append(P[0])
        else:
            L.append(P[1])

        counter = 1
        while len(L) > 0:
            P, L = self.hopcroft_step(P, L, state_transitions, alphabet, counter)
            L.sort(key= lambda x: len(x))
            counter += 1
            self.wait(2)

        new_state_transitions = form_transition_table(P, state_transitions, alphabet)

        return P, new_state_transitions