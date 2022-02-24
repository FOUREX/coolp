import pygame as pg
import time
import math
from random import randint, choice


WINDOW = W_WIDTH, W_HEIGHT = 800, 650
CENTER = HALF_W, HALF_H = W_WIDTH // 2, W_HEIGHT // 2
METER = 30 # 30 пикселей == 1 метер
GROUND = 630
FPS = 60
DEBUG = False
gravity = (math.pi, 0.0024)


def set_fall_height(height):
    global METER
    METER = int((18 / 30) * height)


user_events = {
    "start_simulation": False,
    "stop_simulation": False
}


pg.font.init()
font = pg.font.SysFont("ubuntu", 16)


def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)


def round(x, y):
    try:
        z = str(x).split(".")
        return f"{z[0]}.{z[1][:y]}"
    except:
        return x


class Dot:
    def __init__(self) -> None:
        self.simulation = False

        self.color = (255, 0, 0)
        self.radius = 10

        self.fall_time_0 = 0
        self.fall_time = 0
        self.fall_distance = 0

        self.angle = math.pi
        
        self.mass = 75
        self.energy = 0
        self.spd = 0

        self.start_pos = self.start_x, self.start_y = HALF_W / 2, 90
        self.x, self.y = self.start_pos


    @property
    def pos(self):
        return self.x, self.y

    @property
    def speed(self):
        return self.spd * 2.120932


    def move(self):
        if self.simulation is True:
            if self.y < GROUND:
                self.x += math.sin(self.angle) * self.spd * METER
                self.y -= math.cos(self.angle) * self.spd * METER


                self.angle, self.spd = addVectors(self.angle, self.spd, gravity[0], gravity[1])

                self.fall_time = time.time() - self.fall_time_0
                self.fall_distance = (self.y - self.start_y) / METER
            else:
                self.simulation = False

    
    def update(self):
        def stop():
            self.simulation = False
            self.x, self.y = self.start_pos
            self.fall_time_0 = 0
            self.fall_time = 0
            self.fall_distance = 0
            self.energy = 0
            self.spd = 0
            user_events.update({"stop_simulation": False})
        
        def start():
            self.fall_time_0 = time.time()
            self.simulation = True
            user_events.update({"start_simulation": False})

        self.energy = self.mass * math.sqrt(2 * self.fall_distance * 9.8)
        if user_events["start_simulation"] is True and self.simulation is False:
            if self.y >= GROUND:
                stop()
            start()
        if user_events["stop_simulation"] is True:
            stop()

"""
class Dot:
    def __init__(self, app):
        self.app = app
        self.sc = self.app.sc
        self.simulation = False

        self.start_x, self.start_y = HALF_W // 2, 90
        self.x, self.y = self.start_x, self.start_y

        self.speed = 0
        self.mass = 100

        self.fall_time_0 = 0
        self.fall_time = 0
        self.fall_distance = 0

        self.radius = self.mass * 0.125
        self.color = (255, 0, 0)
        

    @property
    def pos(self):
        return self.x, self.y

    
    def update(self):
        if user_events["start_simulation"] is True and self.simulation is False:
            self.simulation = True
            self.fall_time_0 = time.time()
            user_events.update({"start_simulation": False})
        if user_events["stop_simulation"] is True and self.simulation is True:
            self.simulation = False
            self.x, self.y = self.start_x, self.start_y
            self.speed = 0
            self.fall_time_0 = 0
            self.fall_time = 0
            self.fall_distance = 0
            user_events.update({"stop_simulation": False})


    def physics(self):
        if self.simulation == True:
            if self.y < GROUND:
                self.fall_time_1 = time.time()
                self.fall_time = self.fall_time_1 - self.fall_time_0


                self.speed += g
                self.y += self.speed / METER


                ""\"
                self.fall_time_1 = time.time()
                self.fall_time = self.fall_time_1 - self.fall_time_0

                self.speed = g * self.fall_time
                for i in range(0, int(self.speed), 1):
                    if self.y < GROUND:
                        self.y += 1
                        self.fall_distance += 1
                        self.fall_time += TIM
                    else:
                        break
                ""\"
"""


