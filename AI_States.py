import numpy as np
from Move import Move


class AI_states:

    def __init__(self, current, white_turn,score,move):
        self.current = current
        self.white_turn = white_turn
        self.score = score
        self.next_move=move

    def __eq__(self, o: object) -> bool:
        if type(self) != type(o):
            return False
        elif self.current != o.current:
            return False
        elif self.white_turn != o.white_turn:
            return False
        return True

    def __hash__(self) -> int:
        return hash(self.current)*self.white_turn