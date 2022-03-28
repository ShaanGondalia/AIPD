from .base_agent import BaseAgent

class DefectAgent(BaseAgent):
  def __init__(self):
    super().__init__(1)
    self.val = 1
  
  def opt(self):
    return 1

  def reset(self):
    self.val = 1
