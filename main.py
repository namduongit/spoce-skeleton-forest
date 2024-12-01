import pygame
import random
import csv
import button
from settings import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface = pygame.Surface((WIDTH_MAP, HEIGHT_MAP))
logo_game = pygame.image.load('Map/Logo/logo_game.png').convert_alpha()
pygame.display.set_icon(logo_game)
pygame.display.set_caption("Spoce Skeleton Forest")
# Bộ đếm thời gian cho màn hình
clock = pygame.time.Clock()

# Cài đặt phông chữ ThaleahFat
font = pygame.font.Font('Map/Font/ThaleahFat.ttf', 18)
# Biến dùng để cuộn màn hình
screen_scroll = 0
bg_scroll = 0
# Biến khởi tạo level và max level
level = 1
MAX_LEVELS = 5
# Biến dùng để người chơi có thể nâng cấp
speed_bullet = 0
dame_bullet = 0
health_bonus = 0
coin_player = 100000
health_tile = 10
bullet_cooldown = 0
# Biến dùng để chơi game
main_game = False
play_game = False
option_game = False
exit_game = False
# Biến dùng để chơi game
next_complete = False
# Biến dùng trong map editor
current_tile = 0
scroll = 0
scroll_left = False
scroll_right = False
scroll_speed = 1