class Branch:
    def __init__(self, app):
        self.app = app
        self.sc = self.app.sc

        self.branch = {
            "right": [(0, 0), (160, 5), (0, 10)],
            "left": [(HALF_W, 0), (HALF_W - 160, 5), (HALF_W, 10)]
        }

        self.branch_list = {}
        self.branch_count = 2
        self.offset = 50

        self.generate()

    
    def generate(self):
        allowed_pos_l = list(range(100, 550, 25))
        allowed_pos_r = list(range(115, 565, 25))

        for i in range(self.branch_count):
            branch_align = choice(list(self.branch.keys()))

            try:
                pos_l = choice(allowed_pos_l)
                allowed_pos_l.remove(pos_l)

                pos_r = choice(allowed_pos_r)
                allowed_pos_r.remove(pos_r)
            except:
                pos = randint(100, 550) # branch["branch"][1][0], branch["branch"][2][1]

            if branch_align == "right": # [(0, 0), (160, 5), (0, 10)]
                branch = self.branch["right"]
                new_branch = [
                    (
                        branch[0][0] + self.offset,
                        branch[0][1] + pos_l - randint(2, 7)
                    ),
                    (
                        branch[1][0] + self.offset + randint(0, 50),
                        branch[1][1] + pos_l + randint(0, 5)
                    ),
                    (
                        branch[2][0] + self.offset,
                        branch[2][1] + pos_l + randint(2, 7)
                    )
                ]
                self.branch_list.update({
                    i: {
                        "branch": new_branch,
                        "rect": [
                            (new_branch[0][0], new_branch[0][1]),
                            (new_branch[1][0] - new_branch[0][0], new_branch[2][1] - new_branch[0][1])
                        ]
                    }
                })
            
            elif branch_align == "left":
                branch = self.branch["left"]
                new_branch = [
                    (
                        branch[0][0] - self.offset,
                        branch[0][1] + pos_r - randint(2, 7)
                    ),
                    (
                        branch[1][0] - self.offset - randint(0, 50),
                        branch[1][1] + pos_r + randint(0, 5)
                    ),
                    (
                        branch[2][0] - self.offset,
                        branch[2][1] + pos_r + randint(2, 7) # [(400, 0), (240, 5), (400, 10)]
                    )
                ] # [(350, 463), (181, 470), (350, 482)]
                self.branch_list.update({
                    i: {
                        "branch": new_branch,
                        "rect": [
                            (new_branch[1][0], new_branch[0][1]),
                            (new_branch[0][0] - new_branch[1][0], new_branch[2][1] - new_branch[0][1])
                        ]
                    }
                })
                print([(HALF_W, 0), (HALF_W - 160, 5), (HALF_W, 10)])


    def draw(self):
        for branch in self.branch_list:
            branch = self.branch_list[branch]
            pg.draw.polygon(self.sc, (242, 162, 58), branch["branch"]) # Гавнакод :>

            if DEBUG is True:
                pg.draw.rect(self.sc, (255, 255, 255), branch["rect"], 1)


class Branchh:
    def __init__(self, app) -> None:
        self.app = app
        self. sc = self.app.sc
        self.pos = 100, 100
        self.count = 1

        self.branches = []
        self.polygon_l = [(0, 0), (160, 5), (0, 10)]
        self.polygon_r = [(160 + 100, 0), (0, 5), (160 + 100, 10)]
        self.pos = 40, 0

        self.generate()
        

    def generate(self):
        pos = list(range(100, 500, 40))
        for i in range(self.count):
            branch_pos = choice(pos)
            pos.remove(branch_pos)
            self.br_l = [
                (
                    self.polygon_l[0][0] + self.pos[0],
                    self.polygon_l[0][1] + self.pos[1] + branch_pos
                ),
                (
                    self.polygon_l[1][0] + self.pos[0] + randint(10, 50),
                    self.polygon_l[1][1] + self.pos[1] + randint(0, 50) + branch_pos
                ),
                (
                    self.polygon_l[2][0] + self.pos[0],
                    self.polygon_l[2][1] + self.pos[1] + randint(0, 25) + branch_pos
                )
            ]
            self.br_r = [
                (
                    self.polygon_r[0][0] + self.pos[0],
                    self.polygon_r[0][1] + self.pos[1] + branch_pos
                ),
                (
                    self.polygon_r[1][0] + self.pos[0] + randint(10, 50),
                    self.polygon_r[1][1] + self.pos[1] + randint(0, 50) + branch_pos
                ),
                (
                    self.polygon_r[2][0] + self.pos[0],
                    self.polygon_r[2][1] + self.pos[1] + randint(0, 25) + branch_pos
                )
            ]

            self.branches.append(self.br_r)
            self.branches.append(self.br_l)
    
    def draw(self):
        for polygon in self.branches:
            pg.draw.polygon(self.sc, (125, 125, 60), polygon)


