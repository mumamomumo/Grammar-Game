import pygame
import random
import pygame_textinput
import time

pygame.init()

WIN = pygame.display.set_mode((500, 500))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

clock = pygame.time.Clock()
sen_list = ['The cat is big', 'The spider ran', "He likes to talk", "He can create games", "The cat hissed"]

textinput = pygame_textinput.TextInputVisualizer()

# [type, choose, correct, wrong]



font = pygame.font.SysFont('Arial', 50)




class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text:str,  pos:tuple, font:int, bg="gray"):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.clicked = False
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x-5, self.y-5, self.size[0]+5, self.size[1]+5)

    def do(self):
        WIN.fill(0)
        self.clicked = True
        print('clicked')

    def show(self):
        if self.clicked == False:
            WIN.blit(self.surface, (self.x, self.y))

    def hide(self):
        self.text = False
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.do()


startButton = Button("Start",(200, 100), 50)

class mainMenu:
    def __init__(self):
        self.in_main = True

    def startButton(self, event):
        if startButton.clicked == False:
            startButton.show()
            if self.in_main:
                startButton.click(event)
        else:
            self.in_main = False
    

def timer(i: int):
    pygame.draw.rect(WIN, (200, 0, 0+(i/2)), pygame.Rect(400, 100+1, 50, 400-i))
    

def sentences():
    global sen
    sen = random.choice(sen_list)
    sen_list.remove(sen)
    
    return sen


menu = mainMenu()

def main():
    # ingredients
    ans = False
    font = pygame.font.Font('freesansbold.ttf', 32)
    gameState = 'choose'
    i = 1
    cheat = 0
    # steps
    while True:
        clock.tick(30)
        events = pygame.event.get()

        if not(menu.in_main):
            WIN.fill((250, 90, 100))
            #game
            WIN.blit(font.render('Unscramble this sentence:', True, (100, 250, 150)), (50, 50))
            if gameState == 'choose':
                sen = sentences()
                sen_shuf = list(set(sen.split()))
                
                print(sen_shuf)
                ans = False
                textinput.value = ''
                i=1
                cheat = 1
                gameState = 'type'
            if gameState == 'type':
                # question
                timer(i)
                text = font.render(" ".join(sen_shuf), True, (50, 0,200), (0,0,0)) 
                textRect = text.get_rect()
                textRect.center = (250, 250)
                textRect.y = 100

                # input box
                textinput.update(events)

                # blit
                WIN.blit(font.render(" ".join(sen_shuf), True, (50, 0,200), (0,0,0)), textRect)
                WIN.blit(textinput.surface, (75, 250))
                
                #check if correct
                if ans and ans.lower() == sen.lower():
                    print('correct')
                    time.sleep(1)
                    gameState = 'choose'
                elif ans and ans.lower != sen.lower():
                    print("wrong")
                    sen_list.append(sen)
                    gameState = 'choose'
                elif i >400:
                    print("Out of time")
                    sen_list.append(sen)
                    gameState = 'choose'
                i+=1
            
                if cheat == 2:
                    print("No doing that please")
                    pygame.quit()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.VIDEOEXPOSE:
                cheat += 1
            menu.startButton(event)
            if not(menu.in_main):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    ans = textinput.value
        pygame.display.update()


if __name__ == "__main__":
    main()