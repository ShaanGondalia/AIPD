import numpy as np
import itertools
import random
from torch.utils.data import Dataset, DataLoader
import hyper_parameters as hp

class PreTrainDataset(Dataset):

  def __init__(self):
    self.generate_data()

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

  def generate_data(self):
      d = np.array([seq for seq in itertools.product([0,1], repeat=hp.ROUNDS)])

      #Generate Dataset for All Existing Moves
      cooperate = np.array([0 for i in range(hp.ROUNDS)])
      defect = np.array([1 for i in range(hp.ROUNDS)])

      movesets = random.sample(list(d), hp.SAMPLE)
      self.data = []
      for moveset in movesets:
          self.data.append({
              "NN" : moveset,
              "AGENT" : cooperate,
              "ID" : 0
          })
          self.data.append({
              "NN" : moveset,
              "AGENT" : defect,
              "ID" : 1
          })
          copy_moveset = [0]
          copy_moveset.extend(moveset[1:])
          copy_moveset = np.array(copy_moveset)
          self.data.append({
              "NN": moveset,
              "AGENT" : copy_moveset,
              "ID" : 2
          })
          first_cheat = np.where(moveset[0] == 1)[0]
          if len(first_cheat) > 0:
              grudge_moveset = np.array([0 if i < first_cheat else 1 for i in range(hp.ROUNDS)])
          else:
              grudge_moveset = cooperate
          self.data.append({
              "NN" : moveset,
              "AGENT" : grudge_moveset,
              "ID" : 3
          })

      random.shuffle(self.data)

  def __len__(self):
    return len(self.data)