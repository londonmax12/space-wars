# Import libaries 
import pygame 
import random
import math
import time
# Initialize pygame
pygame.init()
pygame.font.init()

current = 0

# Defines constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_GREY = (128, 128, 128)

# Sets up the screen
sizeX, sizeY = 800, 800
size = (sizeX, sizeY)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Space Wars")
player = pygame.image.load("player.png")
#player.set_colorkey(BLACK)
pygame.display.set_icon(player)
screen.convert_alpha()

# Custom cursor
pygame.mouse.set_visible(False)

# Defines starting variables
done = False
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('Franklin Gothic Medium', 30)
font2 = pygame.font.SysFont('Franklin Gothic Medium', 15)
plrX = sizeX / 2 # Starting player x
plrY = sizeY / 2 # Starting player y
current_cooldown = 0
cooldown = 25 # Delay between shots
cooldownW = 0 # Drift cooldown
cooldownS = 0 
cooldownA = 0
cooldownD = 0
plrVelocity = 4 # Movement speed
in_game = 0
shoot_speed = 23 # How fast the shot travels
initial_life = 0
sides = ["top", "bottom", "left", "right"] # Defines areas for random meteor spawning
coins = 0
powerup_time_1 = 0
powerup_time_2 = 0
powerup_time_3 = 0
lives = 0
level = 1
enemies_killed = 0
enemy_cooldown = 0
paused = False
won = False

mousePos = pygame.mouse.get_pos()
player_pos  = (plrX, plrY)
player_rect = player.get_rect(center = player_pos)
mx, my = pygame.mouse.get_pos()
dx, dy = mx - player_rect.centerx, my - player_rect.centery
angle = math.degrees(math.atan2(-dy, dx)) - 90


# Load images
bullet_projectile = pygame.image.load("projectile.png")
projectile_boosted = pygame.image.load("projectile_boosted.png")
bg = pygame.image.load("background.png").convert()
cursor_image = pygame.image.load("cursor.png")
small_meteor = pygame.image.load("meteor4.png")
medium_meteor1 = pygame.image.load("meteor3.png")
medium_meteor2 = pygame.image.load("meteor2.png")
large_meteor = pygame.image.load("meteor1.png")
logo = pygame.image.load("spacewars.png")
powerup1 = pygame.image.load("powerup-shoot.png")
powerup2 = pygame.image.load("powerup-speed.png")
powerup3 = pygame.image.load("powerup-shield.png")
forcefield_image = pygame.image.load("forcefield.png")
play_b = pygame.image.load("play-button.png")
play_bp = pygame.image.load("play-button-selected.png")
life = pygame.image.load("life.png")
player_boosted = pygame.image.load("player-boosted.png")
cancel_button_image = pygame.image.load("cancel.png")
win = pygame.image.load("win-screen.png")

# Load audio
shotsfx = pygame.mixer.Sound("shot.mp3")
meteorsfx = pygame.mixer.Sound("meteor.mp3")
powerupsfx = pygame.mixer.Sound("powerup.mp3")

