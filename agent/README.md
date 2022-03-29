# Agents


## Types of Agents
Agents can be defined by extension of the BaseAgent, found in ```base_agent.py```. Strategies can be arbitrarily complex, as long as the correct methods of BaseAgent are overloaded. We provide a tool for defining a generic agent that remembers N moves, called MemoryNAgent, found in ```memory_n_agent.py```.

## Defining Agents in the Game

`agents.py` serves two purposes. First, it lists the strategies of each **type** of agent that exists in this game. Secondly, it provides the **count** of each type of agent found in the tournament. For instance, the user may create 4 different types of agents, but can set up a tournament that contains 3 of each type of agent, totaling to 12 agents in the tournament. 

This distinction between the types of agents and the tournament of agents is important, as the LSTM and Q-Tables are only trained to recognize types of agents, not individual instances of each type. This way, we can set up very large tournaments without increasing the training time of the models too much.

To edit the strategies, available types, and counts of agents the user must edit ```AGENT_DICT``` inside of `agents.py`. In the future, this dictionary may get switched to a configuration file instead of python code.

## Defining Strategy for MemoryNAgent

An agent that has N rounds of memory must receive a list of 4^N entries as a parameter. These 4^N entries define what move the agent makes based on the previous N opponent and self moves. We can define the sequence of opponent and self moves as a sequence of 0s and 1s. See, for instance, the case where N = 1:

1. 0 0: Self cooperates, Opponent cooperates
1. 0 1: Self cooperates, Opponent defects
1. 1 0: Self defects, Opponent cooperates
1. 1 1: Self defects, Opponent defects

The decimal representations of this sequence are used as the indices of the strategy vector. For instance index 0 corresponds to case 1 (00), index 2 corresponds to case 3 (10), etc. The entry at each element of the strategy vector is a 0 or 1 corresponding to whether the agent cooperates or defects given the history of moves. For instance, to define a copycat agent, we can write:

* strategy[0] = 0 (cooperate if 0 0)
* strategy[1] = 1 (defect if 0 1)
* strategy[2] = 0 (cooperate if 1 0)
* strategy[3] = 1 (defect if 1 1 )

In the case where N > 1, this definition gets a little more complex. Note that the sequence of moves is 2N total bits. We define the first N bit word as the self moves, and the second N bit word as the opponents moves. The leftmost bit of these N-bit words is the "oldest" move, and the rightmost bit of the word is the "newest" move. So, the sequence now looks like:

(Oldest Self Move, ..., Newest Self Move) (Oldest Opponent Move, ..., Newest Opponent Move). The indexing is the same, so the strategy at index 6 should be what the agent does in the case of 0110. 0110 in human terms is:

* 2 rounds ago I cooperated and the opponent defected
* Last round I defected and the opponent cooperated

Because the list of possible states grows exponentially (4^N), we recommend limiting strategies to N=2.