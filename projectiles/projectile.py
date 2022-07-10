import math
import numpy as np
import pygame


class Projectile:
    def __init__(self, starting_x, starting_y):
        self.x = starting_x
        self.y = starting_y
        self.velocity = 2
        self.img = None
        self.angle = None
        self.tot_dis = 300
        self.dis_traveled = 0

    def projectile_target(self, balloon, path, path_index):
        t_index = path_index
        t_points = path
        s_pos = (self.x, self.y)
        b_speed = self.velocity
        t_pos_0 = (balloon.get_x(), balloon.get_y())
        t_vel = balloon.get_velocity()
        next_point = path[path_index + 1]
        time_0 = math.sqrt((next_point[0] - balloon.get_x()) ** 2 + (next_point[1] - balloon.get_y()) ** 2) / balloon.get_velocity()
        b_travel_dist_0 = b_speed * time_0
        ts_offset_0 = (t_pos_0[0] - s_pos[0], t_pos_0[1] - s_pos[1])

        while t_index + 1 < len(t_points):
            next_point = t_points[t_index + 1]
            t_vel = balloon.get_velocity()
            time_to_next_point = math.sqrt((next_point[0] - balloon.get_x()) ** 2 + (next_point[1] - balloon.get_y()) ** 2) / balloon.get_velocity()
            a = balloon.get_x_velocity() ** 2 + balloon.get_y_velocity() ** 2 - b_speed ** 2
            b = (2 * ts_offset_0[0] * balloon.get_x_velocity() + 2 * ts_offset_0[1] * balloon.get_y_velocity()) - 2 * b_travel_dist_0 * b_speed
            c = ts_offset_0[0] ** 2 + ts_offset_0[1] ** 2 - b_travel_dist_0 ** 2
            bb = b * b
            a2 = 2 * a
            ac4 = 4 * a * c
            if bb >= ac4:
                r = math.sqrt(bb - ac4)
                times = [(-b + r) / a2, (-b - r) / a2]

            time = np.inf
            for candidate_time in times:
                if candidate_time < 0.0:
                    continue

                if candidate_time < time:
                    time = candidate_time

            if not np.isinf(time):
                if time <= time_to_next_point:
                    point_to_aim = (t_pos_0[0] + balloon.get_x_velocity() * time, t_pos_0[1] + balloon.get_y_velocity() * time)
                    changex = point_to_aim[0] - self.x
                    changey = point_to_aim[1] - self.y
                    self.angle = math.atan2(changey, changex)
                    return None
            time_0 += time_to_next_point
            t_pos_0 = next_point
            t_index += 1

    def show_dis(self, balloon):
        return math.sqrt(
            (balloon.get_x() - self.x) ** 2 + (balloon.get_y() - self.y) ** 2
        )

    def move_projectile(self):
        if self.angle != None:
            self.x += math.cos(self.angle) * self.velocity
            self.y += math.sin(self.angle) * self.velocity
            self.dis_traveled += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, "BLACK", (self.x, self.y), 5)
        self.move_projectile()

    def projectile_dead(self):
        if self.dis_traveled >= self.tot_dis:
            return True
        return False