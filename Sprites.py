import pygame, time, random, math
from required import Animation, SpriteGroup
pygame.init()
pygame.mixer.init()
pygame.font.init()
font = pygame.font.Font("airstrike.ttf", 32)
coin_list = SpriteGroup()
kunai_list = SpriteGroup()
player_list = SpriteGroup()
robot_list = SpriteGroup()
fireball_list = SpriteGroup()
tile_list = SpriteGroup()
life_list = [pygame.transform.scale(pygame.image.load("life/0.png"),(80,80)),
             pygame.transform.scale(pygame.image.load("life/1.png"),(80,80)),
             pygame.transform.scale(pygame.image.load("life/2.png"),(80,80)),
             pygame.transform.scale(pygame.image.load("life/3.png"),(80,80)),
             pygame.transform.scale(pygame.image.load("life/4.png"),(80,80)),
             pygame.transform.scale(pygame.image.load("life/5.png"),(80,80)),
             pygame.transform.scale(pygame.image.load("life/6.png"),(80,80)),
             pygame.transform.scale(pygame.image.load("life/7.png"),(80,80)),
             pygame.transform.scale(pygame.image.load("life/8.png"),(80,80))]

class Tile(pygame.sprite.Sprite):
    def __init__(self, grnd, type=None):
        pygame.sprite.Sprite.__init__(self)
        self.ground = grnd
        self.type = type
        if self.type != "acid":
            self.image = pygame.transform.scale(pygame.image.load("Tiles/BGTile (2).png"), (100, 50))
        elif self.type == "acid":
            self.image = pygame.transform.scale(pygame.image.load("Tiles/Acid (1).png"), (100, 50))
        self.scale = .5
        self.rx = 0
        self.x = 700
        self.rect = self.image.get_rect()
        self.y = 500 - self.rect.height

    def update(self, dt):
        self.x -= 10
        if self.x + self.rect.width < 0 and self.type != 'acid':
            if random.randint(0, 10) < self.ground.acid_tile_occourance:
                if not self.contains_acid():
                    acid = Tile(500, type='acid')

                    self.ground.add(acid)
                    pass
            self.x = len(self.ground.ground_tiles) * self.rect.width + self.x
        if self.x + self.rect.width < 0 and self.type == 'acid':
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, (self.x + (self.rect.width * self.rx), self.y))

    def contains_acid(self):
        for t in self.ground.ground_tiles:
            if t.type == 'acid':
                return True
        return False


class Ground(pygame.sprite.Sprite):
    def __init__(self, acid=6):
        pygame.sprite.Sprite.__init__(self)
        self.ground_tiles = SpriteGroup()
        x = 0
        cx = 0
        self.acid_tile_occourance = acid
        while True:
            t = Tile(self, 500)
            t.x, t.y = t.rect.width * x, 500 - t.rect.height
            cx = t.x
            if cx > 800 + t.rect.width:
                break
            else:
                self.ground_tiles.add(t)
            x += 1

    def add(self, tile):
        tile.x, tile.y = tile.rect.width * (len(self.ground_tiles.sprites()) - 1.1), 500 - tile.rect.height
        self.ground_tiles.add(tile)

    def update(self, dt):
        self.ground_tiles.update(dt)

    def draw(self, screen):
        self.ground_tiles.draw(screen)

