from .cooperate_agent import CooperateAgent
from .copy_agent import CopyAgent
from .defect_agent import DefectAgent
from .grudge_agent import GrudgeAgent
import numpy as np

class Agents():
  def __init__(self):
    self.agents = [CooperateAgent(), DefectAgent(), CopyAgent(), GrudgeAgent()]

  def get_random_agent(self):
    agent = np.random.choice(self.agents)
    return agent

  def reset_all_agents(self):
    for agent in self.agents:
        agent.reset()

