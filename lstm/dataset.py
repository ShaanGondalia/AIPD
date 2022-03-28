import numpy as np
import itertools
import random
from torch.utils.data import Dataset, DataLoader
from .hyper_parameters import *

class PreTrainDataset(Dataset):

  def __init__(self, agents):
    self.generate_data(agents)

  def __getitem__(self, idx):
    item = self.data[idx]
    nn_moves = item["NN"]
    agent_moves = item["AGENT"]
    agent_id = item["ID"]
    combined_moves = np.vstack([nn_moves,agent_moves]).T

    return {
        "input" : combined_moves,
        "output" : agent_id
    }

  def generate_data(self, agents):
      d = np.array([seq for seq in itertools.product([0,1], repeat=ROUNDS)])
      movesets = random.sample(list(d), SAMPLE)
      self.data = []

      for agent in agents.agents:
          for moveset in tqdm(movesets):
              agent_moves = []
              for move in moveset:
                  agent_moves.append(agent.play())
                  agent.update(move)
              self.data.append({
                  "NN" : moveset,
                  "AGENT" : agent_moves,
                  "ID" : agent.id()
              })
              agent.reset()

      random.shuffle(self.data)

  def __len__(self):
    return len(self.data)