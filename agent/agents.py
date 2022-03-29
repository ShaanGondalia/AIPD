from .memory_n_agent import MemoryNAgent
import numpy as np


AGENT_DICT = {
  "Cooperate": {
    "id": 0,
    "count": 2,
    "n": 1,
    "strategy": [0, 0, 0, 0]
  },
  "Defect": {
    "id": 1,
    "count": 1,
    "n": 1,
    "strategy": [1, 1, 1, 1]
  },
  "Copy": {
    "id": 2,
    "count": 3,
    "n": 1,
    "strategy": [0, 1, 0, 1]
  },
  "Generic": {
    "id": 3,
    "count": 1,
    "n": 1,
    "strategy": [1, 0, 0, 1]
  },
}


class Agents():
  def __init__(self):
    self.agents = []
    self.tournament = []
    for agent in AGENT_DICT:
      self.agents.append(MemoryNAgent(AGENT_DICT[agent]['id'], AGENT_DICT[agent]['n'], AGENT_DICT[agent]['strategy']))
      for i in range(AGENT_DICT[agent]['count']):
        self.tournament.append(MemoryNAgent(AGENT_DICT[agent]['id'], AGENT_DICT[agent]['n'], AGENT_DICT[agent]['strategy']))

  def get_random_agent(self):
    agent = np.random.choice(self.agents)
    return agent

  def get_random_agent_in_tournament(self):
    agent = np.random.choice(self.tournament)
    return agent