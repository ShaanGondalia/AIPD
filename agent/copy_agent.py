from .base_agent import BaseAgent

class CopyAgent(BaseAgent):
  def __init__(self):
    super().__init__(2)
    self.prev_val = 0
    self.val = 0

  def update(self, val):
    self.val = val

  def opt(self):
    return 0