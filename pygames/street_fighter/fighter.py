import pygame
import random

dbclock = pygame.time.Clock()


class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_power = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 200
        self.alive = True
        self.should_move = False
        self.should_attack = False

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.size, y * self.size, self.size, self.size
                )
                temp_img_list.append(
                    pygame.transform.scale(
                        temp_img,
                        (self.size * self.image_scale, self.size * self.image_scale),
                    )
                )
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 6
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get keypresses
        key = pygame.key.get_pressed()

        # can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False:
            # check player controls
            if self.player == 1:
                # movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_SPACE] and self.jump == False:
                    self.vel_y = -25
                    self.jump = True
                if (
                    key[pygame.K_e]
                    or key[pygame.K_r]
                    or key[pygame.K_q]
                    or key[pygame.K_w]
                ):
                    self.attack(target)
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_r]:
                        self.attack_type = 2
                    if key[pygame.K_q]:
                        self.attack_type = 4
                    if key[pygame.K_w]:
                        self.attack_type = 6
                if pygame.mouse.get_pressed()[0]:
                    self.attack(target)
                    self.attack_type = 3
                if key[pygame.K_q] and pygame.mouse.get_pressed()[0]:
                    self.attack(target)
                    self.attack_type = 5
            # if self.player == 2:
            #     # movement
            #     if key[pygame.K_LEFT]:
            #         dx = -SPEED
            #         self.running = True
            #     if key[pygame.K_RIGHT]:
            #         dx = SPEED
            #         self.running = True
            #     # jump
            #     if key[pygame.K_UP] and self.jump == False:
            #         self.vel_y = -25
            #         self.jump = True
            #     if key[pygame.K_KP1] or key[pygame.K_KP0]:
            #         self.attack(target)
            #         if key[pygame.K_KP1]:
            #             self.attack_type = 1
            #         if key[pygame.K_KP0]:
            #             self.attack_type = 2

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 160:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 160 - self.rect.bottom

        # ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # update player position
        self.rect.x += dx
        self.rect.y += dy

        if self.player == 1:
            if self.alive == False:
                self.rect.y = 330

    def ai(self, target, round_over):
        TARGET_DISTANCE = abs(self.rect.x - target.rect.x)
        if self.flip == False:
            MOVE_DIR = -1
        else:
            MOVE_DIR = 1
        attacking_rect = pygame.Rect(
            self.rect.centerx - (2 * self.rect.width * self.flip),
            self.rect.y,
            2 * self.rect.width,
            self.rect.height,
        )

        if self.attacking == False and self.alive == True and round_over == False:
            # Attack
            if target.attacking == False:
                    if TARGET_DISTANCE >= attacking_rect.width:
                            self.running = True
                            self.rect.move_ip(-3 * MOVE_DIR, 0)
            else:
                self.should_attack = random.choice([True, False, False])
                if TARGET_DISTANCE <= attacking_rect.width and target.jump == False:
                        self.attack(target)
                        self.attack_type = 1

    # handle animation updates
    def update(self, target):
        # check what action the player is performing
        if self.player == 1:
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.update_action(8)
            elif self.attacking == True:
                if self.attack_type == 1:  # Punch1
                    self.update_action(2)
                elif self.attack_type == 2:  # Combo Punch
                    self.update_action(1)
                elif self.attack_type == 3:  # Figma Punch
                    self.update_action(3)
                elif self.attack_type == 4:  # Normal Kick
                    self.update_action(5)
                elif self.attack_type == 5:  # Combo Kick
                    self.update_action(4)
                elif self.attack_type == 6:  # Chhotu Kick
                    self.update_action(6)
            elif self.jump == True:
                self.update_action(0)
            elif self.running == True:
                self.update_action(7)
            else:
                self.update_action(0)
        elif self.player == 2:
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.update_action(3)
            elif self.attacking == True:
                if self.attack_type == 1:  # Punch1
                    self.update_action(2)
            elif self.running == True:
                self.update_action(1)
            else:
                self.update_action(0)

        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack was executed
                if self.player == 1:
                    if (
                        self.action == 1
                        or self.action == 2
                        or self.action == 3
                        or self.action == 4
                        or self.action == 5
                        or self.action == 6
                    ):
                        self.attacking = False
                        self.attack_cooldown = 20
                    if target.hit == True:
                        if self.action == 1:
                            target.health -= 22
                        if self.action == 2:
                            target.health -= 12
                        if self.action == 3:
                            target.health -= 25
                        if self.action == 4:
                            target.health -= 18
                        if self.action == 5:
                            target.health -= 15
                        if self.action == 6:
                            target.health -= 12
                if self.player == 2:
                    if self.action == 2:
                        self.attacking = False
                        self.attack_cooldown = 100
                    if target.hit == True:
                        if self.action == 2:
                            target.health -= 20

    def load_ranged_attack(self, surface, target, img):
        if self.player == 2:
            if self.action == 2:
                surface.blit(
                    pygame.transform.scale_by(img, 0.5),
                    (
                        target.rect.x - 50,
                        self.rect.top,
                        self.rect.width / 4,
                        self.rect.height / 4,
                    ),
                )

    def menu_character(self, surface):
        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.action += 1
            if self.action > len(self.animation_list[self.action]):
                self.action = 0
        surface.blit(pygame.transform.scale_by(self.image, 1.25), (350, 150))

    def attack(self, target):
        if self.attack_cooldown == 0:
            # execute attack
            self.attacking = True
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                1 * self.rect.width,
                self.rect.height,
            )
            if attacking_rect.colliderect(target.rect):
                target.hit = True
            else:
                target.hit = False

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(
            img,
            (
                self.rect.x - (self.offset[0] * self.image_scale),
                self.rect.y - (self.offset[1] * self.image_scale),
            ),
        )
