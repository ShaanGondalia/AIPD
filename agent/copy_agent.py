from .base_agent import BaseAgent

class CopyAgent(BaseAgent):
  def __init__(self, id):
    super().__init__(id)
    self.val = 0

  def update(self, val):
    self.val = val

  def opt(self):
    return 0