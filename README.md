# Visualization of the Hopcroft algorithm 
Visualization implemented on Python and [Manim Community Edition](https://www.manim.community/)

## **Setup and run**
To run this project, follow next steps:
1. Download project
2. Install Manim (and it's dependencies)
```
pip install manim
```
3.  Enter your DFA into data.txt in the next format
```
[symbols of alphabet]
[amount of terminate states]
[index numbers of terminate states]
[total amount of states]
[transition table for dfa]
```
Below is an example of DFA with:
  - alphabet - 'o', 'a', 'x'
  - three terminate states - 1, 2, 5;
```
o a x
3
1 2 5
6
1 3 4
5 -1 2
-1 -1 2
5 3 4
5 3 4
-1 -1 2
```
>Note: '-1' means no transition for this character from this state
4. Open terminal and go to the directory with project
5. Run next command to generate a visualization in video format (quality: 720p 30fps)
```
manim algo_visualize.py AlgoScene -pqm
```

## **Repository content**
- data.txt - file from which information about DFA is taken (contains example)
- algo_manim.py - script for manim visualization
- algo_text_min_output.py - script for minimal text visualization (only input DFA and minimized DFA will be displayed)
- algo_text_max_output.py - script for detailed text visualization (each step will be displayed)

## **Examples**
![Alt Text](examples/all_terminal_except_4.gif)