# Entity classes
class projectile(pygame.sprite.Sprite):
    def __init__(self, speed, rotation, x, y, mx, my, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.speed = speed
        self.rotation = rotation
        self.rect = self.image.get_rect(center = (x, y))
        self.x = x - self.rect.width / 2
        self.y = y - self.rect.height / 2
        offset = abs((mx - x)) + abs((my - y))
        ratio = speed/offset
        self.x_movement = (mx - x)*ratio
        self.y_movement = (my - y)*ratio        
        self.alive = True
    def draw(self):
        rot_image = pygame.transform.rotate(self.image, self.rotation)
        rot_image_rect = rot_image.get_rect(center = self.rect.center)
        screen.blit(rot_image, rot_image_rect.topleft)
    def move(self):
        self.x += self.x_movement
        self.y += self.y_movement
        self.rect.x = self.x
        self.rect.y = self.y

class spaceship():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.alive = True
        self.rect = player.get_rect(center = (x, y))
        self.image = player
    def draw(self, x, y, angle):
        self.rect.x = x - 56
        self.rect.y = y - 37
        rot_image = pygame.transform.rotate(self.image, angle)
        rot_image_rect = rot_image.get_rect(center = self.rect.center)
        screen.blit(rot_image, rot_image_rect.topleft)
        #pygame.draw.rect(screen, (0, 255, 0), self.rect)
        
class small_meteor_spawn(pygame.sprite.Sprite):
    def __init__ (self, targetX, targetY, speed, sidespawned, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rotation = random.randrange(0, 360)
        self.image = small_meteor
        self.size = (self.image.get_width(), self.image.get_height())

        self.targetX = targetX
        self.targetY = targetY

        self.side = random.choice(sides)
        if sidespawned == True:            
            if self.side == "top":
                y = 1
                x = random.randrange(sizeX)
            elif self.side == "bottom":
                y = sizeY - 1
                x = random.randrange(sizeX)
            elif self.side == "left":
                y = random.randrange(sizeY)
                x = 1
            elif self.side == "right":
                y = random.randrange(sizeY)
                x = sizeX - 1
        else:
            if self.side == "top":
                self.targetY = 1
                self.targetX = random.randrange(sizeX)
            elif self.side == "bottom":
                self.targetY = sizeY - 1
                self.targetX = random.randrange(sizeX)
            elif self.side == "left":
                self.targetY = random.randrange(sizeY)
                self.targetX = 1
            elif self.side == "right":
                self.targetY = random.randrange(sizeY)
                self.targetX = sizeX - 1
        
        self.rect = self.image.get_rect(center = (x, y))
        self.x = x - self.rect.width / 2
        self.y = y - self.rect.height / 2
        self.speed = speed
        dx, dy = self.targetX - self.x, self.targetY - self.y
        #offset = abs(dx) + abs(dy)
        #ratio = speed/offset

        self.angle = math.atan2(dy, dx)
        self.alive = True
        
    def draw(self):
        #self.rect = small_meteor.get_rect(center = self.projectile_pos)
        rot_image = pygame.transform.rotate(small_meteor, self.rotation)
        rot_image_rect = rot_image.get_rect(center = self.rect.center)        
        screen.blit(rot_image, (self.x, self.y))
        #pygame.draw.rect(screen, (0, 255, 0), self.rect)
    def move(self):
        x_movement = self.speed * math.cos(self.angle)
        y_movement = self.speed * math.sin(self.angle)
        self.x += x_movement
        self.y += y_movement
        self.rect.x = self.x
        self.rect.y = self.y
    def stepback(self):
        x_movement = self.speed * math.cos(self.angle)
        y_movement = self.speed * math.sin(self.angle)
        self.x -= x_movement
        self.y -= y_movement
        self.rect.x = self.x
        self.rect.y = self.y

class medium_meteor_spawn(pygame.sprite.Sprite):
    def __init__ (self, targetX, targetY, speed, sidespawned, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.rotation = random.randrange(0, 360)
        imagerand = random.randrange(1,2)
        self.targetX = targetX
        self.targetY = targetY
        if imagerand == 1:
            self.image = medium_meteor1
        else:
            self.image = medium_meteor2
            
        self.side = random.choice(sides)
        if sidespawned == True:
            if self.side == "top":
                y = 1
                x = random.randrange(sizeX)
            elif self.side == "bottom":
                y = sizeY - 1
                x = random.randrange(sizeX)
            elif self.side == "left":
                y = random.randrange(sizeY)
                x = 1
            elif self.side == "right":
                y = random.randrange(sizeY)
                x = sizeX - 1
        else:         
            if self.side == "top":
                self.targetY = -50
                self.targetX = random.randrange(sizeX)
            elif self.side == "bottom":
                self.targetY = sizeY + 50
                self.targetX = random.randrange(sizeX)
            elif self.side == "left":
                self.targetY = random.randrange(sizeY)
                self.targetX = -50
            elif self.side == "right":
                self.targetY = random.randrange(sizeY)
                self.targetX = sizeX + 50
                
        self.rect = self.image.get_rect(center = (x, y))
        self.x = x - self.rect.width / 2
        self.y = y - self.rect.height / 2
        self.speed = speed
        offset = abs((self.targetX - x)) + abs((self.targetY - y))
        ratio = speed/offset
        self.x_movement = (self.targetX - x)*ratio
        self.y_movement = (self.targetY - y)*ratio
        self.alive = True
    def draw(self):
        rot_image = pygame.transform.rotate(self.image, self.rotation)
        rot_image_rect = rot_image.get_rect(center = self.rect.center)        
        screen.blit(rot_image, (self.x, self.y))
        #pygame.draw.rect(screen, (0, 255, 0), self.rect)
    def move(self):
        self.x += self.x_movement
        self.y += self.y_movement
        self.rect.x = self.x
        self.rect.y = self.y        
    def split(self):
        small_meteors.append(small_meteor_spawn(plrX, plrY, 2, False, self.x + self.rect.width / 2, self.y + self.rect.height / 2))
        small_meteors.append(small_meteor_spawn(plrX, plrY, 2, False, self.x + self.rect.width / 2, self.y + self.rect.height / 2))
        self.alive = False

class large_meteor_spawn(pygame.sprite.Sprite):
    def __init__ (self, targetX, targetY, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.rotation = random.randrange(0, 360)
        self.image = large_meteor 
        self.side = random.choice(sides)
        if self.side == "top":
            y = -100
            x = random.randrange(sizeX)
        elif self.side == "bottom":
            y = sizeY - 1
            x = random.randrange(sizeX)
        elif self.side == "left":
            y = random.randrange(sizeY)
            x = 1
        elif self.side == "right":
            y = random.randrange(sizeY)
            x = sizeX - 1
        self.rect = self.image.get_rect(center = (x, y))
        self.x = x - self.rect.width / 2
        self.y = y - self.rect.height / 2
        self.speed = speed
        offset = abs((targetX - x)) + abs((targetY - y))
        ratio = speed/offset
        self.x_movement = (targetX - x)*ratio
        self.y_movement = (targetY - y)*ratio
        self.alive = True
    def draw(self):
        rot_image = pygame.transform.rotate(self.image, self.rotation)
        rot_image_rect = rot_image.get_rect(center = self.rect.center)        
        screen.blit(rot_image, (self.x, self.y))
        #pygame.draw.rect(screen, (0, 255, 0), self.rect)
    def move(self):
        self.x += self.x_movement
        self.y += self.y_movement
        self.rect.x = self.x
        self.rect.y = self.y        
    def split(self):
        medium_meteors.append(medium_meteor_spawn(plrX, plrY, 2, False, self.x + self.rect.width / 2, self.y + self.rect.height / 2))
        self.alive = False

class powerup(pygame.sprite.Sprite):
    def __init__ (self, x, y, speed, targetX, targetY):
        self.type = random.randrange(1,4)
        if self.type == 1: # Shot speed
            self.image = powerup1
        elif self.type == 2: # Speed
            self.image = powerup2
        elif self.type == 3: # Shield
            self.image = powerup3
        self.rect = self.image.get_rect(center = (x, y))
        self.x = x
        self.y = y
        self.speed = speed
        offset = abs((targetX - x)) + abs((targetY - y))
        ratio = speed/offset
        self.x_movement = (targetX - x)*ratio
        self.y_movement = (targetY - y)*ratio
        self.alive = True
    def move(self):
        self.x += self.x_movement
        self.y += self.y_movement
        self.rect.x = self.x
        self.rect.y = self.y
    def draw(self):       
        screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(screen, (0, 255, 0), self.rect)
        
class forcefield_class(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.active = False
        self.image = forcefield_image
        self.rect = self.image.get_rect()
    def move(self):
        self.x = plrX - 65
        self.y = plrY - 67
    def draw(self):
        if self.active == True:
            screen.blit(self.image, (self.x, self.y))

class play_button(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 105
        self.y = 450
        self.image = play_b
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

class lives_icon():
    def __init__(self):
        self.y = 10
        self.x = sizeX - (40 * lives) - 10
        self.image = life
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        
class cancel_button(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 575
        self.y = 575
        self.image = cancel_button_image
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True        
# Single objects
plr = spaceship(plrX, plrY, angle)
forcefield = forcefield_class(plrX, plrY)
play = play_button()
cancel = cancel_button()

# Arrays of objects
projectiles = []
small_meteors = []
medium_meteors = []
large_meteors = []
powerups = []
lives_icons = []

# Updates the screen
def redraw_game_window():
    mousePos = pygame.mouse.get_pos()
    screen.blit(cursor_image, mousePos)
    pygame.display.flip()

# Main game Loop
while not done:
    if in_game:
        if paused == False:
            # Adds the 3 initial life icons
            if initial_life < 3:
                initial_life += 1
                lives += 1
                lives_icons.append(lives_icon())
                
            # Checks the objects are on the screen then calculates the positions
            for i in projectiles:
                if i.x < sizeX + 50 and i.x > -50 and i.y < sizeY + 50 and i.y > -50:
                    i.move()
                else:
                    i.alive = False
            for i in small_meteors:
                if i.x < sizeX + 50 and i.x > -50 and i.y < sizeY + 50 and i.y > -50:
                    i.move()
                else:
                    i.alive = False
            for i in medium_meteors:
                if i.x < sizeX + 100 and i.x > -100 and i.y < sizeY + 100 and i.y > -100:
                    i.move()
                else:
                    i.alive = False
            for i in large_meteors:
                if i.x < sizeX + 100 and i.x > -100 and i.y < sizeY + 100 and i.y > -100:
                    i.move()
                else:
                    i.alive = False 
            for i in powerups:
                if i.x < sizeX + 50 and i.x > -50 and i.y < sizeY + 50 and i.y > -50:
                    i.move()
                else:
                    i.alive = False
                
            # Moves player when WASD is pressed or if the player shoots
            keys = pygame.key.get_pressed()    
            if plrX > 0:
                if keys[pygame.K_a]:
                     plrX -= plrVelocity
            if plrX < sizeX:
                if keys[pygame.K_d]:
                     plrX += plrVelocity
            if plrY > 0:
                if keys[pygame.K_w]:
                     plrY -= plrVelocity
            if plrY < sizeY:
                if keys[pygame.K_s]:
                     plrY += plrVelocity                
            if keys[pygame.K_SPACE]:
                if current_cooldown < 1:
                    current_cooldown = cooldown
                    if powerup_time_1 > 0:
                        projectiles.append(projectile(shoot_speed, angle, plrX, plrY, mx, my, projectile_boosted))
                    else:
                        projectiles.append(projectile(shoot_speed, angle, plrX, plrY, mx, my, bullet_projectile))
                    shotsfx.play()

            if current_cooldown > 0:
                current_cooldown -= 1       
            # Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        cooldownW = 60           
                    if event.key == pygame.K_s:
                        cooldownS = 60
                    if event.key == pygame.K_a:
                        cooldownA = 60
                    if event.key == pygame.K_d:
                        cooldownD = 60

            # Draws background
            screen.blit(bg, (0, 0))
            
            # Draws array objects to screen
            for i in projectiles:
                i.draw()
            for i in small_meteors:
                i.draw()
            for i in medium_meteors:
                i.draw()
            for i in large_meteors:
                i.draw()
            for i in powerups:
                i.draw()
            for i in lives_icons:
                i.draw()
            #Calculates where and which way the player and forcefield should be then draws
            player_rect = player.get_rect(center = (plrX, plrY))
            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - player_rect.centerx, my - player_rect.centery
            angle = math.degrees(math.atan2(-dy, dx)) - 90
            forcefield.move()
            plr.draw(plrX, plrY, angle)
            forcefield.draw()
            
            # Checks if powerups are active
            if powerup_time_1 > 0:
                cooldown = 7
                powerup_time_1 -= 1
            else:
                cooldown = 25
            if powerup_time_2 > 0:
                plrVelocity = 7
                powerup_time_2 -= 1
                plr.image = player_boosted
            else:
                plrVelocity = 4
                plr.image = player
            if powerup_time_3 > 0:
                powerup_time_3 -= 1
                forcefield.active = True
                
            else:
                forcefield.active = False
                
            # Checks for collisions
            for i in projectiles:
                for m in small_meteors:
                    collision = pygame.sprite.collide_rect_ratio(0.7)(m, i)
                    if collision:
                        i.alive = False
                        meteorsfx.play()
                        coins += random.randrange(5,10)
                        enemies_killed += 1
                        if random.randrange(1,10) == 1:
                            powerups.append(powerup(m.x, m.y, 1, plrX, plrY))
                        m.alive = False
                        break
            for i in projectiles:
                for m in medium_meteors:
                    collision = pygame.sprite.collide_rect_ratio(0.8)(m, i)
                    if collision:
                        i.alive = False
                        coins += random.randrange(5,10)
                        enemies_killed += 1
                        meteorsfx.play()
                        m.split()
                        break            
            for i in projectiles:
                for l in large_meteors:
                    collision = pygame.sprite.collide_rect_ratio(0.9)(l, i)
                    if collision:
                        i.alive = False
                        enemies_killed += 1
                        coins += random.randrange(5,10)
                        meteorsfx.play()
                        l.split()
                        break   
            for m in small_meteors:
                collision = pygame.sprite.collide_rect_ratio(0.7)(m, plr)
                if collision:
                    if lives >= 1:
                        small_meteors.remove(m)
                        lives -= 1
                        del lives_icons[-1]
                    if lives < 1:
                        in_game = False
            for m in medium_meteors:
                collision = pygame.sprite.collide_rect_ratio(0.7)(m, plr)
                if collision:
                    if lives >= 1:
                        medium_meteors.remove(m)
                        lives -= 1
                        del lives_icons[-1]
                    if lives < 1:
                        done = False
            for m in large_meteors:
                collision = pygame.sprite.collide_rect_ratio(0.8)(m, plr)
                if collision:
                    if lives >= 1:
                        large_meteors.remove(m)
                        lives -= 1
                        del lives_icons[-1]
                    if lives < 1:
                        done = False
            for p in powerups:
                collision = pygame.sprite.collide_rect_ratio(0.7)(p, plr)
                if collision:
                    powerupsfx.play()
                    if p.type == 1:
                        powerup_time_1 = 500
                    if p.type == 2:
                        powerup_time_2 = 500
                    if p.type == 3:
                        powerup_time_3 = 500
                    powerups.remove(p)
            if forcefield.active == True:
                for m in small_meteors:
                    collision = pygame.sprite.collide_rect_ratio(0.9)(m, plr)        
                    if collision:
                        m.alive = False
                for m in medium_meteors:
                    collision = pygame.sprite.collide_rect_ratio(0.9)(m, plr)        
                    if collision:
                        m.alive = False
                for m in large_meteors:
                    collision = pygame.sprite.collide_rect_ratio(1)(m, plr)        
                    if collision:
                        m.alive = False
                        
            # Removes dead objects
            for i in projectiles:
                if i.alive == False:
                    projectiles.remove(i)
            for m in small_meteors:
                if m.alive == False:              
                    small_meteors.remove(m)
            for m in medium_meteors:
                if m.alive == False:
                    medium_meteors.remove(m)
            for l in large_meteors:
                if l.alive == False:
                    large_meteors.remove(l)
            for p in powerups:
                if p.alive == False:
                    powerups.remove(p)



            # Checks if the player has killed enough enemys to reach the next level and spawns meteor
            if enemies_killed > level / 2 + 8:
                enemies_killed = 0
                enemy_cooldown = 120 - level
                level += 1       
            if enemy_cooldown > 1:
                enemy_cooldown -= 1
            else:
                enemy_cooldown = 120 - level * 1.5
                enemy_type = random.randrange(1, 10)
                if enemy_type < 6:
                    small_meteors.append(small_meteor_spawn(plrX, plrY, 2 * ((level / 30) + 1), True, 0, 0))
                elif enemy_type < 9:
                    medium_meteors.append(medium_meteor_spawn(plrX, plrY, 1.5 * ((level / 30) + 1), True, 0, 0))
                else:
                    large_meteors.append(large_meteor_spawn(plrX, plrY, 1 * ((level / 30) + 1)))
                    
            # Checks if the player has completed level 30
            if won == False:
                if level > 30:
                    paused = True
                                         
            # Adds drift             
            if plrY > 0:                
                if cooldownW > 0:
                    plrY = plrY - (cooldownW/25)
                    cooldownW -= 1
            if plrY < sizeY:
                if cooldownS > 0:
                    plrY = plrY + (cooldownS/25)
                    cooldownS -= 1
            if plrX > 0:
                if cooldownA > 0:
                    plrX = plrX - (cooldownA/25)
                    cooldownA -= 1
            if plrX < sizeX:
                if cooldownD > 0:
                    plrX = plrX + (cooldownD/25)
                    cooldownD -= 1
                  
            # Screen text
            remaining_enemies = int(level / 2 + 8 - enemies_killed + 1)
            level_text = font.render(("Level - %s" % level), False, WHITE)
            score_text = font.render(("Score - %s" % coins), False, WHITE)
            counter_text = font2.render(("Enemies until next level - %s" % remaining_enemies), False, TRANSPARENT_GREY)
            screen.blit(level_text, (10, 10))
            screen.blit(score_text, (10, 40))
            screen.blit(counter_text, (305, 5))
            
            # Refreshes screen and adds ticking delay
            redraw_game_window()
            clock.tick(fps)

        # Runs if the game is paused
        else:
            screen.blit(bg, (0,0))
            # Draws previous objects to screen
            for i in projectiles:
                i.draw()
            for i in small_meteors:
                i.draw()
            for i in medium_meteors:
                i.draw()
            for i in large_meteors:
                i.draw()
            for i in powerups:
                i.draw()
            for i in lives_icons:
                i.draw()

            screen.blit(level_text, (10, 10))
            screen.blit(score_text, (10, 40))
            # Draws win screen and cancel button
            screen.blit(win, (200, 200))
            cancel.draw()
            
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if cancel.is_over((mx, my)) == True:
                        paused = False
                        won = True
                        print(in_game)
                        in_game = True
                        print(in_game)

            #Updates game window
            redraw_game_window()
            clock.tick(fps)
    # Runs if the player is not in game
    elif in_game == False:
        if paused == False:
            #Draws the menu
            screen.blit(bg,(0,0))
            screen.blit(logo,(200,200))   
            play.draw()  
            mx, my = pygame.mouse.get_pos()
            m_pos = (mx, my)

            # Menu event loop
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play.is_over(m_pos) == True:
                        level = 1
                        lives = 0
                        enemies_killed = 0
                        coins = 0
                        enemy_cooldown = 120 / level
                        initial_life = 0
                        powerup_time_1 = 0
                        powerup_time_2 = 0
                        powerup_time_3 = 0
                        plrX = sizeX / 2
                        plrY = sizeY / 2
                        projectiles.clear()
                        small_meteors.clear()
                        medium_meteors.clear()
                        large_meteors.clear()
                        powerups.clear()
                        lives_icons.clear()
                        in_game = True
                        
            # Checks if the mouse is over the play button
            if play.is_over(m_pos) == True:
                play.image = play_bp
            else:
                play.image = play_b

            # Updates display
            redraw_game_window()
            clock.tick(fps)
pygame.quit()