class Button:
    def __init__(self, app, buttons):
        self.app = app
        self.sc = self.app.sc

        for button in buttons:
            button = buttons[button]
            button_type = button["shape"]["type"]

            if button_type == "circle":
                pg.draw.circle(self.sc,
                               button["shape"]["color"],
                               button["pos"],
                               button["shape"]["radius"],
                               button["shape"]["width"])

                if DEBUG is True:
                    pg.draw.rect(self.sc, (255, 255, 255), button["shape"]["rect"], 1)
            
            elif button_type == "square":
                pg.draw.rect(self.sc,
                             button["shape"]["color"],
                             (
                                button["pos"]["x"], button["pos"]["y"],
                                button["shape"]["value"]["width"], button["shape"]["value"]["height"]
                             ),
                             button["shape"]["width"])

                if DEBUG is True:
                    pg.draw.rect(self.sc, (255, 255, 255), button["shape"]["rect"], 1)
            
            elif button_type == "polygon":
                pg.draw.polygon(self.sc,
                                button["shape"]["color"],
                                button["shape"]["value"],
                                button["shape"]["width"])
                if DEBUG is True:
                    pg.draw.rect(self.sc, (255, 255, 255), button["shape"]["rect"], 1)


class Label:
    def __init__(self, app, labels):
        self.app = app
        self.sc = self.app.sc

        for label in labels:
            label = labels[label]
            
            text = font.render(str(label["text"]), True, label["color"])
            self.sc.blit(text, label["pos"])

