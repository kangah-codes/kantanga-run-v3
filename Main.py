import pygame
from required import Animation, SpriteGroup
from Sprites import Player,Tile,Ground,Robot,Coin
from Sprites import player_list,kunai_list,robot_list,fireball_list,coin_list
pygame.init()

# Defining global variables
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption("Katanga Run")
pygame.display.set_icon(pygame.transform.rotate(pygame.image.load("png/Kunai.png"),90))
white = (255,255,255)

clock = pygame.time.Clock()
fps = 60

player = Player()
ground = Ground()
coin = Coin()

#Adding Sprites
player_list.add(player)
robot_list.add(Robot(1000))
coin_list.add(coin)

running = True

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    # player_list.draw(screen)
    kunai_list.draw(screen)
    robot_list.draw(screen)
    player_list.draw(screen)
    fireball_list.draw(screen)
    coin_list.draw(screen)
    ground.draw(screen)

    if player.x >= 80:
        player.x = 80
        if player.isFalling or player.isJumping:
            player.x = 80
            ground.update(30)
            coin_list.update(30)

    player_list.update(fps)
    fireball_list.update(30)
    kunai_list.update()
    #robot_list.update(30)

    pygame.display.update()
