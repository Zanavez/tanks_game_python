import pygame
from ObjectMap import ObjectMap

class MapGeneration:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.SCREEN_WIDTH_MAP, self.SCREEN_HEIGHT_MAP = 1620, 720
        self.SCREEN_WIDTH_MENU = 500
        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.display = pygame.display
        self.window = self.display.set_mode([self.SCREEN_WIDTH_MAP + self.SCREEN_WIDTH_MENU, self.SCREEN_HEIGHT_MAP],
                                            pygame.RESIZABLE, 32)
        self.display.set_caption('Tanks')

        self.object_list_render = []
        self.target_object_render = ObjectMap(self.window, "metal_wall.png", (30, 30), (0, 0), 1)

        self.map_render = []

        self._my_tank = 1
        self._enemy_tank = 1

        self._is_game = True

        self._is_add_object = True

        self.font_text = pygame.font.Font('freesansbold.ttf', 16) #Установка шрифта

        self.texts = []
        self.text_object = []

    @property
    def my_tank(self):
        return self._my_tank

    @my_tank.setter
    def my_tank(self, val):
        self._my_tank = val

    @property
    def enemy_tank(self):
        return self._enemy_tank

    @enemy_tank.setter
    def enemy_tank(self, val):
        self._enemy_tank = val

    def menu_render(self):
        self.texts = []
        text_my_tank = self.font_text.render("X "+str(self.my_tank), True, (255, 255, 255), (0, 0, 0))
        text_my_tank_rect = text_my_tank.get_rect()
        text_my_tank_rect.center = (self.SCREEN_WIDTH_MAP + (self.SCREEN_WIDTH_MENU // 2) - 100,
                                    self.SCREEN_HEIGHT_MAP - 200)

        self.texts.append((text_my_tank, text_my_tank_rect))

        text_enemy_tank = self.font_text.render("X "+str(self.enemy_tank), True, (255, 255, 255), (0, 0, 0))
        text_enemy_tank_rect = text_enemy_tank.get_rect()
        text_enemy_tank_rect.center = (self.SCREEN_WIDTH_MAP + (self.SCREEN_WIDTH_MENU // 2) - 100,
                                       self.SCREEN_HEIGHT_MAP - 300)

        self.texts.append((text_enemy_tank, text_enemy_tank_rect))

        text_wall_break = self.font_text.render("X бесконечность", True, (255, 255, 255), (0, 0, 0))
        text_wall_break_rect = text_wall_break.get_rect()
        text_wall_break_rect.center = (self.SCREEN_WIDTH_MAP + (self.SCREEN_WIDTH_MENU // 2) - 100,
                                       self.SCREEN_HEIGHT_MAP - 400)

        self.texts.append((text_wall_break, text_wall_break_rect))

        text_wall_metal = self.font_text.render("X бесконечность", True, (255, 255, 255), (0, 0, 0))
        text_wall_metal_rect = text_wall_metal.get_rect()
        text_wall_metal_rect.center = (self.SCREEN_WIDTH_MAP + (self.SCREEN_WIDTH_MENU // 2) - 100,
                                       self.SCREEN_HEIGHT_MAP - 500)

        self.texts.append((text_wall_metal, text_wall_metal_rect))

        my_tank = ObjectMap(self.window, "gray_tank.png", (30, 30),
                            (text_my_tank_rect.left - 50, text_my_tank_rect.top - 10))
        enemy_tank = ObjectMap(self.window, "yellow_tank.png", (30, 30),
                               (text_enemy_tank_rect.left - 50, text_enemy_tank_rect.top - 10))
        wall_break = ObjectMap(self.window, "break_wall.png", (30, 30),
                               (text_wall_break_rect.left - 50, text_wall_break_rect.top - 10))
        wall_metal = ObjectMap(self.window, "metal_wall.png", (30, 30),
                               (text_wall_metal_rect.left - 50, text_wall_metal_rect.top - 10))

        self.text_object = [my_tank, enemy_tank, wall_break, wall_metal]

    def start_game(self):
        self.render_map()
        self.menu_render()
        while self._is_game:
            self.window.fill([0, 0, 0])
            self.get_event()
            if self._is_add_object:
                self.move_target_object()
            self.show_object()
            self.show_menu()
            self.display.update()
            self.clock.tick(self.FPS)

    def move_target_object(self):
        position_mouse = pygame.mouse.get_pos()
        self.target_object_render.set_position((position_mouse[0] // 30 * 30, position_mouse[1] // 30 * 30))

    def show_menu(self):
        for text, rect in self.texts:
            self.window.blit(text, rect)
        for obj in self.text_object:
            obj.display()
        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(self.SCREEN_WIDTH_MAP, 0,
                                                                   self.SCREEN_WIDTH_MENU, self.SCREEN_HEIGHT_MAP),  10)

    def show_object(self):
        for object_game in self.object_list_render + [self.target_object_render]:
            object_game.display()

    def get_event(self):
        event_list = pygame.event.get()
        keys = pygame.key.get_pressed()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                position_mouse = pygame.mouse.get_pos()
                if position_mouse[0] <= self.SCREEN_WIDTH_MAP:
                    for i, object_map in enumerate(self.object_list_render):
                        is_hit = object_map.get_rect().collidepoint(position_mouse)
                        if is_hit:
                            if self._is_add_object is False:
                                x, y = object_map.get_position()
                                self.rewrite_map(x//30, y//30, 0)
                                break
                    if self._is_add_object:
                        x, y = self.target_object_render.get_position()
                        self.rewrite_map(x//30, y//30, self.target_object_render.type_obj)
                    self.render_map()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.target_object_render = ObjectMap(self.window, "metal_wall.png", (30, 30), (0, 0), 1)
                    self._is_add_object = True
                if event.key == pygame.K_2:
                    self.target_object_render = ObjectMap(self.window, "break_wall.png", (30, 30), (0, 0), 2)
                    self._is_add_object = True
                if event.key == pygame.K_3:
                    if self.my_tank > 0:
                        self.target_object_render = ObjectMap(self.window, "gray_tank.png", (30, 30), (0, 0), 4)
                        self._is_add_object = True
                if event.key == pygame.K_4:
                    if self.enemy_tank > 0:
                        self.target_object_render = ObjectMap(self.window, "yellow_tank.png", (30, 30), (0, 0), 5)
                        self._is_add_object = True
                if event.key == pygame.K_5:
                    self.target_object_render = ObjectMap(self.window, "metal_wall.png", (30, 30), (-10, -10), 1)
                    self._is_add_object = False
            if event.type == pygame.QUIT:
                pygame.quit()
            self.menu_render()

    def rewrite_map(self, x, y, type_obj):
        with open("files/map.txt", "w") as file:
            self.map_render[y][x] = type_obj
            for y in self.map_render:
                line = "".join(map(str, y)) + "\n"
                file.write(line)

    def swithe_tank(self):
        if (self._my_tank == 0 or self._enemy_tank == 0) and self.target_object_render.type_obj in (4, 5):
            self.target_object_render = ObjectMap(self.window, "metal_wall.png", (30, 30), (0, 0), 1)

    def render_map(self):
        self.my_tank = 1
        self.enemy_tank = 1
        self.map_render = []
        self.object_list_render = []
        with open("files/map.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.replace("\n", "")
                y = [int(x) for x in line]
                self.map_render.append(y)
            try:
                for y in range(self.SCREEN_HEIGHT_MAP // 30):
                    for x in range(self.SCREEN_WIDTH_MAP // 30):
                        if self.map_render[y][x] == 1:
                            self.object_list_render.append(ObjectMap(self.window, "metal_wall.png",
                                                                     (30, 30), (x * 30, y * 30), 1))
                        elif self.map_render[y][x] == 2:
                            self.object_list_render.append(ObjectMap(self.window, "break_wall.png",
                                                                     (30, 30), (x * 30, y * 30), 2))
                        elif self.map_render[y][x] == 4:
                            self.object_list_render.append(ObjectMap(self.window, "gray_tank.png",
                                                                     (30, 30), (x * 30, y * 30), 4))
                            self.my_tank -= 1
                            self.swithe_tank()
                        elif self.map_render[y][x] == 5:
                            self.object_list_render.append(ObjectMap(self.window, "yellow_tank.png",
                                                                     (30, 30), (x * 30, y * 30), 5))
                            self.enemy_tank -= 1
                            self.swithe_tank()
            except:
                for _ in range(self.SCREEN_HEIGHT_MAP // 30):
                    self.map_render.append("0" * (self.SCREEN_WIDTH_MAP // 30))