g = Ground()
t = Tile(400)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Create states for the Player - run, idle, throw, jump, fall etc
        self.image = {
            "idle": Animation([
                "png/Idle__000.png",
                "png/Idle__001.png",
                "png/Idle__002.png",
                "png/Idle__003.png",
                "png/Idle__004.png",
                "png/Idle__005.png",
                "png/Idle__006.png",
                "png/Idle__007.png",
                "png/Idle__008.png",
                "png/Idle__009.png",
            ],100,True),

            "run": Animation([
                "png/Run__000.png",
                "png/Run__001.png",
                "png/Run__002.png",
                "png/Run__003.png",
                "png/Run__004.png",
                "png/Run__005.png",
                "png/Run__006.png",
                "png/Run__007.png",
                "png/Run__008.png",
                "png/Run__009.png",
            ],100,True),

            "throw": Animation([
                "png/Throw__000.png",
                "png/Throw__001.png",
                "png/Throw__002.png",
                "png/Throw__003.png",
                "png/Throw__004.png",
                "png/Throw__005.png",
                "png/Throw__006.png",
                "png/Throw__007.png",
                "png/Throw__008.png",
                "png/Throw__009.png",
            ],100,True),

            "jump": Animation([
                "png/Jump__000.png",
                "png/Jump__001.png",
                "png/Jump__002.png",
                "png/Jump__003.png",
                "png/Jump__004.png",
                "png/Jump__005.png",
            ],100,True),

            "fall": Animation([
                "png/Jump__006.png",
                "png/Jump__007.png",
                "png/Jump__008.png",
                "png/Jump__009.png",
            ],100,True),
            "die": Animation([
                "png/Dead__000.png",
                "png/Dead__001.png",
                "png/Dead__002.png",
                "png/Dead__003.png",
                "png/Dead__004.png",
                "png/Dead__005.png",
                "png/Dead__006.png",
                "png/Dead__007.png",
                "png/Dead__008.png",
                "png/Dead__009.png",
            ],100,True),
            "attack": Animation([
                "png/Attack__000.png",
                "png/Attack__001.png",
                "png/Attack__002.png",
                "png/Attack__003.png",
                "png/Attack__004.png",
                "png/Attack__005.png",
                "png/Attack__006.png",
                "png/Attack__007.png",
                "png/Attack__008.png",
                "png/Attack__009.png",
            ],100,True)
        }
        self.state = self.image["die"]
        self.state.get_mask()
        self.jumpSpeed = 100.0
        self.scale = .39
        self.isJumping = False
        self.isFalling = True
        self.rect = self.state.getScaledImage(self.scale).get_rect()
        self.x = 50
        self.y = 450 - self.rect.height
        self.flip = False
        self.jumpAcceleration = 800
        self.jumpVelocity = 0
        self.last_shot = 100
        self.dead = False
        self.dead_count = 0
        self.radius = self.rect.width/2
        self.life = 8
        self.isAttacking = False
        self.speed = 3
        self.score = 0

    def update(self,dt):
        # return self.mask
        self.state.update(30)

        if self.isJumping or self.isFalling:
            self.y += self.jumpVelocity * (30 / 1000.0)
            self.jumpVelocity += self.jumpAcceleration * (30 / 1000.0)
            if self.jumpVelocity >= 0:
                self.state = self.image["fall"]
            elif self.jumpVelocity < 0 :
                self.state = self.image["jump"]

        if self.y < 450 - 171:
            self.isFalling = True
            self.isJumping = False

        if self.y > 450 - 171:
            self.y = 450 - 171
            self.isFalling = False
            self.isJumping = False

        key = pygame.key.get_pressed()

        if key[pygame.K_d] and not key[pygame.K_w]:
            self.state = self.image["run"]
            self.flip = False
            self.x += self.speed

        if key[pygame.K_d] and key[pygame.K_w] and self.y == 450 - 171:
            self.flip = False
            self.isJumping = True
            self.jumpVelocity = -450
            self.x += self.speed

        if key[pygame.K_a]:
            self.state = self.image["run"]
            self.flip = True
            self.x -= self.speed

        if key[pygame.K_w] and self.y == 450 - 171:
            self.state = self.image["jump"]
            self.isJumping = True
            self.jumpVelocity = -450

        if not (key[pygame.K_a] or key[pygame.K_d]) and not(self.isFalling or self.isJumping):
            self.state = self.image["idle"]

        if key[pygame.K_j] and not (key[pygame.K_d] or key[pygame.K_a] or key[pygame.K_h]):
            self.state = self.image["throw"]
            if time.time() - self.last_shot > 0.5:
                kunai_list.add(Kunai(self.x+100,self.y+100))
                self.last_shot = time.time()

        if key[pygame.K_j] and key[pygame.K_d] and not (key[pygame.K_a] or key[pygame.K_h]):
            self.state = self.image["throw"]
            if time.time() - self.last_shot > 0.5:
                kunai_list.add(Kunai(self.x+100,self.y+100))
                self.last_shot = time.time()

        if key[pygame.K_j] and key[pygame.K_a] and not (key[pygame.K_d] or key[pygame.K_h]):
            self.state = self.image["throw"]
            if time.time() - self.last_shot > 0.5:
                kunai_list.add(Kunai(self.x+100,self.y+100))
                self.last_shot = time.time()

        if key[pygame.K_h] and not (key[pygame.K_d] or key[pygame.K_a] or key[pygame.K_j]):
            self.state = self.image["attack"]

        if key[pygame.K_h] and key[pygame.K_d] and not (key[pygame.K_a] or key[pygame.K_j]):
            self.state = self.image["attack"]

        if key[pygame.K_h] and key[pygame.K_a] and not (key[pygame.K_d] or key[pygame.K_j]):
            self.state = self.image["attack"]

        # for fireball in fireball_list:
        #     fire_offset = (int(self.x-fireball.x), int(self.y-fireball.y))
        #
        #     if (fire_offset[0] > -80) and (fire_offset[1] >= -110):
        #         if fire_offset[0] > -80 and fireball.x + fireball.rect.width < self.x:
        #             pass
        #         else:
        #             if self.state != self.image["attack"]:
        #                fireball.kill()
        #                self.life -= 0
        #                if self.life <= 0:
        #                    self.dead = True
        #             else:
        #                fireball.kill()
        for fireball in fireball_list:
            if pygame.sprite.collide_mask(self, fireball.mask):
                print("Collide")

        for robot in robot_list:
            rob_offset = (int(self.x - robot.x), int(self.y - robot.y))

            if rob_offset[0] >= -77 and rob_offset[1] >= -183:
                self.life -= 0

                if self.state == self.image["attack"]:
                    robot.life -= 1
                if rob_offset[0] > -77 and robot.x + robot.rect.width > self.x:
                    pass

        for coin in coin_list:
            coin_offset = (round(self.x - coin.x), round(self.y - coin.y))

            if coin_offset[0] >= -52 and coin_offset[1] >= -248:
                if coin.state == coin.image["life"]:
                    if self.life < 8:
                        self.life += 1
                        coin.state = random.choice(coin.types)
                        coin.x = random.randint(3000,5000)
                    else:
                        pass
                if coin.state == coin.image["bronze"]:
                    self.score += 1
                    coin.x = random.randint(3000, 5000)
                    coin.state = random.choice(coin.types)
                if coin.state == coin.image["silver"]:
                    self.score += 5
                    coin.x = random.randint(3000, 5000)
                    coin.state = random.choice(coin.types)
                if coin.state == coin.image["gold"]:
                    self.score += 10
                    coin.x = random.randint(3000, 5000)
                    coin.state = random.choice(coin.types)

        for t in g.ground_tiles:
            if t.contains_acid():
                print("Ok")


        if self.dead:
            self.state.update(6.67)
            self.state = self.image["die"]
            self.dead_count += 1
            if self.dead_count >= 30:
                self.kill()
                self.dead_count = 0


    def draw(self,screen):
        text = font.render("Score:%s"%(self.score), True, (0, 0, 0))
        if self.flip:
                img = pygame.transform.flip(self.state.getScaledImage(self.scale), True, False)
        else:
            img = self.state.getScaledImage(self.scale)

        screen.blit(img,(self.x,self.y))
        screen.blit(text,(600,20))

        life = int(self.life)

        if life >= 0:
            screen.blit(life_list[life],(50,30))

