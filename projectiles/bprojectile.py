from cmath import sqrt
from projectiles.projectile import Projectile
import numpy, math
import pygame

class Boomerang(Projectile):
    def __init__(self, starting_x, starting_y):
        super().__init__(starting_x, starting_y)
        self.durability = 5
        self.tot_dis = 400
        self.dist_toTravel = []

    def projectile_target(self, balloon, path, path_index, delta_time):
        rangeBX = balloon.get_x()
        rangeBY = balloon.get_y()
        diffX = rangeBX - self.x
        diffY = rangeBY - self.y
        run = True
        count = 0
        while run:

            count += 1

            if (count * self.velocity * delta_time) ** 2 >= diffX**2 + diffY**2:
                run = False
                diffX += balloon.get_x_velocity() * delta_time
                diffY += balloon.get_y_velocity() * delta_time
                tempX = rangeBX + balloon.get_x_velocity() * (count) * delta_time
                tempY = rangeBY + balloon.get_y_velocity() * (count) * delta_time
                if self.inCheck(
                    path[path_index][0],
                    path[path_index][1],
                    path[path_index + 1][0],
                    path[path_index + 1][1],
                    tempX,
                    tempY,
                ):
                    self.angle = math.atan2(diffY, diffX)
                    self.img = pygame.transform.rotozoom(
                        self.img, -math.degrees(self.angle), 1
                    )
                    self.mask = pygame.mask.from_surface(self.img)
                    self.dist_toTravel = [diffX, diffY]
                    return True

                else:
                    return False

            diffX += balloon.get_x_velocity() * delta_time
            diffY += balloon.get_y_velocity() * delta_time
            if count >= 100:
                run = False
                self.angle = 0


    def getAngles(self,first_angle):
        tot_travel = sqrt(self.dist_toTravel[0]**2 + self.dist_toTravel[1]**2)
        one_way = self.tot_dis/2 -tot_travel
        min_val = min(self.dist_toTravel[0],self.dist_toTravel[1])
        s_sq = one_way ** 2 - min_val**2
        return math.atan2(min_val, sqrt(s_sq))

    def move_projectile(self, delta_time):
        angles = []
        if self.angle != None:
            angles.append(self.angle)
            z = self.getAngles(self.angle)
            angles.append(z)
            angles.append(z)
            angles.append(self.angle)
            for i in range(len(angles)):
                a = angles[i]
                if i <= 1:
                    self.x += math.cos(a) * self.velocity * delta_time
                    self.y += math.sin(a) * self.velocity * delta_time
                    self.dis_traveled += self.velocity * delta_time
                else:
                    self.x += math.cos(a) * self.velocity * delta_time
                    self.y += math.sin(a) * self.velocity * delta_time
                    self.dis_traveled += self.velocity * delta_time