# Back ground trong game
img_1 = pygame.image.load('Map/Backgrounds/1.png').convert_alpha()
img_2 = pygame.image.load('Map/Backgrounds/2.png').convert_alpha()
img_3 = pygame.image.load('Map/Backgrounds/3.png').convert_alpha()
# Biến đổi background sao cho vừa màn hình (1024 x 512)
bg_1 = pygame.transform.scale(img_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_2 = pygame.transform.scale(img_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_3 = pygame.transform.scale(img_3, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Bề mặt dùng trong map editor
layer_1 = pygame.image.load('Map/Backgrounds/1.png').convert_alpha()
layer_2 = pygame.image.load('Map/Backgrounds/2.png').convert_alpha()
layer_3 = pygame.image.load('Map/Backgrounds/3.png').convert_alpha()
layer_1 = pygame.transform.scale(layer_1, (WIDTH_MAP, HEIGHT_MAP))
layer_2 = pygame.transform.scale(layer_2, (WIDTH_MAP, HEIGHT_MAP))
layer_3 = pygame.transform.scale(layer_3, (WIDTH_MAP, HEIGHT_MAP))

empty_heath_bar = pygame.image.load('Entity/Player/assets/health_bar.png').convert_alpha()
chart_health = pygame.image.load('Entity/Player/assets/chart.png').convert_alpha()
board = pygame.image.load('Entity/Player/assets/board.png').convert_alpha()
bullet_image = pygame.image.load('Entity/Player/assets/bullet.png').convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (int(bullet_image.get_width() * 0.03), int(bullet_image.get_height() * 0.03)))
# board = pygame.transform.scale(board, (int(board.get_width() * 0.8), int(board.get_height() * 0.8)))
'''================================= Các ảnh ở cửa số chính ======================================='''
background = pygame.image.load('MainGame/main_game.png').convert_alpha()
background = pygame.transform.scale(background, (int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))

# Cái ảnh settings của game dành cho player
setting_game_image = pygame.image.load('MainGame/settings_game.png').convert_alpha()
setting_game_image = pygame.transform.scale(setting_game_image, (350, 370))
'''================================================================================================'''

'''==================================== Các nút ở cửa sổ chính ===================================='''
play_btn = pygame.image.load('MainGame/button_action/PlayBtn.png').convert_alpha()
play_btn_hover = pygame.image.load('MainGame/button_action/PlayClick.png').convert_alpha()
play_btn = pygame.transform.scale(play_btn, (MAINBTN_WIDTH, MAINBTN_HEIGHT))
play_btn_hover = pygame.transform.scale(play_btn_hover, (MAINBTN_WIDTH, MAINBTN_HEIGHT))

exit_btn = pygame.image.load('MainGame/button_action/ExitBtn.png').convert_alpha()
exit_btn_hover = pygame.image.load('MainGame/button_action/ExitClick.png').convert_alpha()
exit_btn = pygame.transform.scale(exit_btn, (int(MAINBTN_WIDTH), int(MAINBTN_HEIGHT)))
exit_btn_hover = pygame.transform.scale(exit_btn_hover, (int(MAINBTN_WIDTH), int(MAINBTN_HEIGHT)))

option_btn = pygame.image.load('MainGame/button_action/OptBtn.png').convert_alpha()
option_btn_hover = pygame.image.load('MainGame/button_action/OptClick.png').convert_alpha()
option_btn = pygame.transform.scale(option_btn, (int(MAINBTN_WIDTH), int(MAINBTN_HEIGHT)))
option_btn_hover = pygame.transform.scale(option_btn_hover, (int(MAINBTN_WIDTH), int(MAINBTN_HEIGHT)))

play = button.Button(100, 120, play_btn, play_btn_hover, 1)
exit = button.Button(100, 120 + 10 + MAINBTN_HEIGHT, exit_btn, exit_btn_hover, 1)
option = button.Button(100, 120 + 10 * 2 + MAINBTN_HEIGHT * 2, option_btn, option_btn_hover, 1)
'''=================================================================================================='''

'''==================================== Các nút ở trong map editor ===================================='''
save_img = pygame.image.load('MainGame/button_action/save_btn.png').convert_alpha()
load_img = pygame.image.load('MainGame/button_action/load_btn.png').convert_alpha()

save_btn = button.Button(714, 416 - save_img.get_height() * 0.8, save_img, save_img, 0.8)
load_btn = button.Button(714 + save_img.get_width(),  416 - save_img.get_height() * 0.8, load_img, load_img, 0.8)
'''=================================================================================================='''

'''==================================== Các nút ở trong game ===================================='''
upgarde_dame = pygame.image.load('MainGame/button_action/dameBullet.png').convert_alpha()
upgrade_dame_hover = pygame.image.load('MainGame/button_action/dameHover.png').convert_alpha()
upgrade_health = pygame.image.load('MainGame/button_action/healthUpgrade.png').convert_alpha()
upgrade_health_hover = pygame.image.load('MainGame/button_action/healthHover.png').convert_alpha()
upgrade_speed_bullet = pygame.image.load('MainGame/button_action/speedBullet.png').convert_alpha()
upgrade_speed_bullet_hover = pygame.image.load('MainGame/button_action/speedHover.png').convert_alpha()
recover_health = pygame.image.load('MainGame/button_action/recoverHealth.png').convert_alpha()
recover_health_hover = pygame.image.load('MainGame/button_action/recoverHover.png').convert_alpha()
upgrade_cooldown = pygame.image.load('MainGame/button_action/cooldown.png').convert_alpha()
upgrade_cooldown_hover = pygame.image.load('MainGame/button_action/cooldownHover.png').convert_alpha()
dame_upgrade = button.Button(SCREEN_WIDTH - 50, 200, upgarde_dame, upgrade_dame_hover, 1)
health_upgrade = button.Button(SCREEN_WIDTH - 50, 250, upgrade_health, upgrade_health_hover, 1)
speed_bullet_upgrade = button.Button(SCREEN_WIDTH - 50, 300, upgrade_speed_bullet, upgrade_speed_bullet_hover, 1)
recover_health_upgrade = button.Button(SCREEN_WIDTH - 50, 350, recover_health, recover_health_hover, 1)
cooldown_upgrade = button.Button(SCREEN_WIDTH - 50, 400, upgrade_cooldown, upgrade_cooldown_hover, 1)

home = pygame.image.load('MainGame/button_action/home.png').convert_alpha()
home_hover = pygame.image.load('MainGame/button_action/homeHover.png').convert_alpha()
home_btn = button.Button(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, home, home_hover, 1)

restartClick = pygame.image.load('MainGame/button_action/restartClick.png').convert_alpha()
restartHover = pygame.image.load('MainGame/button_action/restartHover.png').convert_alpha()
menuClick = pygame.image.load('MainGame/button_action/menuClick.png').convert_alpha()
menuHover = pygame.image.load('MainGame/button_action/menuHover.png').convert_alpha()

menu_btn = button.Button(SCREEN_WIDTH // 2 - 20 - restartClick.get_width(), SCREEN_HEIGHT // 2 - 100, menuClick, menuHover, 1)
restart_btn = button.Button(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 100, restartClick, restartHover, 1)
'''=================================================================================================='''


'''================================== Các loại âm thanh trong game =================================='''
coin_recieved = pygame.mixer.Sound('Audio/coin.wav')
coin_recieved.set_volume(0.3)
jump = pygame.mixer.Sound('Audio/jump.wav')
jump.set_volume(0.3)
shot = pygame.mixer.Sound('Audio/shot.wav')
shot.set_volume(0.3)
game_over_audio = pygame.mixer.Sound('Audio/game_over.wav')
game_over_audio.set_volume(0.3)
punch = pygame.mixer.Sound('Audio/punch.wav')
punch.set_volume(0.3)
hurt = pygame.mixer.Sound('Audio/hurt.wav')
hurt.set_volume(0.3)
win_game = pygame.mixer.Sound('Audio/win.wav')
win_game.set_volume(0.3)
play_audio = False
'''=================================================================================================='''

# Nhóm sprite
skeleton_group = pygame.sprite.Group()
bigger_group = pygame.sprite.Group()
demon_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
shop_group = pygame.sprite.Group()

decoration_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
lamp_group = pygame.sprite.Group()
fence_group = pygame.sprite.Group()
rock_group = pygame.sprite.Group()
grass_group = pygame.sprite.Group()

level_complete_group = pygame.sprite.Group()

'''================================== Các class trong game ===================================='''
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        animation_types = ['Idle', 'Run', 'Jump', 'Hurt', 'Shot', 'Dead', 'Recharge', 'Walk', 'Punch']
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.scale = scale
        self.frame_index = 0
        self.animation_list = []
        for animation in animation_types:
            sprite_sheet = pygame.image.load(f'Entity/Player/image/{animation}.png').convert_alpha()
            number_frames = sprite_sheet.get_width() // PLAYER_WIDTH
            temp_list = []
            for i in range(number_frames):
                frames = sprite_sheet.subsurface(i * PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
                frames = pygame.transform.scale(frames, (int(PLAYER_WIDTH * self.scale), int(PLAYER_HEIGHT * self.scale)))
                temp_list.append(frames)
            self.animation_list.append(temp_list)
        # Các biến giới hạn tối đa
        self.max_health = 150 + health_bonus
        self.max_bullet = 20
        self.dame = 20
        self.speed = 5
        self.direction = 1
        self.flip = False
        # Các biến khởi tạo
        self.health = self.max_health
        self.bullet = self.max_bullet
        # Biến dùng để di chuyển
        self.moving_left = False
        self.moving_right = False
        self.move_jump = False
        self.run = False
        self.in_air = False
        self.hurt = False
        self.shoot = False
        self.punch = False
        self.rechange = False
        self.vel_y = 0
        # Ảnh và vị trí của player
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Biến đợi chờ là hạnh phúc
        self.shoot_cooldown = 0
        # Biến kiếm tra va chạm
        self.width = self.rect.width
        self.height = self.rect.height
        self.collision_rect = pygame.Rect(self.rect.centerx - 10 * self.scale, self.rect.bottom - 20 * self.scale, 20 * self.scale, 20 * self.scale)
        self.coin_collision = pygame.Rect(self.rect.centerx - 10 * self.scale, self.rect.centery, 20 * self.scale, self.rect.height  // 2)
        # Nhóm đạn dược của người chơi
        self.bullets = pygame.sprite.Group()

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        # ['Idle', 'Run', 'Jump', 'Hurt', 'Shot', 'Dead', 'Recharge', 'Walk', 'Punch']
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 5: # Dead
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action == 2: # Jump
                self.update_action(0)
            elif self.action == 3: # Hurt
                self.update_action(0)
                self.hurt = False
            elif self.action == 4: # Shot
                self.update_action(0)
                self.shoot = False
            elif self.action == 6: # Recharge
                self.bullet = self.max_bullet
                self.update_action(0)
            elif self.action == 8: # Punch
                self.update_action(0)
            else:
                self.frame_index = 0

    def move(self):
        screen_scroll = 0
        dx = 0
        dy = 0

        # Điều chỉnh theo hướng di chuyển
        if self.run:
            dx = (self.speed * self.direction) * 2
        if self.moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        if self.moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
        if self.move_jump and not self.in_air:
            self.vel_y = -12
            self.move_jump = False
            self.in_air = True

        # Thêm trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Kiểm tra va chạm
        for tile in world.obstacle_list:
            # Trục x
            if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width, self.collision_rect.height):
                dx = 0
            # Trục y
            if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width, self.collision_rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.collision_rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.collision_rect.bottom

        # Ngăn chặn đập đầu dô tường
        if self.collision_rect.left + dx < 0 or self.collision_rect.right + dx > SCREEN_WIDTH:
            dx = 0
        # Kiểm tra coi có bị rớt xuống vực không
        if self.coin_collision.top > SCREEN_HEIGHT:
            self.health = 0
            dy = 0

        # Cập nhật vị trí của collision_rect
        self.collision_rect.x += dx
        self.collision_rect.y += dy

        # Cập nhật vị trí của self.rect để đồng bộ hóa với collision_rect
        self.rect.centerx = self.collision_rect.centerx
        self.rect.bottom = self.collision_rect.bottom
        # Cập nhật ví trí của coin_collision
        self.coin_collision.x = self.rect.centerx - 10 * self.scale
        self.coin_collision.y = self.rect.centery

        # Cập nhật cuộn màn hình
        if (self.collision_rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) or \
        (self.collision_rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
            self.collision_rect.x -= dx
            screen_scroll = -dx



        return screen_scroll

    def gun(self):
        if self.shoot_cooldown == 0 and self.bullet > 0:
            self.shoot_cooldown = 50 - bullet_cooldown
            bullet = Bullet(self.rect.centerx, self.rect.centery + 20 * self.scale, self.direction, self.flip)
            self.bullets.add(bullet)
            self.bullet -= 1
            print('Đã thêm')

    def update(self):
        # ['Idle', 'Run', 'Jump', 'Hurt', 'Shot', 'Dead', 'Recharge', 'Walk', 'Punch']
        if self.health <= 0:
            self.health = 0
            self.update_action(5)
            self.hurt = False
            self.moving_left = False
            self.moving_right = False
            self.shoot = False
            self.move_jump = False
            self.in_air = False
            self.punch = False
            self.run = False
        else:
            if self.run:
                self.update_action(1)
            elif self.in_air:
                self.update_action(2)
            elif self.hurt:
                self.update_action(3)
            elif self.shoot:
                self.update_action(4)
            elif self.rechange or self.bullet == 0:
                self.update_action(6)
                # Tất cả hành động khác dừng lại
                self.moving_left = False
                self.moving_right = False
                self.move_jump = False
                self.punch = False
                self.run = False
                self.hurt = False
            elif self.moving_left or self.moving_right:
                self.update_action(7)
            elif self.punch:
                self.update_action(8)
            else:
                self.update_action(0)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self):
        self.update_animation()
        self.update()
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, 'Red', self.collision_rect, 1)
        pygame.draw.rect(screen, 'Black', self.rect, 1)
        pygame.draw.rect(screen, 'Yellow', self.coin_collision, 1)
        for bullet in self.bullets:
            bullet.draw()
            bullet.update()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, flip):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 + speed_bullet
        self.image = pygame.image.load('Entity/Player/assets/1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self):
        self.rect.x += (self.direction * self.speed + speed_bullet) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, 'Black', self.rect, 1)

class CoinBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.animation_list = []
        sprite_sheet = pygame.image.load('Decoration/coin.png').convert_alpha()
        number_frames = sprite_sheet.get_width() // COIN_WIDTH
        for i in range(number_frames):
            frames = sprite_sheet.subsurface(i * COIN_WIDTH, 0, COIN_WIDTH, COIN_HEIGHT)
            frames = pygame.transform.scale(frames, (int(COIN_WIDTH * 1.5), int(COIN_HEIGHT * 1.5)))
            self.animation_list.append(frames)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        screen.blit(self.image, self.rect)

class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        animation_types = ['Idle', 'Walk', 'Attack', 'Die', 'Hurt']
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.frame_index = 0
        self.animation_list = []
        for animation in animation_types:
            sprite_sheet = pygame.image.load(f'Entity/Skeleton/image/{animation}.png').convert_alpha()
            number_frames = sprite_sheet.get_width() // SKELETON_WIDTH
            temp_list = []
            for i in range(number_frames):
                frames = sprite_sheet.subsurface(i * SKELETON_WIDTH, 0, SKELETON_WIDTH, SKELETON_HEIGHT)
                frames = pygame.transform.scale(frames, (int(SKELETON_WIDTH * scale), int(SKELETON_HEIGHT * scale)))
                temp_list.append(frames)
            self.animation_list.append(temp_list)
        # Các biến khởi tạo
        self.health = 100
        self.dame = 10
        self.speed = 1
        self.direction = 1
        self.flip = False
        # Các biến dùng để di chuyển
        self.moving_left = False
        self.moving_right = False
        self.attack = False
        self.hurt = False
        self.vel_y = 0
        # Ảnh và vị trí của player
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Biến chờ đợi là hành phúc
        self.dame_cooldown = 0
        # Biến kiểm tra va chạm
        self.width = self.rect.width
        self.height = self.rect.height
        self.collision_rect = pygame.Rect(self.rect.centerx - 5 * scale, self.rect.centery - 10 * scale, 10 * scale, 42 * scale)
        # Biến dành cho ai
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        # Biến tầm nhìn
        self.vision = pygame.Rect(0, 0, 250, self.height)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action == 4: # Hurt
                self.update_action(0)
                self.hurt = False
            elif self.action == 2: # Attack
                self.update_action(0)
                self.attack = False
            else:
                self.frame_index = 0

    def move(self):
        dx = 0
        dy = 0

        # Điều chỉnh theo hướng di chuyển
        if self.moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        if self.moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
        # Thêm trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Kiểm tra va chạm
        for tile in world.obstacle_list:
            # Trục x
            if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width, self.collision_rect.height):
                dx = 0
            # Trục y
            if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width, self.collision_rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.collision_rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.collision_rect.bottom

        # Ngăn chặn đập đầu dô tường
        if self.collision_rect.left + dx < 0 or self.collision_rect.right + dx > SCREEN_WIDTH:
            dx = 0

        # Cập nhật vị trí của collision_rect
        self.collision_rect.x += dx
        self.collision_rect.y += dy

        # Cập nhật vị trí của self.rect để đồng bộ hóa với collision_rect
        self.rect.centerx = self.collision_rect.centerx
        self.rect.bottom = self.collision_rect.bottom

    def ai(self, player):
        # Chỗ này để cập nhật tầm nhìn của skeleton
        if self.direction == -1:
            self.vision.x = self.rect.centerx + 250 * self.direction
        else:
            self.vision.x = self.rect.centerx
        self.vision.y = self.rect.y
        if self.health > 0:
            if self.vision.colliderect(player.coin_collision) and player.health > 0:
                self.idling = True
                self.idling_counter = 10
                self.speed = 2
                if abs(self.rect.centerx - player.rect.centerx) > 30:
                    if self.rect.centerx > player.rect.centerx:
                        self.moving_left = True
                        self.moving_right = False
                    else:
                        self.moving_left = False
                        self.moving_right = True
                    self.move()
                else:
                    self.moving_left = False
                    self.moving_right = False
                    self.attack = True
                    if self.attack == True:
                        if self.dame_cooldown == 0:
                            player.health -= 10
                            print(player.health)
                            self.dame_cooldown = 100
                            punch.play()
                            if random.randint(1, 3) == 1:
                                player.hurt = True
            else:
                self.speed = 1
            if not self.idling and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = random.randint(60, 300)
                self.moving_left = False
                self.moving_right = False
            else:
                if not self.idling:
                    if self.direction == 1:
                        self.moving_right = True
                        self.moving_left = False
                    else:
                        self.moving_right = False
                        self.moving_left = True
                    self.move()
                    self.move_counter += 1
                    if self.move_counter > 32:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll

    def update(self):
        # ['Idle', 'Walk', 'Attack', 'Die', 'Hurt']
        if self.health <= 0:
            self.health = 0
            self.update_action(3)
            self.hurt = False
            self.moving_left = False
            self.moving_right = False
            self.attack = False
        else:
            if self.moving_left or self.moving_right:
                self.update_action(1)
            elif self.attack:
                self.update_action(2)
            elif self.hurt:
                self.update_action(4)
            else:
                self.update_action(0)
        if self.dame_cooldown > 0:
            self.dame_cooldown -= 1

    def draw(self, player):
        self.update()
        self.update_animation()
        self.ai(player)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, 'Red', self.collision_rect, 1)
        pygame.draw.rect(screen, 'Black', self.rect, 1)
        pygame.draw.rect(screen, 'Yellow', self.vision, 1)

