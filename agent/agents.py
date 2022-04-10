from .memory_n_agent import MemoryNAgent
import numpy as np
import json


class Agents():
  def __init__(self, file):
    data = json.load(file)
    agent_list = data["agents"]
    self.agents = []
    self.tournament = []
    for agent in agent_list:
      self.agents.append(MemoryNAgent(agent['id'], agent['n'], agent['strategy']))
      for i in range(agent['count']):
        self.tournament.append(MemoryNAgent(agent['id'], agent['n'], agent['strategy']))
    print(self.tournament)

  def get_random_agent(self):
    agent = np.random.choice(self.agents)
    return agent

  def get_random_agent_in_tournament(self):
    agent = np.random.choice(self.tournament)
    return agent