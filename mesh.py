from random import randint, random
import pygame
from point import Point
from edge import Edge
import numpy as np

class ClothMesh():
    def __init__(self, topLeft, size):
        super().__init__()
        self.topLeft = topLeft
        self.size = size
        self.spacing = 20
        self.points = []
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                object = Point((
                    topLeft[0] + i * self.spacing,
                    topLeft[1] + j * self.spacing
                    ),
                    100,
                    (255, 255, 255)
                )
                is_fixed = False
                if i == 0 and j == 0:
                    is_fixed = True
                elif i == round(size[0]*0.25) and j == 0:
                    is_fixed = True
                elif i == round(size[0]*0.5) and j == 0:
                    is_fixed = True
                elif i == round(size[0]*0.75) and j == 0:
                    is_fixed = True
                elif i == size[0] - 1 and j == 0:
                    is_fixed = True
                self.points.append(object)
                self.points[-1].isFixed = is_fixed
        
        self.edges = []
        for i in range(0, size[0] - 1):
            for j in range(0, size[1] - 1):
                p0 = self.points[i + j * size[0]]
                p1 = self.points[i + 1 + j * size[0]]
                edge = Edge(p0, p1, (255, 255, 255))
                self.edges.append(edge)
                
                p0 = self.points[i + j * size[0]]
                p1 = self.points[i + (j + 1) * size[0]]
                edge = Edge(p0, p1, (255, 255, 255))
                self.edges.append(edge)
        for i in range(0, size[0] - 1):
            p0 = self.points[i + (size[1] - 1) * size[0]]
            p1 = self.points[i + 1 + (size[1] - 1) * size[0]]
            edge = Edge(p0, p1, (255, 255, 255))
            self.edges.append(edge)
        for j in range(0, size[1] - 1):
            p0 = self.points[(size[0] - 1) + j * size[0]]
            p1 = self.points[(size[0] - 1) + (j + 1) * size[0]]
            edge = Edge(p0, p1, (255, 255, 255))
            self.edges.append(edge)
        
        self.bounce = 0.9
        self.gravity = 0.5
        self.friction = 0.995

        self.prevMousePos = pygame.mouse.get_pos()
        self.currMousePos = self.prevMousePos
        self.isMouseDown = False

    def reset(self):
        for point in self.points:
            point.reset_pos()
        for edge in self.edges:
            edge.reset()

    def is_intersecting(self, mouse_x, mouse_y, x1, y1, x2, y2):
        # Calculate the direction of the ray
        ray_dx = mouse_x - x1
        ray_dy = mouse_y - y1
        
        # Calculate the direction of the line
        line_dx = x2 - x1
        line_dy = y2 - y1
        
        # Check if the ray and line are parallel
        if ray_dx * line_dy == ray_dy * line_dx:
            return False
        
        # Calculate the t parameter of the intersection point
        t = (ray_dx * (y1 - mouse_y) + ray_dy * (mouse_x - x1)) / (line_dx * ray_dy - line_dy * ray_dx)
        
        # Check if the t value is within the valid range
        if t < 0 or t > 1:
            return False
        
        # Calculate the coordinates of the intersection point
        intersection_x = x1 + t * line_dx
        intersection_y = y1 + t * line_dy

        if abs(intersection_x-mouse_x) < self.spacing * 0.7 and abs(intersection_y-mouse_y) < self.spacing * 0.7:
            return True
        
        return False

    def update_points(self):
        points_not_fixed = [point for point in self.points if not point.isFixed and not point.isDead]
        vxs = [point.x - point.old_pos[0] for point in points_not_fixed]
        vys = [point.y - point.old_pos[1] for point in points_not_fixed]
        for i, point in enumerate(points_not_fixed):
            point.old_pos[0] = point.x
            point.old_pos[1] = point.y
            point.x += vxs[i] * self.friction
            point.y += (vys[i] * self.friction) + self.gravity

    def constrain_points(self):
        max_x = pygame.display.Info().current_w
        max_y = pygame.display.Info().current_h
        min_x = 0
        min_y = 0
        for point in self.points:
            if not point.isFixed and not point.isDead:
                vx = (point.x - point.old_pos[0]) * self.friction
                vy = (point.y - point.old_pos[1]) * self.friction

                if point.x > max_x:
                    point.x = max_x
                    point.old_pos[0] = point.x + vx * self.bounce
                    # point.isDead = True
                elif point.x < min_x:
                    point.x = min_x
                    point.old_pos[0] = point.x + vx * self.bounce
                    # point.isDead = True
                if point.y > max_y:
                    point.y = max_y
                    point.old_pos[1] = point.y + vy * self.bounce
                    # point.isDead = True
                elif point.y < min_y:
                    point.y = min_y
                    point.old_pos[1] = point.y + vy * self.bounce

    def update_edges(self):
        for edge in self.edges:
            if not edge.isBroken and not (edge.p0.isDead and edge.p1.isDead):
                self.currMousePos = pygame.mouse.get_pos()
                p1 = self.currMousePos
                p2 = self.prevMousePos
                p3 = (edge.p0.x , edge.p0.y)
                p4 = (edge.p1.x , edge.p1.y)
                result = self.is_intersecting(p1[0], p1[1], edge.p0.x , edge.p0.y, edge.p1.x , edge.p1.y)
                self.prevMousePos = self.currMousePos
                if result and self.isMouseDown:
                    # print(result)
                    edge.isBroken = True

                dx = edge.p1.x - edge.p0.x
                dy = edge.p1.y - edge.p0.y
                distance = (dx * dx + dy * dy)**0.5
                difference = edge.length - distance
                percent = difference / distance / 2
                offsetX = dx * percent
                offsetY = dy * percent

                if not edge.p0.isFixed:
                    edge.p0.x -= offsetX
                    edge.p0.y -= offsetY
                if not edge.p1.isFixed:
                    edge.p1.x += offsetX
                    edge.p1.y += offsetY
    
    def render_points(self):
        for point in self.points:
            point.render_pos()
    
    def render_edges(self):
        for edge in self.edges:
            edge.render_pos()
    
    def update(self):
        self.update_points()
        for i in range(0, 8):
            self.update_edges()
            self.constrain_points()
        self.render_points()
        self.render_edges()
