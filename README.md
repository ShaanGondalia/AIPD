# AIPD

This repository explores the behavioral evolution of NN agents in the prisoner's dilemma. Currently, it implements a two-stage process for playing against opponents. The first stage is an LSTM that is used to predict the strategy of the opponent. The second stage is a set of Q tables that are trained to play against each strategy independently.

## Usage

To train models on the agents defined in Agents.py, run:

```python main.py -t true -s <save_filename>```

To test the trained models in the tournament defined in Agents.py, run:

```python main.py -l <load_filename>```

## Agents

To create new agent types, new strategies, and new tournament configurations check the [Agent Documentation](agent/README.md). Note that whenever a new agent type or strategy is added to the AGENT_DICT, the model must be retrained (otherwise results are unknown). Also note that all agent types must have a different ID.