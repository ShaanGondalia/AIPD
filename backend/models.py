from lstm.lstm import LSTM
import torch
import torch.nn as nn
import numpy as np
import pickle

LSTM_HIDDEN = 200
LSTM_LAYERS = 4
IN = 2
OUT = 2
NUM_AGENTS = 4
DEVICE = 'cpu'

class MiniAgent:
    
    def __init__(self, load_fname):
        self.lstm = LSTM(IN, LSTM_HIDDEN, OUT, NUM_AGENTS, LSTM_LAYERS, DEVICE)
        self.load(load_fname)
        
    def load(self, fname):
        print(f"Loading Models from file: {fname}")
        self.lstm.load(fname)
        with open(f'saved/{fname}.pickle', 'rb') as handle:
            self.q_agents = pickle.load(handle)
        for i in range(NUM_AGENTS):
            self.q_agents[i].set_epsilon(-1)

    def action(self, agent_moves, opponent_moves):
        combined_moves = np.vstack([agent_moves, opponent_moves]).T
        input = torch.Tensor(combined_moves).type(torch.FloatTensor).to('cpu').unsqueeze(0)
        pred_id, _ = self.lstm.predict_id(input) 
        q_agent = self.q_agents[pred_id]
        action = q_agent.pick_action(combined_moves, False)
        return action



    


    


    