from Tank import Tank
from Wall import Wall
from Bullet import Bullet
from ObjectMap import ObjectMap
import pygame
from datetime import datetime
from random import randint


class MainApp:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.HIT_TANK_PLAYER_1 = pygame.USEREVENT + 1
        self.HIT_TANK_PLAYER_2 = pygame.USEREVENT + 2
        self.GAME_OVER = pygame.USEREVENT + 3
        self.SCREEN_HEIGHT_MENU = 180
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1620, 720
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.display = pygame.display
        self.window = self.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT + self.SCREEN_HEIGHT_MENU],
                                            pygame.RESIZABLE, 32)
        self.display.set_caption('Tanks')
        self.my_tank = None
        self.enemy_tank = None

        self.object_list_enemy = []
        self.object_list_wall = []
        self.object_list_bullet = []

        self.map_render = []

        self.position_players = {}

        self._is_game = True
        self._screen_game = True

        self._information = {"gray_tank.png": {
                                    "bullet": 0,
                                    "broke": 0,
                                    "hit_tank": 0},
                              "yellow_tank.png": {
                                  "bullet": 0,
                                  "broke": 0,
                                  "hit_tank": 0
                              },
                              "bullet_to_bullet": 0}

        self.font_text = pygame.font.Font('freesansbold.ttf', 16)

        self.texts = []

    def menu_render(self):
        self.texts = []
        text_my_tank = self.font_text.render("X "+str(self.my_tank.live), True, (255, 255, 255), (0, 0, 0))
        text_my_tank_rect = text_my_tank.get_rect()
        text_my_tank_rect.center = (self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT + self.SCREEN_HEIGHT_MENU // 2)

        self.texts.append((text_my_tank, text_my_tank_rect))

        text_enemy_tank = self.font_text.render("X "+str(self.enemy_tank.live), True, (255, 255, 255), (0, 0, 0))
        text_enemy_tank_rect = text_enemy_tank.get_rect()
        text_enemy_tank_rect.center = (self.SCREEN_WIDTH // 2 + 100, self.SCREEN_HEIGHT + self.SCREEN_HEIGHT_MENU // 2)

        self.texts.append((text_enemy_tank, text_enemy_tank_rect))

    def show_menu(self):
        for text, rect in self.texts:
            self.window.blit(text, rect)
        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(0, self.SCREEN_HEIGHT,
                                                                   self.SCREEN_WIDTH, self.SCREEN_HEIGHT_MENU),  10)

    def start_game(self):
        self.render_map()
        self.menu_render()
        while self._is_game:
            self.window.fill([0, 0, 0])
            self.get_event()
            self.move_object()
            self._hit_event()
            self.show_object()
            self.show_menu()
            self.display.update()
            self.clock.tick(self.FPS)
        self.game_over_screen()

    def game_over_screen(self):
        while self._screen_game:
            self.window.fill([0, 0, 0])
            font = pygame.font.Font('freesansbold.ttf', 32)

            text_in = ""
            if self.my_tank.live < self.enemy_tank.live:
                text_in = "Жёлтый танк победил"
            else:
                text_in = "Серый танк победил"

            text = font.render(text_in, True, (255, 255, 255), (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 100)

            text_1 = font.render("Отчет об окончании игры сгенерирован", True, (255, 255, 255), (0, 0, 0))
            textRect_1 = text_1.get_rect()
            textRect_1.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

            self.window.blit(text, textRect)
            self.window.blit(text_1, textRect_1)

            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    self.add_result_database()
                    pygame.quit()

            self.display.update()

    def show_object(self):
        for object_game in self.object_list_enemy + self.object_list_wall + self.object_list_bullet:
            object_game.display()

    def move_object(self):
        for object_game in self.object_list_enemy + self.object_list_bullet:
            object_game.move()

    def get_event(self):
        event_list = pygame.event.get()
        keys = pygame.key.get_pressed()

        self._move_tank_event(self.my_tank, keys, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d])
        self._move_tank_event(self.enemy_tank, keys, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = self.my_tank.fire()
                    self._information[self.my_tank.path_img]["bullet"] += 1
                    self.object_list_bullet.append(bullet)
                if event.key == pygame.K_p:
                    bullet = self.enemy_tank.fire()
                    self._information[self.enemy_tank.path_img]["bullet"] += 1
                    self.object_list_bullet.append(bullet)
            if event.type == self.HIT_TANK_PLAYER_1:
                self.my_tank.set_new_position(self.position_players["my_tank"])
            if event.type == self.HIT_TANK_PLAYER_2:
                self.enemy_tank.set_new_position(self.position_players["enemy_tank"])
            if event.type == self.GAME_OVER:
                self._is_game = False

        self._hit_wall_tank()

    def _move_tank_event(self, tank, keys, index_keys):
        if keys[index_keys[0]]:
            tank.direction = (0, -1)
            tank.transform_direction = (0, 1)
        elif keys[index_keys[1]]:
            tank.direction = (0, 1)
            tank.transform_direction = (0, -1)
        elif keys[index_keys[2]]:
            tank.direction = (-1, 0)
            tank.transform_direction = (1, 0)
        elif keys[index_keys[3]]:
            tank.direction = (1, 0)
            tank.transform_direction = (-1, 0)
        else:
            tank.direction = (0, 0)

    def _hit_event(self):
        self._hit_wall_tank()
        self._hit_bullet_object()

    def _hit_wall_tank(self):
        for enemy in self.object_list_enemy:
            id_walls = enemy.rect.collidelist(self.object_list_wall)
            if id_walls != -1:
                wall = self.object_list_wall[id_walls]
                range_hit = pygame.math.Vector2(wall.rect.centerx - enemy.rect.centerx,
                                                wall.rect.centery - enemy.rect.centery).length()
                if int(range_hit) < 37:
                    enemy.reflect()

    def _hit_bullet_object(self):
        for i, bullet in enumerate(self.object_list_bullet):
            id_walls = bullet.rect.collidelist(self.object_list_wall)
            id_tank = bullet.rect.collidelist(self.object_list_enemy)
            id_bullet = bullet.rect.collidelist(self.object_list_bullet[:i] + self.object_list_bullet[i+1:])
            if id_walls != -1:
                wall = self.object_list_wall[id_walls]
                if wall.type_wall == 2:
                    self.object_list_wall.pop(id_walls)
                    self._information[bullet.target_tank.path_img]["broke"] += 1
                self.object_list_bullet.pop(i)
            elif id_tank != -1:
                tank = self.object_list_enemy[id_tank]
                tank.live = 1
                self._information[bullet.target_tank.path_img]["hit_tank"] += 1
                self.object_list_bullet.pop(i)
                self.menu_render()
            elif id_bullet != -1:
                self._information["bullet_to_bullet"] += 1
                self.object_list_bullet.pop(i)
                self.object_list_bullet.pop(id_bullet)


    def render_tank(self, type_tank, cell):
        if type_tank == 4:
            self.my_tank = Tank(self.window, "gray_tank.png", (0, 0), 3, (30, 30), (cell[0] * 30, cell[1] * 30),
                                self.HIT_TANK_PLAYER_1, self.GAME_OVER)
            self.position_players["my_tank"] = (cell[0] * 30, cell[1] * 30)
            self.object_list_enemy.append(self.my_tank)
        if type_tank == 5:
            self.enemy_tank = Tank(self.window, "yellow_tank.png", (0, 0), 3, (30, 30), (cell[0] * 30, cell[1] * 30),
                                   self.HIT_TANK_PLAYER_2, self.GAME_OVER)
            self.object_list_enemy.append(self.enemy_tank)
            self.position_players["enemy_tank"] = (cell[0] * 30, cell[1] * 30)

    def render_map(self):
        with open("files/map.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.replace("\n", "")
                y = [int(x) for x in line]
                self.map_render.append(y)
            for y in range(self.SCREEN_HEIGHT // 30):
                for x in range(self.SCREEN_WIDTH // 30):
                    if self.map_render[y][x] == 1:
                        self.object_list_wall.append(Wall("metal_wall.png", x * 30, y * 30, self.window,
                                                          self.map_render[y][x]))
                    elif self.map_render[y][x] == 2:
                        self.object_list_wall.append(Wall("break_wall.png", x * 30, y * 30, self.window,
                                                          self.map_render[y][x]))
                    self.render_tank(self.map_render[y][x], (x, y))

    def last_id_result(self):
        with open("files/results.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) > 0:
                id_result = lines[-1].split("|")[0]
                return int(id_result) + 1
            return 1

    def generate_file_results(self, name_file):
        with open(name_file, "w+", encoding="utf-8") as file:
            file.write("Итоги игры\n")
            sum_bullet = 0
            sum_wall = 0
            sum_hit = 0
            for key in self._information:
                if key == "gray_tank.png":
                    file.write("Статистика серого танка:\n")
                    file.write(f"Количества здоровья: {self.my_tank.live}\n")
                    file.write(f"Выпущенно снарядов за игру: {self._information[key]['bullet']}\n")
                    file.write("\tИз этих снарядов:\n")
                    file.write(f"\t\tСнаряды, сломавшие стены: {self._information[key]['broke']}\n")
                    file.write(f"\t\tСнаряды, попавшие в танк противника: {self._information[key]['hit_tank']}\n")

                    sum_bullet += self._information[key]['bullet']
                    sum_wall += self._information[key]['broke']
                    sum_hit += self._information[key]['hit_tank']
                elif key == "yellow_tank.png":
                    file.write("Статистика желтого танка:\n")
                    file.write(f"Количества здоровья: {self.enemy_tank.live}\n")
                    file.write(f"Выпущенно снарядов за игру: {self._information[key]['bullet']}\n")
                    file.write("\tИз этих снарядов:\n")
                    file.write(f"\t\tСнаряды, сломавшие стены: {self._information[key]['broke']}\n")
                    file.write(f"\t\tСнаряды, попавшие в танк противника: {self._information[key]['hit_tank']}\n")

                    sum_bullet += self._information[key]['bullet']
                    sum_wall += self._information[key]['broke']
                    sum_hit += self._information[key]['hit_tank']
                else:
                    file.write("\n")
                    file.write(f"Снаряды, попавшие в снаряды противника: {self._information[key]}\n")

            file.write("-" * 60 + "\n")
            file.write("Общая статистика\n")
            file.write(f"Выпущенно снарядов за игру: {sum_bullet}\n")
            file.write("\tИз этих снарядов:\n")
            file.write(f"\t\tСнаряды, сломавшие стены: {sum_wall}\n")
            file.write(f"\t\tСнаряды, попавшие в танк: {sum_hit}\n")
            file.write(f"Снаряды, попавшие в танк: {sum_hit}\n")
            if self.my_tank.live < self.enemy_tank.live:
                file.write(f"Победил жёлтый танк")
            else:
                file.write(f"Победил серый танк")

    def add_result_database(self):
        with open("files/results.txt", "a+", encoding="utf-8") as file:
            id_result = self.last_id_result() #ID результата игры
            path_file = f"files/results/{randint(1, 10000000)}.txt"
            self.generate_file_results(path_file)
            datetime_now = datetime.now()
            file.write(f"{id_result}|{datetime_now.strftime('%d/%m/%Y, %H:%M')}|{path_file}\n")