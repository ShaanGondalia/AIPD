from .memory_n_agent import MemoryNAgent
from .ai_agent import AIAgent
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
      if agent['type'] == 'memory':
        self.agents.append(MemoryNAgent(agent['name'], agent['id'], agent['n'], agent['strategy']))
        for i in range(agent['count']):
          self.tournament.append(MemoryNAgent(agent['name'], agent['id'], agent['n'], agent['strategy']))
      elif agent['type'] == 'ai':
        # self.agents.append(AIAgent(agent['name'], agent['id'], agent['dimensions'], agent['file']))
        for i in range(agent['count']):
          self.tournament.append(AIAgent(agent['name'], agent['id'], agent['dimensions'], agent['file']))

  def get_random_agent(self):
    agent = np.random.choice(self.agents)
    return agent

  def get_random_agent_in_tournament(self):
    agent = np.random.choice(self.tournament)
    return agent