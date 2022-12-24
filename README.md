# AIPD

This repository explores the behavioral evolution of NN agents in the prisoner's dilemma. Currently, it implements a two-stage process for playing against opponents. The first stage is an LSTM that is used to predict the strategy of the opponent. The second stage is a set of Q tables that are trained to play against each strategy independently.

## Usage
To visualize our results locally, navigate to the `frontend` directory in your cloned repository and run:

```bash
npm install
npm start
```

This will start our application at `http://localhost:3000`, which can be viewed in your browser.

### Training
To train all models on an agent configuration, run:

```python main.py -a <path_to_agent_config> -t -s <save_filename>```

To train only the q_table/lstm run:

```python main.py -a <path_to_agent_config> -t -s <save_filename> -m qtable```

```python main.py -a <path_to_agent_config> -t -s <save_filename> -m lstm```

### Evaluation
To evaluate the performance of the trained models, run:

```python main.py -a <path_to_agent_config> -l <load_filename>```

To run and visualize a tournament, run:

```python main.py -a <path_to_agent_config> -r -n <save_filename> -v```

To save visualizations for any command (if possible), add `-v` to the command.


## Agents

To create new agent types, new strategies, and new tournament configurations check the [Agent Documentation](agent/README.md). Note that whenever a new agent type or strategy is added to the AGENT_DICT, the model must be retrained (otherwise results are unknown). Also note that all agent types must have a different ID.

## Hyper-Parameters

All Model hyper-parameters are kept in the params.py file.
