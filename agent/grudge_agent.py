from .base_agent import BaseAgent

class GrudgeAgent(BaseAgent):
  def __init__(self, id):
    super().__init__(id)

  def update(self, val):
    if val == 1:
      self.val = 1
  
  def opt(self):
    if self.val == 0:
      return 0
    return 1