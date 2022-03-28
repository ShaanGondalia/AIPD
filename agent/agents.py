from .memory_n_agent import MemoryNAgent
import numpy as np


AGENT_DICT = {
  "Cooperate": {
    "n": 1,
    "strategy": [0, 0, 0, 0]
  },
  "Defect": {
    "n": 1,
    "strategy": [1, 1, 1, 1]
  },
  "Copy": {
    "n": 1,
    "strategy": [0, 1, 0, 1]
  },
  "Generic": {
    "n": 1,
    "strategy": [1, 0, 0, 1]
  },
}


class Agents():
  def __init__(self):
    i = 0
    self.agents = []
    for agent in AGENT_DICT:
      self.agents.append(MemoryNAgent(i, AGENT_DICT[agent]['n'], AGENT_DICT[agent]['strategy']))
      i+=1

  def get_random_agent(self):
    agent = np.random.choice(self.agents)
    return agent
