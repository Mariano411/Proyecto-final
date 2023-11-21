############################################################################################
###                                                                                      ###
###   PyGame with a Pea shoot bullet for defensing the zombie army coming            ###
###                                                                                      ###
###   Author: Junjie Shi                                                                 ###
###   Email : handsomestone@gmail.com                                                    ### 
###                                                                                      ### 
###   Do Enjoy the game!                                                                 ###
###   You need to have Python and PyGame installed to run it.                            ###
###   Run it by typing "python zombie.py" in the terminal                                ###
###                                                                                      ### 
###   This program is free software: you can redistribute it and/or modify               ### 
###   it under the terms of the GNU General Public License as published by               ### 
###   the Free Software Foundation, either version 3 of the License, or                  ### 
###   (at your option) any later version.                                                ### 
###                                                                                      ### 
###   This program is distributed in the hope that it will be useful,                    ### 
###   but WITHOUT ANY WARRANTY; without even the implied warranty of                     ### 
###   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                      ### 
###   GNU General Public License for more details.                                       ### 
###                                                                                      ### 
###   You should have received a copy of the GNU General Public License                  ### 
###   along with this program.  If not, see <http://www.gnu.org/licenses/>.              ###                                                                              ###
###                                                                                      ###
############################################################################################

import pygame, random, sys, time
from pygame.locals import *

#set up some variables
WINDOWWIDTH = 1366
WINDOWHEIGHT = 758
FPS = 60

MAXGOTTENPASS = 10
ZOMBIESIZE = 70 #includes newKindZombies
ADDNEWZOMBIERATE = 30
ADDNEWKINDZOMBIE = ADDNEWZOMBIERATE

NORMALZOMBIESPEED = 2
NEWKINDZOMBIESPEED = NORMALZOMBIESPEED / 2

PLAYERMOVERATE = 15
BULLETSPEED = 10
ADDNEWBULLETRATE = 15

TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                if event.key == pygame.K_1:
                    return 1  # Usuario selecciona escenario 1
                elif event.key == pygame.K_2:
                    return 2  # Usuario selecciona escenario 2
                elif event.key == pygame.K_3:
                    return 3  # Usuario selecciona escenario 3
                
def playerHasHitZombie(playerRect, zombies):
    for z in zombies:
        if playerRect.colliderect(z['rect']):
            return True
    return False

def bulletHasHitZombie(bullets, zombies):
    for b in bullets:
        if b['rect'].colliderect(z['rect']):
            bullets.remove(b)
            return True
    return False

def bulletHasHitCrawler(bullets, newKindZombies):
    for b in bullets:
        if b['rect'].colliderect(c['rect']):
            bullets.remove(b)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#, pygame.FULLSCREEN)
pygame.display.set_caption('Zombie Defence')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('grasswalk.mp3')

# set up images
playerImage = pygame.image.load('Pea.png')
playerRect = playerImage.get_rect()


bulletImage = pygame.image.load('PB.png')
bulletRect = bulletImage.get_rect()

zombieImage = pygame.image.load('Z.png')
newKindZombieImage = pygame.image.load('Balde.png')
newKindZombieImage = pygame.image.load('ZD.png')

backgroundImage = pygame.image.load('menu.jpeg')
rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
windowSurface.blit(rescaledBackground, (0, 0))
windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))

