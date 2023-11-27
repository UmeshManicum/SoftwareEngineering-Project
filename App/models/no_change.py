from App.models import state
from .state import *

class NoChange(State):
    __tablename__='no_change'

    def __init__(self, ranking):
        self.ranking = ranking

    def notify(self):
        return None
        #return("No Change State")

    def update_state(self):
        if self.ranking.curr_ranking != self.ranking.prev_ranking:
            self.ranking.state = self.ranking.change_state
            return self.ranking.state