from .memory_n_agent import MemoryNAgent
import numpy as np
import json


class Agents():
  def __init__(self, file):
    data = json.load(file)
    agent_list = data["agents"]
    self.agents = []
    self.tournament = []
    print("Tournament configuration:")
    for agent in agent_list:
      print(f"\t{agent['name']}: {agent['count']}")
      self.agents.append(MemoryNAgent(agent['name'], agent['id'], agent['n'], agent['strategy']))
      for i in range(agent['count']):
        self.tournament.append(MemoryNAgent(agent['name'], agent['id'], agent['n'], agent['strategy']))

  def get_random_agent(self):
    agent = np.random.choice(self.agents)
    return agent

  def get_random_agent_in_tournament(self):
    agent = np.random.choice(self.tournament)
    return agent