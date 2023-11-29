from App.models import state
from .state import *

class Change(State):
    __tablename__='change'

    def __init__(self, ranking):
        self.ranking = ranking
  
    def notify(self):
        self.ranking.prev_ranking = self.ranking.curr_ranking
        self.ranking.update_state()
        return self.ranking
        #return("Change State")

    def update_state(self):
        #if self.ranking.curr_ranking == self.ranking.prev_ranking:
        self.ranking.state = self.ranking.no_change_state
        return self.ranking.state