class Bigger(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        folder_path = 'Entity/Bigger'
        animation_types = ['Idle', 'Walk', 'Attack', 'Hurt', 'Die']
        self.action = 0
        self.frame_index = 0
        self.animation_list = []
        for animation in animation_types:
            temp_list = []
            sprite_sheet = pygame.image.load(f'{folder_path}/image/{animation}.png')
            number_frame = sprite_sheet.get_width() // BIGGER_WIDTH
            for i in range(number_frame):
                frames = sprite_sheet.subsurface(i * BIGGER_WIDTH, 0, BIGGER_WIDTH, BIGGER_HEIGHT)
                frames = pygame.transform.scale(frames, (int(BIGGER_WIDTH * scale), int(BIGGER_HEIGHT * scale)))
                temp_list.append(frames)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Define variable ai movement
        self.moving_left = False
        self.moving_right = False
        self.attack = False
        self.hurt = False
        self.die = False
        self.speed = 1
        self.vel_y = 0
        # Define max value
        self.max_health = 30
        self.max_dame = 5
        # Define variable
        self.health = self.max_health
        self.dame = self.max_dame
        # Define variable timer and direction
        self.update_time = pygame.time.get_ticks()
        self.direction = -1
        self.flip = False
        # Defind ai variable
        self.idling = False
        self.idling_counter = 0
        self.move_counter = 0
        self.dame_cooldown = 0
        # Define variable to check collision
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision_rect = pygame.Rect(self.rect.centerx + 5 * scale, self.rect.top - 9 * scale, 10 * scale, 50 - scale)
        # Define variable to check vision player
        self.vision = pygame.Rect(0, 0, 250, self.height)

    def update_action(seLf, new_action):
        if seLf.action != new_action:
            seLf.action = new_action
            seLf.frame_index = 0

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.attack:
                self.attack = False
                self.update_action(0)
            elif self.hurt:
                self.hurt = False
                self.update_action(0)
            elif self.die:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def move(self):
        dx = 0
        dy = 0

        # Điều chỉnh theo hướng di chuyển
        if self.moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = True
        if self.moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = False

        # Thêm trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Kiểm tra va chạm
        for tile in world.obstacle_list:
            # Trục x
            if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width, self.collision_rect.height):
                dx = 0
            # Trục y
            if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width, self.collision_rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.collision_rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.collision_rect.bottom

        # Ngăn chặn đập đầu dô tường
        if self.collision_rect.left + dx < 0 or self.collision_rect.right + dx > SCREEN_WIDTH:
            dx = 0

        # Cập nhật vị trí của collision_rect
        self.collision_rect.x += dx
        self.collision_rect.y += dy

        # Cập nhật vị trí của self.rect để đồng bộ hóa với collision_rect
        self.rect.centerx = self.collision_rect.centerx
        self.rect.bottom = self.collision_rect.bottom

    def ai(self, player):
        # Chỗ này để cập nhật tầm nhìn của skeleton
        if self.direction == -1:
            self.vision.x = self.rect.centerx + 250 * self.direction
        else:
            self.vision.x = self.rect.centerx
        self.vision.y = self.rect.y
        if self.health > 0:
            if self.vision.colliderect(player.coin_collision) and player.health > 0:
                self.idling = True
                self.idling_counter = 10
                self.speed = 2
                if abs(self.rect.centerx - player.rect.centerx) > 30:
                    if self.rect.centerx > player.rect.centerx:
                        self.moving_left = True
                        self.moving_right = False
                    else:
                        self.moving_left = False
                        self.moving_right = True
                    self.move()
                else:
                    self.moving_left = False
                    self.moving_right = False
                    self.attack = True
                    if self.attack == True:
                        if self.dame_cooldown == 0:
                            player.health -= 10
                            print(player.health)
                            self.dame_cooldown = 100
                            punch.play()
                            if random.randint(1, 3) == 1:
                                player.hurt = True
            else:
                self.speed = 1
            if not self.idling and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = random.randint(60, 300)
                self.moving_left = False
                self.moving_right = False
            else:
                if not self.idling:
                    if self.direction == 1:
                        self.moving_right = True
                        self.moving_left = False
                    else:
                        self.moving_right = False
                        self.moving_left = True
                    self.move()
                    self.move_counter += 1
                    if self.move_counter > 32:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.moving_left = False
            self.moving_right = False
            self.attack = False
            self.hurt = False
            self.die = True
            self.update_action(4)
            # ['Idle', 'Walk', 'Attack', 'Hurt', 'Die']
        else:
            if self.hurt:
                self.update_action(3)
            elif self.attack:
                self.update_action(2)
            elif self.moving_left or self.moving_right:
                self.update_action(1)
            else:
                self.update_action(0)
        if self.dame_cooldown > 0:
            self.dame_cooldown -= 1


    def draw(self, player):
        self.update()
        self.update_animation()
        self.ai(player)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, 'Red', self.collision_rect, 1)
        pygame.draw.rect(screen, 'Black', self.rect, 1)
        pygame.draw.rect(screen, 'Yellow', self.vision, 1)


