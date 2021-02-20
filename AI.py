from random import randint
from pygame.rect import Rect


class AIComponent:
    def __init__(self):
        self.state = None

    def update(self, pl):
        pass


class PatrolAI(AIComponent):
    def __init__(self, area: Rect):
        super().__init__()
        self.state = 'patrol'
        self.area = area
        self.destination = [randint(area.x, area.x + area.w), randint(area.y, area.y + area.h)]

    def update(self, pl):
        if hasattr(self, 'position') and hasattr(self, 'speed') and hasattr(self, 'velocity'):
            move = [self.speed, self.speed]

            if pl.rect.x > self.destination[0]:
                move[0] *= -1
            elif not self.position[0]:
                move[0] = 0

            if pl.rect.y > self.destination[1]:
                move[1] *= -1
            elif not self.position[1]:
                move[1] = 0

            self.velocity += move

            if not any(move):
                self.destination = [randint(self.area.x, self.area.x + self.area.w),
                                    randint(self.area.y, self.area.y + self.area.h)]

