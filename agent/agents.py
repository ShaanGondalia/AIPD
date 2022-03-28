from .cooperate_agent import CooperateAgent
from .copy_agent import CopyAgent
from .defect_agent import DefectAgent
from .grudge_agent import GrudgeAgent
from .memory_n_agent import MemoryNAgent
import numpy as np


MEMORY_AGENT_MOVES = [0, 1, 0, 1] #CC:C, CD:D, DC:C, DD:D

class Agents():
  def __init__(self):
    self.agents = [CooperateAgent(0), DefectAgent(1), CopyAgent(2), MemoryNAgent(3, 1, MEMORY_AGENT_MOVES)]

  def get_random_agent(self):
    agent = np.random.choice(self.agents)
    return agent