class Demon(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        folder_path = 'Entity/Demon'
        animation_types = ['Idle', 'Walk', 'Cleave', 'Hurt', 'Death']
        self.action = 0
        self.frame_index = 0
        self.animation_list = []
        for animation in animation_types:
            temp_list = []
            # Đếm trong thư mục image có bao nhiêu file ảnh
            number_frame = len(os.listdir(f'{folder_path}/image/{animation}'))
            for i in range(1, number_frame + 1):
                frames = pygame.image.load(f'{folder_path}/image/{animation}/{i}.png').convert_alpha()
                frames = pygame.transform.scale(frames, (int(DEMON_WIDTH * scale), int(DEMON_HEIGHT * scale)))
                temp_list.append(frames)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Define variable movement
        self.moving_left = False
        self.moving_right = False
        self.attack = False
        self.hurt = False
        self.die = False
        self.speed = 1
        self.vel_y = 0
        # Define max value
        self.max_health = 1000
        self.max_dame = 50
        # Define variable
        self.health = self.max_health
        self.dame = self.max_dame
        # Define variable timer and direction
        self.update_time = pygame.time.get_ticks()
        self.direction = -1
        self.flip = False
        # Defind ai variable
        self.idling = False
        self.idling_counter = 0
        self.move_counter = 0
        self.dame_cooldown = 0
        # Define variable to check collision
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision_rect = pygame.Rect(self.rect.centerx - 10 * scale, self.rect.centery + 20 * scale, 20 * scale, 60 * scale)
        # Define variable to check vision player
        self.vision = pygame.Rect(0, 0, 250, self.height)

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION - 20:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.attack:
                self.attack = False
                self.update_action(0)
            elif self.hurt:
                self.hurt = False
                self.update_action(0)
            elif self.die:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def move(self):
        dx = 0
        dy = 0

        # Điều chỉnh theo hướng di chuyển
        if self.moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = True
        if self.moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = False

        # Thêm trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Kiểm tra va chạm
        for tile in world.obstacle_list:
            # Trục x
            if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width, self.collision_rect.height):
                dx = 0
            # Trục y
            if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width, self.collision_rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.collision_rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.collision_rect.bottom

        # Ngăn chặn đập đầu dô tường
        if self.collision_rect.left + dx < 0 or self.collision_rect.right + dx > SCREEN_WIDTH:
            dx = 0

        # Cập nhật vị trí của collision_rect
        self.collision_rect.x += dx
        self.collision_rect.y += dy

        # Cập nhật vị trí của self.rect để đồng bộ hóa với collision_rect
        self.rect.centerx = self.collision_rect.centerx
        self.rect.bottom = self.collision_rect.bottom

    def ai(self, player):
         # Chỗ này để cập nhật tầm nhìn của skeleton
        if self.direction == -1:
            self.vision.x = self.rect.centerx + 250 * self.direction
        else:
            self.vision.x = self.rect.centerx
        self.vision.y = self.rect.y
        if self.health > 0:
            if self.vision.colliderect(player.coin_collision) and player.health > 0:
                self.idling = True
                self.idling_counter = 10
                self.speed = 2
                if abs(self.rect.centerx - player.rect.centerx) > 30:
                    if self.rect.centerx > player.rect.centerx:
                        self.moving_left = True
                        self.moving_right = False
                    else:
                        self.moving_left = False
                        self.moving_right = True
                    self.move()
                else:
                    self.moving_left = False
                    self.moving_right = False
                    self.attack = True
                    if self.attack == True:
                        if self.dame_cooldown == 0:
                            player.health -= 10
                            print(player.health)
                            self.dame_cooldown = 100
                            punch.play()
                            if random.randint(1, 3) == 1:
                                player.hurt = True
            else:
                self.speed = 1
            if not self.idling and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = random.randint(60, 300)
                self.moving_left = False
                self.moving_right = False
            else:
                if not self.idling:
                    if self.direction == 1:
                        self.moving_right = True
                        self.moving_left = False
                    else:
                        self.moving_right = False
                        self.moving_left = True
                    self.move()
                    self.move_counter += 1
                    if self.move_counter > 32:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.moving_left = False
            self.moving_right = False
            self.attack = False
            self.hurt = False
            self.die = True
            self.update_action(4)
        else:
            if self.hurt:
                self.update_action(3)
            elif self.attack:
                self.update_action(2)
            elif self.moving_left or self.moving_right:
                self.update_action(1)
            else:
                self.update_action(0)
        if self.dame_cooldown > 0:
            self.dame_cooldown -= 1

    def draw(self, player):
        self.update()
        self.update_animation()
        self.ai(player)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, 'Red', self.collision_rect, 1)
        pygame.draw.rect(screen, 'Black', self.rect, 1)
        pygame.draw.rect(screen, 'Yellow', self.vision, 1)

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        folder_path = 'Entity/Boss'
        animation_types = ['Idle', 'Walk', 'Attack', 'Hurt', 'Die']
        self.action = 0
        self.frame_index = 0
        self.animation_list = []
        for animation in animation_types:
            temp_list = []
            # Đếm trong thư mục image có bao nhiêu file ảnh
            number_frame = len(os.listdir(f'{folder_path}/{animation}'))
            for i in range(1, number_frame + 1):
                image = pygame.image.load(f'{folder_path}/{animation}/{i}.png').convert_alpha()
                frames = image.subsurface(0, 0, BOSS_WIDTH, BOSS_HEIGHT - 18 * scale)
                temp_list.append(frames)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Define variable movement
        self.moving_left = False
        self.moving_right = False
        self.attack = False
        self.hurt = False
        self.die = False
        self.speed = 1
        self.vel_y = 0
        # Define max value
        self.max_health = 3000
        self.max_dame = 100
        # Define variable
        self.health = self.max_health
        self.dame = self.max_dame
        # Define variable timer and direction
        self.update_time = pygame.time.get_ticks()
        self.direction = -1
        self.flip = False
        # Defind ai variable
        self.idling = False
        self.idling_counter = 0
        self.move_counter = 0
        self.dame_cooldown = 0
        # Define variable to check collision
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.collision_rect = pygame.Rect(self.rect.centerx - 10 * scale, self.rect.centery + 20 * scale, 20 * scale, 60 * scale)
        # Define variable to check vision player
        self.vision = pygame.Rect(0, 0, 250, self.height)

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION - 20:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.attack:
                self.attack = False
                self.update_action(0)
            elif self.hurt:
                self.hurt = False
                self.update_action(0)
            elif self.die:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def move(self):
        dx = 0
        dy = 0

        # Điều chỉnh theo hướng di chuyển
        if self.moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = True
        if self.moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = False

        # Thêm trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Kiểm tra va chạm
        for tile in world.obstacle_list:
            # Trục x
            if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width, self.collision_rect.height):
                dx = 0
            # Trục y
            if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width, self.collision_rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.collision_rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.collision_rect.bottom

        # Ngăn chặn đập đầu dô tường
        if self.collision_rect.left + dx < 0 or self.collision_rect.right + dx > SCREEN_WIDTH:
            dx = 0

        # Cập nhật vị trí của collision_rect
        self.collision_rect.x += dx
        self.collision_rect.y += dy

        # Cập nhật vị trí của self.rect để đồng bộ hóa với collision_rect
        self.rect.centerx = self.collision_rect.centerx
        self.rect.bottom = self.collision_rect.bottom

    def ai(self, player):
        # Chỗ này để cập nhật tầm nhìn của skeleton
        if self.direction == -1:
            self.vision.x = self.rect.centerx + 250 * self.direction
        else:
            self.vision.x = self.rect.centerx
        self.vision.y = self.rect.y
        if self.health > 0:
            if self.vision.colliderect(player.coin_collision) and player.health > 0:
                self.idling = True
                self.idling_counter = 10
                self.speed = 2
                if abs(self.rect.centerx - player.rect.centerx) > 30:
                    if self.rect.centerx > player.rect.centerx:
                        self.moving_left = True
                        self.moving_right = False
                    else:
                        self.moving_left = False
                        self.moving_right = True
                    self.move()
                else:
                    self.moving_left = False
                    self.moving_right = False
                    self.attack = True
                    if self.attack == True:
                        if self.dame_cooldown == 0:
                            player.health -= self.max_dame
                            print(player.health)
                            self.dame_cooldown = 100
                            punch.play()
                            if random.randint(1, 3) == 1:
                                player.hurt = True
            else:
                self.speed = 1
            if not self.idling and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = random.randint(60, 300)
                self.moving_left = False
                self.moving_right = False
            else:
                if not self.idling:
                    if self.direction == 1:
                        self.moving_right = True
                        self.moving_left = False
                    else:
                        self.moving_right = False
                        self.moving_left = True
                    self.move()
                    self.move_counter += 1
                    if self.move_counter > 32:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.moving_left = False
            self.moving_right = False
            self.attack = False
            self.hurt = False
            self.die = True
            self.update_action(4)
        else:
            if self.hurt:
                self.update_action(3)
            elif self.attack:
                self.update_action(2)
            elif self.moving_left or self.moving_right:
                self.update_action(1)
            else:
                self.update_action(0)
        if self.dame_cooldown > 0:
            self.dame_cooldown -= 1

    def draw(self, player):
        self.update()
        self.update_animation()
        self.ai(player)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, 'Red', self.collision_rect, 1)
        pygame.draw.rect(screen, 'Black', self.rect, 1)
        pygame.draw.rect(screen, 'Yellow', self.vision, 1)
        # Vẽ thanh máu trên đầu
        pygame.draw.rect(screen, 'Red', (self.rect.x, self.rect.y - 20, self.rect.width, 10))
        pygame.draw.rect(screen, 'Green', (self.rect.x, self.rect.y - 20, self.rect.width * (self.health / self.max_health), 10))


