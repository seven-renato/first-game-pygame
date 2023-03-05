import pygame # 2 D Graphics para criar jogos
import os
pygame.font.init() # Definir a fonte que será usada
pygame.mixer.init() # Abre biblioteca de som

#Surface - Basicamente a janela
WIDTH,HEIGHT = 900,500

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Valores Constantes devem ser escritos em MAIUSCULO
pygame.display.set_caption("First Game in PYGAME!") # Titulo da aba

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT) # Posicão no meio, la em cima, grossura e altura

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1 # Numero do evento, para eventos separados e novos necessario
RED_HIT = pygame.USEREVENT + 2  # Se fossem os dois + 1, estariam no mesmo valor e seriam o mesmo evento

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) # Resize
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")),(WIDTH,HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE,(0,0)) # Cor para toda a tela, em RGB, precisa dar UPDATE (Fill)
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)#Coloca a font, o texto, sempre 1, e a cor
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))#Usar blit quando quer colocar um surface sobre a  tela (Texto ou imagens)
    WIN.blit(RED_SPACESHIP, (red.x,red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    # O topo da esquerda é o (0,0)
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # Left # Não ultrapassar a tela
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 20:  # Down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 20: # Down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red): # Mover as balas, ver a colisão e excluir quando sai da tela ou toca
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): # O Yellow colidiu em algum momento com um retangulo
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet) # Enviar um evento de dentro da função como aviso, ja que não tem como acessar isso
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1, WHITE)
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    yellow =  pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # Dado que estamos atualizando a posição do X, e sempre esta tendo um update
    red =  pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # Basicamente serve para alterar a posição, ja que vai desenha por parâmetro

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # Controla a velocidade do loop do while
        for event in pygame.event.get(): # Checar cado um dos eventos que esta acontecendo no Pygame
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: # Ao invés de ver se esta pressionado, ver se foi clickado uma vez, para não spammar
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5) # O tiro sair do meio e ponta do boneco
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5) # O tiro sair do meio e ponta do boneco
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            winner_text = ""
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()


            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() # Enquanto essa linha esta ocorrendo, o pygame vai ficar de olho no teclado, e retornar a lista de clicks
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red) # Ver se qualquer uma das balas colidem com um dos personagens

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()

if __name__ == "__main__": # Garante que esta função "main" ira rodar apenas se este arquivo for a base, não tem como executar por outro lugar
    main() # Não pode importar de qualquer lugar