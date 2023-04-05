import pygame
 
class Edge():
    def __init__(self, p0, p1, color):
        self.p0 = p0
        self.p1 = p1
        self.color = color
        self.length = ((p1.x - p0.x)**2 + (p1.y - p0.y)**2)**0.5
        self.isBroken = False

    def reset(self):
        self.isBroken = False

    def render_pos(self):
        if not self.isBroken:
            pygame.draw.line(
                pygame.display.get_surface(),
                self.color,
                (self.p0.x, self.p0.y),
                (self.p1.x, self.p1.y),
                width=1
            )
    
    def update(self):
        self.render_pos()
        