class Shop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = pygame.image.load('Decoration/shop.png').convert_alpha()
        number_frames = sprite_sheet.get_width() // SHOP_WIDTH
        self.animation_list = []
        self.frame_index = 0
        for i in range(number_frames):
            frames = sprite_sheet.subsurface(i * SHOP_WIDTH, 0, SHOP_WIDTH, SHOP_HEIGHT)
            self.animation_list.append(frames)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.update_time = pygame.time.get_ticks()

    def update_animation(self):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

    def draw(self):
        self.rect.x += screen_scroll
        self.update_animation()
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, 'Black', self.rect, 1)

class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)

class Fence(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'Decoration/fence_{type}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def draw(self):
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)

class Grass(pygame.sprite.Sprite):
    def __init__(self,type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'Decoration/grass_{type}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def draw(self):
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)

class Lamp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Decoration/lamp.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.5), int(self.image.get_height() * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def draw(self):
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)

class Rock(pygame.sprite.Sprite):
    def __init__(self,type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'Decoration/rock_{type}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def draw(self):
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = pygame.image.load('Decoration/coin.png').convert_alpha()
        self.animation_list = []
        number_frames = sprite_sheet.get_width() // COIN_WIDTH
        for i in range(number_frames):
            frames = sprite_sheet.subsurface(i * COIN_WIDTH, 0, COIN_WIDTH, COIN_HEIGHT)
            self.animation_list.append(frames)
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.update_time = pygame.time.get_ticks()

    def update(self, screen_scroll):
        self.rect.x += screen_scroll  # Di chuyển theo màn hình cuộn

    def draw(self):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
        screen.blit(self.image, self.rect)

class NextLevel(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)


''' ----------------------- Dữ liệu thế giới ----------------------- '''
class World:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, world_data):
        self.level_length = len(world_data[0])
        player = None
        for y, row in enumerate(world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)  # Tuple
                    if (tile >= 0 and tile <= 4) or (tile >= 9 and tile <= 17) or (tile >= 19 and tile <= 20):
                        self.obstacle_list.append(tile_data)
                    elif tile == 22:
                        rock = Rock(1, img_rect.x, img_rect.y)
                        rock_group.add(rock)
                    elif tile == 23:
                        rock = Rock(2, img_rect.x, img_rect.y)
                        rock_group.add(rock)
                    elif tile == 24:
                        rock = Rock(3, img_rect.x, img_rect.y)
                        rock_group.add(rock)
                    # Grass
                    elif tile == 25:
                        grass = Grass(1, img_rect.x, img_rect.y)
                        grass_group.add(grass)
                    elif tile == 26:
                        grass = Grass(2, img_rect.x, img_rect.y)
                        grass_group.add(grass)
                    elif tile == 27:
                        grass = Grass(3, img_rect.x, img_rect.y)
                        grass_group.add(grass)
                    # Lamp
                    elif tile == 28:
                        lamp = Lamp(img_rect.x, img_rect.y)
                        lamp_group.add(lamp)
                    # Fence
                    elif tile == 29:
                        fence = Fence(1, img_rect.x, img_rect.y)
                        fence_group.add(fence)
                    elif tile == 30:
                        fence = Fence(2, img_rect.x, img_rect.y)
                        fence_group.add(fence)
                    elif tile == 31: # Shop
                        shop = Shop(img_rect.x, img_rect.y)
                        shop_group.add(shop)
                    # Next Level
                    elif tile == 32:
                        next_level = NextLevel(img_rect.x, img_rect.y, img)
                        level_complete_group.add(next_level)
                    elif tile == 33: # Skeleton
                        skeleton = Skeleton(img_rect.x, img_rect.y, 1)
                        skeleton_group.add(skeleton)
                    elif tile == 34: # Player
                        player = Player(img_rect.x, img_rect.y, 0.75)
                    # Coin
                    elif tile == 35:
                        coin = Coin(img_rect.x, img_rect.y)
                        coin_group.add(coin)
                    elif tile == 36:
                        bigger = Bigger(img_rect.x, img_rect.y, 1)
                        bigger_group.add(bigger)
                    elif tile == 37:
                        demon = Demon(img_rect.x, img_rect.y, 1)
                        demon_group.add(demon)
                    elif tile == 38:
                        boss = Boss(img_rect.x, img_rect.y, 1)
                        boss_group.add(boss)
                    else:
                        decoration = Decoration(img_rect.x, img_rect.y, img)
                        decoration_group.add(decoration)

        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1].x += screen_scroll
            screen.blit(tile[0], tile[1])

