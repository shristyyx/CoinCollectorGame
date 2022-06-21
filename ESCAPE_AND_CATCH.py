import pygame
import random

#initialize the game
pygame.init()

#creating display surface
GAME_FOLDER = 'C:/Users/shris/PycharmProjects/pythonProject/escape_and_catch/'
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#setting the caption and background
pygame.display.set_caption("Escape & Catch")
background_image = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'background.jpg'), (WINDOW_WIDTH,WINDOW_HEIGHT))

#game actors
uncle = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'actor1.webp'),(60,80))
uncle_rect = uncle.get_rect()
uncle_rect.centerx = WINDOW_WIDTH//2
uncle_rect.centery = WINDOW_HEIGHT//2
uncle_velocity = 5

coin = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'coin.png'), (32, 32))
coin_rect = coin.get_rect()
coin_rect.left = WINDOW_WIDTH - 100
coin_rect.top = WINDOW_HEIGHT//2


#Game Sounds
loss = pygame.mixer.Sound(GAME_FOLDER + 'loss.wav')
loss.set_volume(0.5)
pick = pygame.mixer.Sound(GAME_FOLDER + 'pickup.wav')
pick.set_volume(0.5)
background_music = pygame.mixer.music.load(GAME_FOLDER+ 'background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#Game HUD
big_game_font = pygame.font.Font(GAME_FOLDER + 'font1.ttf', 60)
small_game_font = pygame.font.Font(GAME_FOLDER + 'font1.ttf', 30)
other_game_font = pygame.font.Font(GAME_FOLDER + 'font2.ttf', 40)
black_color = pygame.Color(0,0,0)
white_color = pygame.Color(255, 255, 255)

#rendering texts
game_title = big_game_font.render('Escape & Catch', True, black_color)
game_title_rect = game_title.get_rect()
game_title_rect.centerx = WINDOW_WIDTH//2
game_title_rect.top = 10

player_score = 0
player_lives = 3
score = small_game_font.render('Score: '+ str(player_score), True, white_color)
score_rect = score.get_rect()
score_rect.left = 50
score_rect.top = 10

game_over_text = big_game_font.render('GAME OVER!', True, white_color)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

game_restart_text = other_game_font.render('r: restart ', True, white_color)
game_restart_text_rect = game_restart_text.get_rect()
game_restart_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)

game_quit_text = other_game_font.render('q: quit ', True, white_color)
game_quit_text_rect = game_quit_text.get_rect()
game_quit_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 +100)

pickup_text1 = other_game_font.render('Hurrrayyyy you got this one !!', True, white_color)
pickup_text2 = small_game_font.render('Shristyyx', True, white_color)


pickup_text1_rect = pickup_text1.get_rect()
pickup_text1_rect.center = (WINDOW_WIDTH//2, 100)
pickup_text2_rect = pickup_text2.get_rect()
pickup_text2_rect.right = WINDOW_WIDTH - 10
pickup_text2_rect.top = 10
pickup_text1_rect.center = (WINDOW_WIDTH//2, 100 )

#main game loop
game_status = 1
FPS = 60
clock = pygame.time.Clock()
running = True


while running:
    #listen to the events (user actions)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_q:
                running = False
            elif ev.key == pygame.K_r:
                player_score = 0
                pygame.mixer.music.play(-1)
                coin_rect.left = 0
                coin_rect.top = 400
                uncle_rect.centery = WINDOW_HEIGHT // 2
                score = small_game_font.render('Score: ' + str(player_score), True, white_color)
                game_status = 1

    #apply the background
    display_surface.blit(background_image, (0,0))

    if game_status == 1:
        #know the keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] :
            uncle_rect.top -= uncle_velocity
        elif keys[pygame.K_DOWN]  :
            uncle_rect.top += uncle_velocity
        elif keys[pygame.K_RIGHT]  :
            uncle_rect.right += uncle_velocity
        elif keys[pygame.K_LEFT] :
            uncle_rect.left -= uncle_velocity

        #check whether uncle stole coin
        if coin_rect.colliderect(uncle_rect):
            pick.play()
            uncle_velocity+=1
            coin_rect.left = random.randint(100, WINDOW_WIDTH - coin_rect.width)
            coin_rect.top = random.randint(100, WINDOW_HEIGHT - coin_rect.height)
            player_score+=1
            score = small_game_font.render('Score: ' + str(player_score), True, white_color)


        elif uncle_rect.left < 0 or uncle_rect.right > WINDOW_WIDTH or uncle_rect.top <0 or uncle_rect.bottom > WINDOW_HEIGHT:
            loss.play()
            game_status = 2

        #draw the actors
        display_surface.blit(uncle, uncle_rect)
        display_surface.blit(coin, coin_rect)


    elif game_status == 2:
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(game_restart_text, game_restart_text_rect)
        display_surface.blit(game_quit_text, game_quit_text_rect)

    #draw the HUD
    display_surface.blit(game_title, game_title_rect)
    display_surface.blit(score, score_rect)
    display_surface.blit(pickup_text1, pickup_text1_rect)
    display_surface.blit(pickup_text2, pickup_text2_rect)

    #refesh the window
    pygame.display.update()

    #moderate the rate of iteration
    #By this the game runs at the same speed over different CPU's
    #Also cooperative multi tasking is achieved
    clock.tick(FPS)











#quit the game
pygame.quit()