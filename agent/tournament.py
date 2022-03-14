from .cooperate_agent import CooperateAgent
from .copy_agent import CopyAgent
from .defect_agent import DefectAgent
from .grudge_agent import GrudgeAgent
import numpy as np

class Tournament():
  def __init__(self):
    self.agents = [CooperateAgent(), DefectAgent(), CopyAgent(), GrudgeAgent()]

  def get_random_agent():
    agent = np.random.choice(agents)
    return agent