''' ----------------------- Chuẩn bị thành phần cho main game -----------------------'''
# Tạo mảng lưu các tile trong map
img_list = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f'Map/Tile/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# Lưu trữ các nút trong map editor
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(WIDTH_MAP + 10 + button_col * TILE_SIZE + button_col * 10, 10 + button_row * TILE_SIZE + button_row * 10, img_list[i], img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 7:
		button_row += 1
		button_col = 0
# Hàm vẽ chữ
def draw_text(text, font, color, x, y):
    # Transform string to img
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Hàm vẽ background để tạo hiệu ứng 3D dựa trên các layer
def draw_bg():
    width = layer_1.get_width()
    for i in range(20):
        screen.blit(bg_1, ((i * width) - bg_scroll * 0.5, 0))
        screen.blit(bg_2, ((i * width) - bg_scroll * 0.6, 0))
        screen.blit(bg_3, ((i * width) - bg_scroll * 0.7, 0))

# Dùng để reset level khi chơi lại hoặc qua màn mới
def reset_level():
    # Các nhóm sprite rỗng
    decoration_group.empty()
    fence_group.empty()
    grass_group.empty()
    lamp_group.empty()
    rock_group.empty()
    shop_group.empty()
    coin_group.empty()
    skeleton_group.empty()
    bigger_group.empty()
    demon_group.empty()
    boss_group.empty()
    level_complete_group.empty()
    # Tạo lại mảng rỗng
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

def map_editor():
    action_edit = True
    global current_tile
    global scroll
    global scroll_left
    global scroll_right
    global scroll_speed
    global main_game
    global level
    global MAX_LEVELS
    global player
    screen.fill(GRAY)
    # Chỗ này dùng để vẽ chữ nè
    draw_text(f'Current Level: {level}', font, WHITE, 10, HEIGHT_MAP + 5)
    draw_text(f'Curent Tile: {current_tile}', font, WHITE, 10, HEIGHT_MAP + 20)
    draw_text('Press UP/DOWN to change level', font, WHITE, 10, HEIGHT_MAP + 35)
    draw_text('Press LEFT/RIGHT to scroll map', font, WHITE, 10, HEIGHT_MAP + 50)
    draw_text('Press ESC to return to main menu', font, BLACK, 10, HEIGHT_MAP + 65)
    # Vẽ cái nền chỗ cso thể thêm tile vào map
    num_tiles = (COLS * TILE_SIZE) // WIDTH_MAP + 1
    for i in range(num_tiles):
        surface.blit(layer_1, ((i * WIDTH_MAP) - scroll * 0.5, 0))
        surface.blit(layer_2, ((i * WIDTH_MAP) - scroll * 0.6, 0))
        surface.blit(layer_3, ((i * WIDTH_MAP) - scroll * 0.7, 0))
    # Vẽ cái lưới chỗ map
    for i in range(ROWS + 1):
        pygame.draw.line(surface, (255, 255, 255), (0, i * TILE_SIZE_MAP ), (WIDTH_MAP, i * TILE_SIZE_MAP))
    for j in range(COLS + 1):
        pygame.draw.line(surface, (255, 255, 255), (j * TILE_SIZE_MAP - scroll, 0), (j * TILE_SIZE_MAP - scroll, HEIGHT_MAP))
    # Vẽ thế giới vào trong chỗ map
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                surface.blit(img_list[tile], (x * TILE_SIZE_MAP - scroll, y * TILE_SIZE_MAP))

    # Nút load mop
    if load_btn.draw(screen):
        scroll = 0
        with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    # Nút lưu map
    if save_btn.draw(screen):
        with open(f'Level/level{level}_data.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)

    # Vẽ mấy cái nút ngoài viền bên phải nè =)))
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    # Tô đậm nút ấn hiện tại
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)


    # Di chuyển bản đồ
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (COLS * TILE_SIZE_MAP) - WIDTH_MAP:
        scroll += 5 * scroll_speed

    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE_MAP
    y = pos[1] // TILE_SIZE_MAP
    # Kiểm tra xem chuột có nằm trong vùng vẽ không
    if pos[0] < (704) and pos[1] < (416):
        # Cập nhật tile vào world data
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_UP and level < MAX_LEVELS:
                level += 1
            if event.key == pygame.K_DOWN and level > 1:
                level -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
        # Exit map editor
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                action_edit = False
                # Cập nhật lại dữ liệu thế giới
                world = World()
                player = world.process_data(world_data)
                main_game = False
        # Exit pygame
        if event.type == pygame.QUIT:
            pygame.quit()
    # Update to screen
    screen.blit(surface, (0, 0))

    return action_edit, main_game

# Các hàm áp dụng lên các nhóm sprite
def draw_enemy(player):
    for skeleton in skeleton_group:
        skeleton.draw(player)
    for bigger in bigger_group:
        bigger.draw(player)
    for demon in demon_group:
        demon.draw(player)
    for boss in boss_group:
        boss.draw(player)

def draw_decoration():
    for decoration in decoration_group:
        decoration.draw()
    for rock in rock_group:
        rock.draw()
    for grass in grass_group:
        grass.draw()
    for lamp in lamp_group:
        lamp.draw()
    for fence in fence_group:
        fence.draw()
    for coin in coin_group:
        coin.draw()
    for next_level in level_complete_group:
        next_level.draw()

def draw_shop():
    for shop in shop_group:
        shop.draw()

def draw_coin():
    for coin in coin_group:
        coin.draw()

def bullet_enemy(player):
    for bullet in player.bullets:
        for skeleton in skeleton_group:
            if bullet.rect.colliderect(skeleton.collision_rect):
                if skeleton.health > 0:
                    skeleton.health -= player.dame + dame_bullet
                    skeleton.hurt = True
                    player.bullets.remove(bullet)
                    hurt.play()
        for bigger in bigger_group:
            if bullet.rect.colliderect(bigger.collision_rect):
                if bigger.health > 0:
                    bigger.health -= player.dame + dame_bullet
                    bigger.hurt = True
                    player.bullets.remove(bullet)
                    hurt.play()
        for demon in demon_group:
            if bullet.rect.colliderect(demon.collision_rect):
                if demon.health > 0:
                    demon.health -= player.dame + dame_bullet
                    demon.hurt = True
                    player.bullets.remove(bullet)
                    hurt.play()
        for boss in boss_group:
            if bullet.rect.colliderect(boss.collision_rect):
                if boss.health > 0:
                    boss.health -= player.dame + dame_bullet
                    boss.hurt = True
                    player.bullets.remove(bullet)
                    hurt.play()

def health_chart(player):
    number_tiles = player.health // health_tile
    step = 0
    for i in range(number_tiles):
        if i  == 5:
            step = 10
        if i == 10:
            step = 21
        screen.blit(chart_health, (76 + i * 16 + step, 33))

def bullet_char(player):
    for i in range(player.bullet):
        screen.blit(bullet_image, (10 + i * 10, 100))

# Tạo mảng data rỗng dùng để chứa dữ liệu thế giới
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# Đọc dữ liệu lên mảng vừa tạo
with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


world = World()
player = world.process_data(world_data)

'''Gangster ở cửa sổ chính'''
GangsterMain = Player(835, 325, 1.5)
CoinBarPlayer = CoinBar(10, 74)
# Vòng lặp chính
running = True
while running:
    # Cài đặt FPS
    clock.tick(FPS)

    if not main_game:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, 'Black', (510, 48, 354, 374))
        screen.blit(setting_game_image, (512, 50))
        GangsterMain.draw()
        if play.draw(screen):
            main_game = True
            play_game = True
        if option.draw(screen):
            main_game = True
            option_game = True
        if exit.draw(screen):
            exit_game = True
            main_game = True
    else:
        if option_game:
            option_game, main_game = map_editor()
        if exit_game:
            running = False
        if play_game:
            draw_bg()
            world.draw()
            draw_shop()
            draw_decoration()
            screen.blit(empty_heath_bar, (10, 10))
            CoinBarPlayer.draw()
            health_chart(player)
            bullet_char(player)
            draw_text(f'x {coin_player}', font, WHITE, 15 + CoinBarPlayer.image.get_width(), 79)
            # Nếu có người chơi
            if player:
                player.draw()
                draw_enemy(player)
                coin_group.update(screen_scroll)
                draw_coin()
                bullet_enemy(player)
                screen_scroll = player.move()
                bg_scroll -= screen_scroll

                # Kiểm tra coi người chơi chạm với đồng xu
                for coin in coin_group:
                    if coin.rect.colliderect(player.coin_collision):
                        coin_group.remove(coin)
                        coin_player += 1
                        coin_recieved.play()

                # Kiểm tra va chạm với mấy cái cửa hàng
                for shop in shop_group:
                    if shop.rect.colliderect(player.coin_collision):
                        screen.blit(board, (870, 10))
                        # Ghi thông tin người chơi
                        draw_text('Info Player', font, 'White', 900, 20)
                        draw_text(f'Health: {player.health}', font, 'White', 880, 50)
                        draw_text(f'Max Health: {player.max_health}', font, 'White', 880, 75)
                        draw_text(f'Bullet speed: {speed_bullet}', font, 'White', 880, 105)
                        draw_text(f'Dame bonus: {dame_bullet}', font, 'White', 880, 135)
                        draw_text(f'Cooldown: {bullet_cooldown}', font, 'White', 880, 165)
                        pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 208, 150, 20))
                        draw_text('+ 1 Dame: 10 xu', font, 'Black', SCREEN_WIDTH - 200, 210)
                        pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 258, 150, 20))
                        draw_text('+ 15 Health: 10 xu', font, 'Black', SCREEN_WIDTH - 200, 260)
                        pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 308, 150, 20))
                        draw_text('+ Speed BL: 15 xu', font, 'Black', SCREEN_WIDTH - 200, 310)
                        pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 358, 150, 20))
                        draw_text('+ Full HP: 5 xu', font, 'Black', SCREEN_WIDTH - 200, 360)
                        pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 408, 150, 20))
                        draw_text('+ Cooldown: 5 xu', font, 'Black', SCREEN_WIDTH - 200, 410)
                        if dame_upgrade.draw(screen):
                            if coin_player >= 10:
                                dame_bullet += 1
                                coin_player -= 10
                        if health_upgrade.draw(screen):
                            if coin_player >= 10:
                                player.max_health += 15
                                health_tile += 1
                                coin_player -= 10
                        if speed_bullet_upgrade.draw(screen):
                            if coin_player >= 15 and speed_bullet < 2:
                                speed_bullet += 1
                                coin_player -= 15
                        if recover_health_upgrade.draw(screen):
                            if coin_player >= 5:
                                player.health = player.max_health
                                coin_player -= 5
                        if cooldown_upgrade.draw(screen):
                            if coin_player >= 5 and bullet_cooldown < 30:
                                bullet_cooldown += 1
                                coin_player -= 5

                # Lấy sự kiện từ người chơi
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.type == pygame.K_ESCAPE:
                            running = False
                    # Sự kiện người chơi
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            player.moving_left = True
                        if event.key == pygame.K_d:
                            player.moving_right = True
                        if event.key == pygame.K_w and player.in_air == False:
                            player.move_jump = True
                            jump.play()
                        if event.key == pygame.K_j:
                            player.punch = True
                        if event.key == pygame.K_LCTRL:
                            player.run = True
                        if event.key == pygame.K_SPACE and player.shoot_cooldown == 0 and player.bullet > 0:
                            player.shoot = True
                            player.gun()
                            shot.play()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            player.moving_left = False
                        if event.key == pygame.K_d:
                            player.moving_right = False
                        if event.key == pygame.K_w:
                            player.move_jump = False
                        if event.key == pygame.K_j:
                            player.punch = False
                        if event.key == pygame.K_LCTRL:
                            player.run = False

                if home_btn.draw(screen):
                    main_game = False
                    play_game = False
                    # Reset lại dữ liệu thế giới
                    world_data = reset_level()
                    # Tải level mới
                    level = 1
                    with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)

                # Kiểm tra coi người chơi có chạm vô cục next Level không
                for pos in level_complete_group:
                    if player.coin_collision.colliderect(pos.rect):
                        level += 1
                        if play_audio == False:
                                win_game.play()
                                play_audio = True
                        if level < MAX_LEVELS:
                            play_audio = False
                            bg_scroll = 0
                            world_data = reset_level()
                            # Tải level mới
                            with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                                reader = csv.reader(csvfile, delimiter = ',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player = world.process_data(world_data)

                if player.health <= 0:
                    if play_audio == False:
                        game_over_audio.play()
                        play_audio = True
                    if menu_btn.draw(screen):
                        main_game = False
                        play_game = False
                        play_audio = False
                        world_data = reset_level()
                        # Tải level mới
                        with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)
                    if restart_btn.draw(screen):
                        bg_scroll = 0
                        play_audio = False
                        world_data = reset_level()
                        # Tải level mới
                        with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)



    # Vòng lặp lấy sự kiện bên ngoài
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Cập nhật lại màn hình
    pygame.display.update()

pygame.quit()