class Gui:
    def __init__(self, app, dot):
        self.app = app
        self.sc = self.app.sc

        self.item_list(dot)
    

    def item_list(self, dot):
        self.dot = dot
        self.items = {
            "buttons": {
                "start_simulation": {
                    "shape": {
                        "type": "polygon",
                        "value": [(410, 10), (440, 30), (410, 50)],
                        "rect": [(410, 10), (30, 40)],
                        "color": (58, 242, 76),
                        "width": 0
                    },
                    "event": "start_simulation"
                },
                "stop_simulation": {
                    "pos": {
                        "x": 450,
                        "y": 10
                    },
                    "shape": {
                        "type": "square",
                        "value": {
                            "width": 40,
                            "height": 40
                        },
                        "color": (242, 58, 58),
                        "width": 0,
                        "rect": [(450, 10), (40, 40)]
                    },
                    "event": "stop_simulation" # "rect": [(450, 10), (40, 40)],
                }
            },
            "labels": {
                "label1": {
                    "pos": (HALF_W + 10, 70),
                    "text": f"Час падіння: {round(self.dot.fall_time, 2)} cекунд",
                    "color": (255, 255, 255)
                },
                "label2": {
                    "pos": (HALF_W + 10, 86),
                    "text": f"Висота падіння: {round(self.dot.fall_distance, 2)} метрів",
                    "color": (255, 255, 255)
                },
                "label3": {
                    "pos": (HALF_W + 10, 102),
                    "text": f"Швидкість: {round(self.dot.speed * METER, 2)} м.с^2",
                    "color": (255, 255, 255)
                },
                "label4": {
                    "pos": (HALF_W + 10, 118),
                    "text": f"Енергія: {round(self.dot.energy, 2)} H",
                    "color": (255, 255, 255)
                },
                "f1": {
                    "pos": (HALF_W + 13, 20),
                    "text": "F1",
                    "color": (255, 255, 255)
                },
                "f2": {
                    "pos": (HALF_W + 60, 20),
                    "text": "F2",
                    "color": (255, 255, 255)
                }
            }
        }

        self.ranges = {}
        self.ranges2 = []
        yep = []
        for group in self.items: # Работает - не трогай
            if group == "buttons":
                for item in self.items[group]: # [(410, 10), (30, 40)]
                    rect = self.items[group][item]["shape"]["rect"]

                    for x in range(rect[0][0], rect[0][0] + rect[1][0]):
                        for y in range(rect[0][1], rect[0][1] + rect[1][1]):
                            yep.append((x, y))
                            self.ranges2.append((x, y))
                    
                    self.ranges.update({item: yep.copy()})
                    yep.clear()

    
    def get_pressed(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_btn = pg.mouse.get_pressed()

        for i in self.ranges:
            if mouse_pos in self.ranges[i]:
                #print(mouse_pos in self.ranges[i])
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                        user_events.update({i: True})
            if mouse_pos in self.ranges2:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    
    def render(self):
        for group in self.items:
            if group == "buttons":
                Button(self.app, self.items[group])
            if group == "labels":
                Label(self.app, self.items[group])


class App:
    def __init__(self):
        self.sc = pg.display.set_mode(WINDOW, vsync=1)
        self.clock = pg.time.Clock()

        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        self.dot = Dot()
        self.gui = Gui(self, self.dot)
        self.branch = Branch(self)


    def draw(self):
        pg.draw.line(self.sc, (0, 255, 0), (0, GROUND), (HALF_W, GROUND), 1)
        pg.draw.circle(self.sc, self.dot.color, self.dot.pos, self.dot.radius)

        pg.draw.line(self.sc, (255, 255, 255), (HALF_W, 0), (HALF_W, W_HEIGHT), 1)
        pg.draw.line(self.sc, (255, 255, 255), (0, 0), (0, W_WIDTH), 2)
        for i in range(0, W_HEIGHT, METER):
            pg.draw.line(self.sc, (255, 255, 255), (0, i), (10, i), 1)
        pg.draw.line(self.sc, (255, 255, 255), (HALF_W, 60), (W_WIDTH, 60), 1)

        pg.draw.line(self.sc, (144, 58, 242), (0, self.dot.pos[1]), (15, self.dot.pos[1]), 3)
        pg.draw.line(self.sc, (217, 58, 242), (0, self.dot.start_y), (0, self.dot.pos[1]), 4)

    
    def on_debug(self):
        if DEBUG is True:
            fall_time = font.render(str(self.dot.fall_time), True, (255, 255, 255))
            self.sc.blit(fall_time, (30, 10))

            fall_distance = font.render(str(int(self.dot.fall_distance)), True, (255, 255, 255))
            self.sc.blit(fall_distance, (30, 30))

            speed = font.render(str(self.dot.spd), True, (255, 255, 255))
            self.sc.blit(speed, (30, 50))

            energy = font.render(str(self.dot.energy), True, (255, 255, 255))
            self.sc.blit(energy, (30, 70))

    
    def run(self):
        a = 0
        while True:
            a += 1
            if a >= 10:
                a = 0
                user_events.update({
                    "start_simulation": False,
                    "stop_simulation": False
                })

            self.sc.fill("black")

            self.dot.move()
            self.draw()
            self.gui.render()
            self.gui.get_pressed()
            self.branch.draw()
            self.dot.update()
            self.gui.item_list(self.dot)
            self.on_debug()
            
            pg.display.flip()
            
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                if i.type == pg.KEYDOWN:
                    if i.key == pg.K_F3:
                        global DEBUG
                        DEBUG = True if DEBUG is False else False
                    if i.key == pg.K_F1:
                        user_events.update({"start_simulation": True})
                    if i.key == pg.K_F2:
                        user_events.update({"stop_simulation": True})

            pg.display.set_caption(str(int(self.clock.get_fps())))
            self.clock.tick(FPS)
            

if __name__ == "__main__":
    app = App()
    app.run()




"""
{
    "buttons": {
        "circle": {
            "pos": (HALF_W + 10, 10),
            "shape": {
                "type": "circle",
                "radius": 10,
                "color": (255, 0, 255),
                "width": 0
            },
            "event": "event_circle"
        },
        "square": {
            "pos": {
                "x": 450,
                "y": 450
            },
            "shape": {
                "type": "square",
                "value": {
                    "width": 10,
                    "height": 10
                },
                "color": (255, 0, 255),
                "width": 0
            },
            "event": "event_square"
        },
        "polygon": {
            "shape": {
                "type": "polygon",
                "value": [(310, 310), (320, 320), (310, 330)],
                "color": (255, 125, 255),
                "width": 0
            },
            "event": "event_polygon"
        }
    }
}
"""