while True:
    # set up the start of the game

    zombies = []
    newKindZombies = []
    bullets = []

    zombiesGottenPast = 0
    puntos = 0

    playerRect.topleft = (325, WINDOWHEIGHT /2) #lugar de aparición de la planta
    moveLeft = moveRight = False
    moveUp=moveDown = False
    shoot = False

    zombieAddCounter = 0
    newKindZombieAddCounter = 0
    bulletAddCounter = 40
    pygame.mixer.music.play(-1, 0.0)

    
    drawText('Bienvenidos a PVZ', font, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 4))
    drawText('Seleccione un escenario', font, windowSurface, (WINDOWWIDTH / 3) - 10, (WINDOWHEIGHT / 3) + 50)
    drawText('Escenario 1 / 2 / 3', font, windowSurface, (WINDOWWIDTH / 2) - 10, (WINDOWHEIGHT / 2) + 50)
    pygame.display.update()

    selected_scenario = waitForPlayerToPressKey()

    if selected_scenario == 1:
        backgroundImage = pygame.image.load('J.jpg')
        rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
    elif selected_scenario == 2:
        backgroundImage = pygame.image.load('F.jpg')
        rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
    elif selected_scenario == 3:
        backgroundImage = pygame.image.load('R.jpeg')
        rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
    
    
    while True: # the game loop runs while the game part is playing
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                if event.key == K_SPACE:
                    shoot = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                
                if event.key == K_SPACE:
                    shoot = False
                    
        #Score
        if puntos == 10:
            BULLETSPEED+=0.2
            playerImage = pygame.image.load('FirePea.png')
            playerRect = playerImage.get_rect()
            bulletImage = pygame.image.load('FB.png')
            bulletRect = bulletImage.get_rect()
            playerRect.topleft = (325, WINDOWHEIGHT /2)
        if puntos == 20:
            BULLETSPEED+=0.2
            playerImage = pygame.image.load('SnowPea.png')
            playerRect = playerImage.get_rect()
            bulletImage = pygame.image.load('SB.png')
            bulletRect = bulletImage.get_rect()
            playerRect.topleft = (325, WINDOWHEIGHT /2)
        if puntos == 30:
            BULLETSPEED+=0.2
            playerImage = pygame.image.load('MZCanon.png')
            playerRect = playerImage.get_rect()
            bulletImage = pygame.image.load('CB.png')
            bulletRect = bulletImage.get_rect()
            playerRect.topleft = (325, WINDOWHEIGHT /2)
        if puntos == 40:
            BULLETSPEED+=0.2
            playerImage = pygame.image.load('Plgoch.png')
            playerRect = playerImage.get_rect()
            bulletImage = pygame.image.load('5.png')
            bulletRect = bulletImage.get_rect()
            playerRect.topleft = (325, WINDOWHEIGHT /2)
            
        # Add new zombies at the top of the screen, if needed.
        zombieAddCounter += 1
        if zombieAddCounter == ADDNEWKINDZOMBIE:
            zombieAddCounter = 0
            zombieSize = ZOMBIESIZE       
            newZombie = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-zombieSize-10), zombieSize, zombieSize),
                        'surface':pygame.transform.scale(zombieImage, (zombieSize, zombieSize)),
                        }

            zombies.append(newZombie)

        # Add new newKindZombies at the top of the screen, if needed.
        newKindZombieAddCounter += 1
        if newKindZombieAddCounter == ADDNEWZOMBIERATE:
            newKindZombieAddCounter = 0
            newKindZombiesize = ZOMBIESIZE
            newCrawler = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-newKindZombiesize-10), newKindZombiesize, newKindZombiesize),
                        'surface':pygame.transform.scale(newKindZombieImage, (newKindZombiesize, newKindZombiesize)),
                        }
            newKindZombies.append(newCrawler)

        # add new bullet
        bulletAddCounter += 1
        if bulletAddCounter >= ADDNEWBULLETRATE and shoot == True:
            bulletAddCounter = 0
            newBullet = {'rect':pygame.Rect(playerRect.centerx+10, playerRect.centery-25, bulletRect.width, bulletRect.height),
						 'surface':pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
						}
            bullets.append(newBullet)

        # Move the player around.
        if moveUp and playerRect.top > 30:
            playerRect.move_ip(0,-1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT-10:
            playerRect.move_ip(0,PLAYERMOVERATE)

        # Move the zombies down.
        for z in zombies:
            z['rect'].move_ip(-1*NORMALZOMBIESPEED, 0)

        # Move the newKindZombies down.
        for c in newKindZombies:
            c['rect'].move_ip(-1*NEWKINDZOMBIESPEED,0)

        # move the bullet
        for b in bullets:
            b['rect'].move_ip(1 * BULLETSPEED, 0)

        # Delete zombies that have fallen past the bottom.
        for z in zombies[:]:
            if z['rect'].left < 0:
                zombies.remove(z)
                zombiesGottenPast += 1

        # Delete newKindZombies that have fallen past the bottom.
        for c in newKindZombies[:]:
            if c['rect'].left <0:
                newKindZombies.remove(c)
                zombiesGottenPast += 1
		
        for b in bullets[:]:
            if b['rect'].right>WINDOWWIDTH:
                bullets.remove(b)
				
        # check if the bullet has hit the zombie
        for z in zombies:
            if bulletHasHitZombie(bullets, zombies):
                puntos += 1
                zombies.remove(z)
    
        for c in newKindZombies:
            if bulletHasHitCrawler(bullets, newKindZombies):
                puntos += 1
                newKindZombies.remove(c)      

        # Draw the game world on the window.
        windowSurface.blit(rescaledBackground, (0, 0))

        # Draw the player's rectangle, rails
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for z in zombies:
            windowSurface.blit(z['surface'], z['rect'])

        for c in newKindZombies:
            windowSurface.blit(c['surface'], c['rect'])

        # draw each bullet
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])

        # Draw the score and how many zombies got past
        drawText('zombis que pasaron: %s' % (zombiesGottenPast), font, windowSurface, 10, 20)
        drawText('puntos: %s' % (puntos), font, windowSurface, 10, 50)

    
        # update the display
        pygame.display.update()
            
        # Check if any of the zombies has hit the player.
        if playerHasHitZombie(playerRect, zombies):
            break
        if playerHasHitZombie(playerRect, newKindZombies):
           break
        
        # check if score is over MAXGOTTENPASS which means game over
        if zombiesGottenPast >= MAXGOTTENPASS:
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()
    time.sleep(1)
    if zombiesGottenPast >= MAXGOTTENPASS:
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        drawText('puntos: %s' % (puntos), font, windowSurface, 10, 30)
        drawText('Bienvenidos a PVZ', font, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 4))
        drawText('Seleccione un escenario', font, windowSurface, (WINDOWWIDTH / 3) - 10, (WINDOWHEIGHT / 3) + 50)
        drawText('Escenario 1 / 2 / 3', font, windowSurface, (WINDOWWIDTH / 2) - 10, (WINDOWHEIGHT / 2) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()
    if playerHasHitZombie(playerRect, zombies):
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        drawText('puntos: %s' % (puntos), font, windowSurface, 10, 30)
        drawText('Bienvenidos a PVZ', font, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 4))
        drawText('Seleccione un escenario', font, windowSurface, (WINDOWWIDTH / 3) - 10, (WINDOWHEIGHT / 3) + 50)
        drawText('Escenario 1 / 2 / 3', font, windowSurface, (WINDOWWIDTH / 2) - 10, (WINDOWHEIGHT / 2) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()
    gameOverSound.stop()


        