class Kunai(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("png/Kunai.png"),(90,20))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        del self.mask

    def update(self):
        self.x += self.speed
        if self.x > 800 + self.rect.width:
            self.kill()

        self.rect = self.image.get_rect()

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

class Robot(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image = {
            "idle":Animation([
                "robot/idle/idle_1.png",
                "robot/idle/idle_2.png",
                "robot/idle/idle_3.png",
                "robot/idle/idle_4.png",
                "robot/idle/idle_5.png",
            ],100,True),
            "die":Animation([
                "robot/die/die_1.png",
                "robot/die/die_2.png",
                "robot/die/die_3.png",
                "robot/die/die_4.png",
                "robot/die/die_5.png",
                "robot/die/die_6.png",
                "robot/die/die_7.png",
                "robot/die/die_8.png",
                "robot/die/die_9.png",
            ],100,True)
        }
        self.state = self.image["idle"]
        self.scale = .4
        self.rect = self.state.getScaledImage(self.scale).get_rect()
        self.x = x
        # self.y = 450 - self.rect.height
        self.y = 250
        self.speed = 3
        self.last_shot = 100
        self.isdead = False
        self.dead_count = 0
        self.shooting = False
        self.life = 5
        self.shoot_timer = 0
        self.mask = pygame.mask.from_surface(self.state.getCurrentFrame(self.scale))

    def update(self,dt):
        if self.x > 600:
            self.x -= self.speed

        if self.x <= 600:
            self.x -= 0.5
            self.shooting = True


        for kunai in kunai_list:
            if kunai.x + kunai.rect.width > self.x + 30 :
                if kunai.y > self.y and kunai.y:
                    kunai.kill()
                    self.life -= 1

        self.rect = self.state.get_rect()


        if self.shooting:
            if time.time() - self.last_shot > 1:
                fireball_list.add(Fireball(self.x,self.y+50))
                self.last_shot = time.time()

        if self.isdead:
            self.state.update(dt-10)
            self.state = self.image["die"]
            self.dead_count += 1
            if self.dead_count >= 20:
                self.kill()
                robot_list.add(Robot(random.randint(3000,4000)))
                self.scale += 0.1
                self.life += 2

        if self.life <= 0:
            self.isdead = True

        self.state.update(dt)

    def draw(self,screen):
        img = self.state.getScaledImage(self.scale)
        screen.blit(img,(self.x,self.y))

class Fireball(pygame.sprite.Sprite,Animation):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Animation([
            "fireball/fire6.png",
            "fireball/fire7.png",
        ],100,True)
        self.scale = .4
        self.rect = self.image.get_rect()
        self.y = y
        self.x = x
        self.speed = 8
        self.burning = True
        self.count = 0
        self.radius = self.rect.width/2
        self.mask = pygame.mask.from_surface(self.image.getCurrentFrame(self.scale))

    def update(self,dt):
        self.image.update(dt)
        self.rect = self.image.getCurrentFrame(self.scale).get_rect()
        self.mask = pygame.mask.from_surface(self.image.getCurrentFrame(self.scale))

        self.x -= self.speed
        if self.x < 0 - self.rect.width:
            self.kill()

    def draw(self,screen):
        img = self.image.getScaledImage(self.scale)
        screen.blit(img,(self.x,self.y))

class Coin(pygame.sprite.Sprite,Animation):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = {
            "life": Animation([
                "life/Bronze_11.png",
                "life/Bronze_12.png",
                "life/Bronze_13.png",
                "life/Bronze_14.png",
                "life/Bronze_15.png",
                "life/Bronze_16.png",
                "life/Bronze_17.png",
                "life/Bronze_18.png",
                "life/Bronze_19.png",
                "life/Bronze_20.png",
            ],100,True),
            "bronze": Animation([
                "score1/Bronze_1.png",
                "score1/Bronze_2.png",
                "score1/Bronze_3.png",
                "score1/Bronze_4.png",
                "score1/Bronze_5.png",
                "score1/Bronze_6.png",
                "score1/Bronze_7.png",
                "score1/Bronze_8.png",
                "score1/Bronze_9.png",
                "score1/Bronze_10.png",
            ],150,True),
            "silver": Animation([
                "score2/Silver_0.png",
                "score2/Silver_1.png",
                "score2/Silver_2.png",
                "score2/Silver_3.png",
                "score2/Silver_4.png",
                "score2/Silver_5.png",
                "score2/Silver_6.png",
                "score2/Silver_7.png",
                "score2/Silver_8.png",
                "score2/Silver_9.png",
            ],150,True),
            "gold": Animation([
                "score3/Gold_1.png",
                "score3/Gold_2.png",
                "score3/Gold_3.png",
                "score3/Gold_4.png",
                "score3/Gold_5.png",
                "score3/Gold_6.png",
                "score3/Gold_7.png",
                "score3/Gold_8.png",
                "score3/Gold_9.png",
                "score3/Gold_10.png",
            ],150,True)
        }
        self.types = [self.image["life"], self.image["gold"], self.image['silver'], self.image["bronze"]]
        self.state = random.choice(self.types)
        self.scale = .1
        self.rect = self.state.getScaledImage(self.scale).get_rect()
        self.y = 450 - self.rect.height
        self.x = random.randint(3000,5000)
        self.speed = 8
        self.count = 0

    def update(self, dt):
        self.x -= 10
        if self.x < 0 - self.rect.width:
            self.state = random.choice(self.types)
            self.x = random.randint(3000,5000)

    def draw(self, screen):
        self.state.update(30)
        img = self.state.getScaledImage(self.scale)
        screen.blit(img, (self.x, self.y))
