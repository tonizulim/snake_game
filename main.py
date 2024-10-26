import pygame
import sys
from random import randint
import time

box_size = 33

class snake:
    def __init__(self):
        #postavljamo blok zmije
        self.snake_block=pygame.image.load("snake_image.bmp").convert()
        self.snake_block=pygame.transform.scale(self.snake_block, (33, 33))

        self.snake_block_head=pygame.image.load("snake_head.bmp").convert()
        self.snake_block_head=pygame.transform.scale(self.snake_block_head, (33, 33))
        self.direction='right'

        self.x = [165, 132, 99, 66, 33]
        self.y = [33, 33, 33, 33, 33]

    #crta zmiju
    def draw(self, screen):
        screen.blit(self.snake_block_head, (self.x[0], self.y[0]))
        for i in range(1, len(self.x)):
            screen.blit(self.snake_block, (self.x[i], self.y[i]))

    #mjenja smjer zmije ovisno o pritisnutom botunu
    def chane_direction(self, direction):
        if(self.direction == 'right' and direction != 'left'):
            self.direction = direction
        if(self.direction == 'left' and direction != 'right'):
            self.direction = direction
        if(self.direction == 'up' and direction != 'down'):
            self.direction = direction
        if(self.direction == 'down' and direction != 'up'):
            self.direction = direction

    #pomice zmiju   
    def move(self):
        for i in range(len(self.x)-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'right':
            self.x[0] += box_size
        
        if self.direction == 'left':
            self.x[0] -= box_size
        
        if self.direction == 'up':
            self.y[0] -= box_size
        
        if self.direction == 'down':
            self.y[0] += box_size

    #provjerava da li je zmija pojela jabuku
    def eat_apple(self,  apple):
        if self.x[0] == apple.x and self.y[0] == apple.y:
            return True
        else:
            return False

    #provjerava da li je zmija pojela sama sebe
    def eat_itself(self):
        for i in range(1, len(self.x), 1):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                return True
            
        return False
            
    #provjerava da li je zmija izašla iz okvira
    def out_of_frame(self):
        if self.x[0] < 0 or self.x[0] > 23*box_size or self.y[0] < 0 or self.y[0] > 17*box_size:
            return True
        else:
            return False

    #provjerava da li je zmija izašla iz okvira i jel pojela sama sebe
    def check_gameover(self):
        if self.eat_itself() or self.out_of_frame():
            return True
        else:
            return False


class apple:
    def __init__(self):
        self.apple_block=pygame.image.load("apple.png").convert()
        self.apple_block=pygame.transform.scale(self.apple_block, (33, 33))

        self.x = 12*box_size
        self.y = 9*box_size
    
    #postavlja jabuku na random mjesto
    def set_apple_random(self, snake):
        self.new_x = randint(0, 23)*box_size
        self.new_y = randint(0, 17)*box_size

        for i in range(0, len(snake.x)):
            if self.new_x == snake.x[i] and self.new_y == snake.y[i]:
                self.set_apple_random(snake)

        self.x = self.new_x
        self.y = self.new_y
    
    #crta jabuku
    def draw(self, screen):
        screen.blit(self.apple_block, (self.x, self.y))

#otvara file cita i sprema score
class fileclass:
    def __init__(self):
        pass

    def write(self, score):
        if int(score) > int(self.highscore):
            self.file = open("rezultati.txt", "w")
            self.file.write(str(score))
            self.file.close()

    def read(self):
        self.file = open("rezultati.txt", "r")
        self.highscore = self.file.read()
        print(self.highscore)
        self.file.close()
        return self.highscore

class display:
    def __init__(self):
        self.fileclass = fileclass()
        self.highscore = self.fileclass.read()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.text_currentscore = self.font.render('Score: 0', False, (255, 255, 255))
        self.text_highscore = self.font.render('Highscore: ' + self.highscore , False, (255, 255, 255))

        

    def draw(self, screen, score):
        self.text_currentscore = self.font.render('Score: ' + str(score), False, (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (24*33, 0, 400, 18*33))

        if(int(score) > int(self.highscore)):
            self.text_highscore = self.font.render('New Highscore: ' + str(score), False, (255, 255, 255))
            self.fileclass.write(score)

        screen.blit(self.text_currentscore, (box_size * 24 + 10, box_size * 9 - 15 - 15))
        screen.blit(self.text_highscore, (box_size * 24 + 10, box_size * 9 - 15 + 15))


class game_over_display:
    def __init__(self):
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.game_over_text = self.font.render('Game Over', False, (255, 255, 255))
        self.restart_game_text = self.font.render('Press enter to restart', False, (255, 255, 255))

        self.game_over_text_rect = self.game_over_text.get_rect(center=(box_size * 12 + 200, box_size * 9))
        self.restart_game_text_rect = self.restart_game_text.get_rect(center=(box_size * 12 + 200, box_size * 9 + 50))


    def draw(self, screen):#**** doradi ovo
        screen.fill((0, 0, 0))
        screen.blit(self.game_over_text, self.game_over_text_rect)
        screen.blit(self.restart_game_text, self.restart_game_text_rect)
        pygame.display.update()

class start_game_display:
    def __init__(self):
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.start_game_text = self.font.render('Pres any key to start', False, (255, 255, 255))
        self.start_game_text_rect = self.start_game_text.get_rect(center=(box_size * 12 + 200, box_size * 9))


    def draw(self, screen):#**** doradi ovo
        screen.fill((0, 0, 0))
        screen.blit(self.start_game_text, self.start_game_text_rect)
        pygame.display.update()


class game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((box_size * 24 + 400, box_size * 18))
        pygame.display.set_caption("Snake")

        #postavljamo pozadinu
        self.background = pygame.image.load("image.jpg").convert()
        self.background = pygame.transform.scale(self.background, (24*33, 18*33))
        self.screen.blit(self.background, (0, 0))

        #Postavljamo zmiju, jabuku, display i game over display
        self.snake = snake()
        self.apple = apple()
        self.display = display()
        self.game_over_display = game_over_display()
        self.start_game_display = start_game_display()

        self.score = 0
        self.game_pause = False
        self.runnig = True

    def start_game(self):
        self.start_game_display.draw(self.screen)
        while self.runnig:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runnig = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    return

    def run(self):
        self.runnig = True
        while self.runnig:
            for event in pygame.event.get():
                #za izlaz iz igre
                if event.type == pygame.QUIT:
                    self.runnig = False
                    pygame.quit()
                    sys.exit()


                if event.type == pygame.KEYDOWN:

                    #ako je igra pauzirana i pritisnemo enter igra se resetira i nastavlja
                    if self.game_pause == True and event.key == pygame.K_RETURN:
                        snake.__init__(self.snake)
                        apple.__init__(self.apple)
                        self.score = 0
                        self.game_pause = False

                    #ako igra nije pauzirana gledamo koji se botun pritisnuo
                    if self.game_pause == False:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.snake.chane_direction('up')
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.snake.chane_direction('down')
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.snake.chane_direction('left')
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.snake.chane_direction('right')

            
            if self.game_pause == False:

                self.snake.move()
                #prvo provjeravamo jel zmija pojela jabuku, pa onda jel pojela sama sebe ili izašla iz okvira
                if self.snake.eat_apple(self.apple):
                    self.score += 1
                    self.apple.set_apple_random(self.snake)
                
                if self.snake.check_gameover():
                    self.game_over_display.draw(self.screen)
                    self.game_pause = True

                #ako je zmija pojela jabuku povecava zmiju
                if len(self.snake.x) != self.score + 5:
                    self.snake.x.append(self.snake.x[len(self.snake.x)-1])
                    self.snake.y.append(self.snake.y[len(self.snake.y)-1])
                

                #prvo stvara pozadinu, pa crta zmiju i jabuku pa ispisuje score
                self.screen.blit(self.background, (0, 0))
                self.snake.draw(self.screen)
                self.apple.draw(self.screen)
                self.display.draw(self.screen, self.score)

            else:
                #ako je igra pauzirana ispisuje se ispisuje game over display
                self.game_over_display.draw(self.screen)


            pygame.display.update()
            
            time.sleep(0.2 - self.score/500 )

game = game()
game.start_game()
game.run()

                    
                        

