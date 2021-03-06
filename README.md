# Block-World-Planner

Planning actions for the block world problem

In this repository, I have implemented the following planners designed or the blocks world problem:

- Forward (progression) planner using breadth first search
- Forward (progression) planner using A* search
- Goal Stack planner

## Block World Problem
The blocks world is described as follows:
There are N blocks, table and a robotic arm. Blocks are identified by integers 1 to N. Each block
can sit on top of another block or on the table. There can be a stack of blocks of arbitrary height.
However only one block can be directly on another block. No two blocks can be sitting directly
on the same block. The bottom most block of a stack must be on the table. The table can hold
any number of blocks. If there is no block on top of a block, then the block is clear. The robotic
arm can hold only one block. If the robotic arm does not hold any block, it is empty.

### Propositions
The propositions for this problem are as follows:
```
(on blocka blocka) – meaning blocka is stacked on blockb
(ontable block)
(clear block)
(hold block)
(empty)
```

### Actions
There are 4 actions specified using the following schemas:
```
action(pick block)
preconditions – (ontable block) (clear block) (empty)
effects – (hold block) ~(clear block) ~(empty) ~(ontable block)
```
```
action(unstack blocka blockb)
preconditions – (on blocka blockb) (clear blocka) (empty)
effects – (hold blocka) clear(blockb) ~(on blocka blockb) ~(empty) ~(clear blocka)
```
```
action(release block)
preconditions – (hold block)
effects – (ontable block) (clear block) (empty) ~(hold block)
```
```
action(stack blocka blockb)
preconditions – clear(blockb) (hold blocka)
effects – (on blocka blockb) (clear blocka) (empty) ~(hold blocka) ~(clear blockb)
```

A state will be specified as a list of propositions that hold good in that state separated by a space in a single
line. For example, in a 3-blocks world, a state can be (on 1 2) (clear 1) (ontable 3) (ontable 2)
(clear 3) (empty).

Given a text file containing the initial and goal state description, and the choice of the planning
approach, this code outputs a file containing the plan from the initial state the goal
state. You have define a good heuristic for performing A* search based forward planner.


### Input
The input to code will be the name of the text file a description of the initial and goal states
along with the planning approach that has to be used. Specifically, the format of the input file is
as follows
```
N
planner
initial
2	
State description
goal
State description
```
The first line is the number of blocks in the blocks world. The second line indicates the choice of
the planner (f-forward planner with BFS, a- forward planner A* search and g- goal stack
planner). The third line indicates that the line following it contains the complete description of the
initial state. This is followed by the line containing the term goal. This is in turn followed by the
line that completely describes the goal state.

### Output
Code output to a text file the plan specified in the following format
```
NA
Action 1
Action 2
...
Action NA
```
The first line indicates the number of actions in the plan. Each line then presents the action that
has to be taken.

### Executing the code


  python l4.py file.txt

where,

file.txt contains the number of blocks, initial state, goal state

The output actions to reach the goal state is printed in "output.txt"

Further implementation details and observations are included in .pdf file.
