from .base_agent import BaseAgent

class DefectAgent(BaseAgent):
  def __init__(self, id):
    super().__init__(id)
    self.val = 1
  
  def opt(self):
    return 1

  def reset(self):
    self.val = 1
