import pygame
import random
import inputbox
pygame.init()

# All Global Variables Are Declared Below This Line
display_width = 800
display_height = 600

# Colors Declaration
white = (255,255,255)
black = (0,0,0)
red = (223,0,0)
amber = (247,218,0)
blue = (77,215,250,0)
dark_blue = (182, 239, 252)
green = (0, 216, 29)

# Creating window for gaming screen & Caption
gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.HWSURFACE | pygame.DOUBLEBUF )
pygame.display.set_caption('Asteroid Evader')
#frames per second
fps = pygame.time.Clock()
background = pygame.Surface(gameDisplay.get_size())
#Convert to color maps
background = background.convert()

# Backgrounds & Game Screen
intro_screen = pygame.image.load('screens/Intro Screen.jpg')
menu_screen = pygame.image.load('screens/menu_screen.png')
how_to_screen = pygame.image.load('screens/how_to_play.png')
gaming_screen = pygame.image.load('screens/gaming_screen.png')
gender_screen = pygame.image.load('screens/gender_select.png')
character_maleimg = pygame.image.load('screens/character_male.png')
character_femaleimg = pygame.image.load('screens/character_female.png')
highscore_screen = pygame.image.load('screens/highscore.png')
dashboard = pygame.image.load('screens/dashboard.png')
name_screen = pygame.image.load('screens/name_select.png')
settings_screen = pygame.image.load('screens/settings.png')
gameover_screen = pygame.image.load('screens/Game_screen.png')
paused_screen_img = pygame.image.load('screens/Paused_screen.png')

#list of spaceships to choose from
spaceship1 = pygame.image.load('assets/spaceships/ship1.png')
spaceship2 = pygame.image.load('assets/spaceships/ship2.png')
spaceship3 = pygame.image.load('assets/spaceships/ship3.png')
spaceship4 = pygame.image.load('assets/spaceships/ship4.png')

#rock
asteroid = pygame.image.load('assets/rocks/a.png')
#mines
mine1 = pygame.image.load('assets/mine/mine1.png')
mine2 = pygame.image.load('assets/mine/mine2.png')
mine3 = pygame.image.load('assets/mine/mine3.png')


# List of Music Files
intro_music = pygame.mixer.Sound("music/intro_music.wav")
menu_music = pygame.mixer.Sound("music/menu_music.wav")
game_music = pygame.mixer.Sound('music/gaming.wav')
game_music1 = pygame.mixer.Sound('music/gaming1.wav')

#icons
settings_icon = pygame.image.load('assets/icons/settings.png')
back_icon = pygame.image.load('assets/icons/back.png')

# fx sounds
clicked = pygame.mixer.Sound('fx/clicks.wav')
crashed = pygame.mixer.Sound('fx/crash.wav')
powerup = pygame.mixer.Sound('fx/powerup.wav')
health_powerup = pygame.image.load('assets/powerups/health.png')
speed_powerup = pygame.image.load('assets/powerups/speed.png')
username = None

#Character - Males
character_1 = pygame.image.load('assets/avatar/char_1.png')
character_2 = pygame.image.load('assets/avatar/char_2.png')
character_3 = pygame.image.load('assets/avatar/char_3.png')

#Character - Females
character_4 = pygame.image.load('assets/avatar/char_4.png')
character_5 = pygame.image.load('assets/avatar/char_5.png')
character_6 = pygame.image.load('assets/avatar/char_6.png')


#Stars - Blue


# Global variables for running functions
character_img = None
current_charnum = None
run_settings = False
how_to_play = False
paused = False
running = False


score = 0

#Stops the pause function from running
def unpause():
    global paused
    paused = False
#Stops the high score function from running
def not_highscore():
    global running
    running = False
#Stops the how to play function from running
def how_to_play_none():
    global how_to_play
    how_to_play = False
#Stops the settings function from running
def not_settings():
    global run_settings
    run_settings = False


#This class is used to display different screens
class DisplayScreen(object):
    #converts image to picels
    def __init__(self, image):
        self.image = image.convert()

    #this method only shows the screen
    def show(self):
        gameDisplay.blit(self.image,(0,0))

    #This method fades the screen in and out
    def fade(self,time):
        self.time = time
        fading = True
        if fading:
            for i in range(255):
                background.fill(black)
                self.image.set_alpha(i)
                gameDisplay.blit(self.image,(0,0))
                pygame.display.flip()
                pygame.time.delay(time)
            for i in range(255):
                background.fill(black)
                background.set_alpha(i)
                gameDisplay.blit(background,(0,0))
                pygame.display.flip()
                pygame.time.delay(time)

#This class is used to display text onto the surface
class DisplayText(object):
    def __init__(self,text,color,size):
        self.text = text
        self.color = color
        self.size = size
    #method for acquiring text
    def texts(self, text, font):
        TextSurf = font.render(text, True, self.color)
        return TextSurf, TextSurf.get_rect()
    #This method is used for only displaying text onto the screen
    def show(self):
        main_text = pygame.font.Font('freesansbold.ttf',self.size)
        TextSurf, TextRect = DisplayText.texts(self.text, main_text)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
    #This method is used for displaying text as buttons
    def buttons(self,x,y,width,height,inactive,active,text_size, action=None):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
            pygame.draw.rect(gameDisplay, active,(x,y,width,height))

            if click[0] == 1 and action is not None:
                #if the button is clicked then another function is called.
                clicked.play()
                action()
        else:
            pygame.draw.rect(gameDisplay, inactive, (x,y,width,height))

        buttonText = pygame.font.Font('fonts/Montserrat-Hairline.otf', self.size)
        textSurf, textRect = DisplayText.texts(self,self.text,buttonText)
        textRect.center = ( (x+(width/2)) , (y +(height/2)) )
        gameDisplay.blit(textSurf, textRect)


#This class is used to load actors which you can't control into screens into screen
class NonActor(pygame.sprite.Sprite):
    def __init__(self, image, x,y,width,height,direction,speed):
        super(NonActor, self).__init__()
        self.image = image.convert_alpha()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed

    #This method is used for moving actors
    def move(self):
        gameDisplay.blit(self.image,(self.x,self.y))
        if self.direction == 'down':
            self.y += self.speed
            if self.y > display_height:
                self.y = 0
        if self.direction == 'up':
            self.y -= self.speed
            if self.y < display_height:
                self.y = 600 + self.height
        if self.direction == 'right':
            self.x += self.speed
            if self.x >= (display_width + self.width):
                self.x = 0
        if self.direction == 'left':
            self.x -= self.speed
            if self.x < display_width:
                print('X is smaller')
                self.x = 0 + self.width


#Same as above
class Stars(pygame.sprite.Sprite):
    def __init__(self, x,y,width,height,color,direction,speed):
        self.x = x
        self.y = y
        self.width = width
        self.height= height
        self.color = color
        self.direction = direction
        self.speed = speed

    def move(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])
        if self.direction == 'down':
            self.y += self.speed
            if self.y > display_height:
                self.y = 0
                self.x = random.randrange(0,display_width)
        if self.direction == 'up':
            self.y -= self.speed
            if self.y < display_height:
                self.y = display_height + self.height
                self.x = random.randrange(0,display_width)
        if self.direction == 'right':
            self.x += self.speed
            if self.x > display_width:
                self.x = 0
        if self.direction == 'left':
            self.x -= self.speed
            if self.x < display_height:
                self.x = 0 + self.width


star1 = Stars(random.randrange(0,display_width),-430, 2,20,blue, 'down',19)
star2 = Stars(random.randrange(0,display_width),-345, 2,20,blue, 'down',21)
star3 = Stars(random.randrange(0,display_width),-452, 2,20,blue, 'down',8)
star4 = Stars(random.randrange(0,display_width),-542, 2,27,blue, 'down',12)
star5 = Stars(random.randrange(0,display_width),-645, 2,29,blue, 'down',16)
star6 = Stars(random.randrange(0,display_width),-732, 2,23,blue, 'down',15)

#Function displays main menu screen.
def MenuScreen():
    pygame.time.delay(100)
    menu = True
    start_game_button = DisplayText('Start Game',black,14)
    how_to_play_button = DisplayText('How To Play',black,14)
    highscore_button = DisplayText('Highscores',black,14)
    settings_button = DisplayText('',black,14)
    screen = DisplayScreen(menu_screen)


    while menu:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.show()
        start_game_button.buttons(293,340,212,52, blue, white, 14, GenderScreen)
        how_to_play_button.buttons(293,405,212,52, blue, white, 14, HowToPlayScreen)
        highscore_button.buttons(293,469,212,52, blue, white, 14, HighscoreScreen)
        settings_button.buttons(760, 0, 40, 38, blue, white, 14, SettingsScreen)

        star1.move()
        star3.move()
        star4.move()
        star2.move()
        star5.move()
        star6.move()
        pygame.display.update()
        fps.tick(60)

#Displays the paused screen
def PausedScreen():
    pygame.time.delay(100)
    paused = True
    screen = DisplayScreen(paused_screen_img)
    star1 = Stars(random.randrange(0,(display_width - 1)),-900,1,21,dark_blue,'down',12)
    star2 = Stars(random.randrange(0,(display_width - 1)),-900,1,21,dark_blue,'down',12)
    star3 = Stars(random.randrange(0,(display_width - 1)),-900,1,21,dark_blue,'down',12)
    star4 = Stars(random.randrange(0,(display_width - 1)),-900,1,21,dark_blue,'down',12)
    star5 = Stars(random.randrange(0,(display_width - 1)),-900,1,21,dark_blue,'down',12)
    star6 = Stars(random.randrange(0,(display_width - 1)),-900,1,21,dark_blue,'down',12)
    resume = DisplayText('',blue,14)

    while paused:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.show()
        star1.move()
        star2.move()
        star3.move()
        star4.move()
        star5.move()
        star6.move()


        resume.buttons(293,340,212,52,blue,white,resume.text,unpause)
        pygame.display.update()
        fps.tick(60)

#Displays the how to play screen
def HowToPlayScreen():
    pygame.time.delay(100)
    how_to_play = True
    screen = DisplayScreen(how_to_screen)
    star1 = Stars(random.randrange(0,display_width),-430, 2,20,blue, 'down',19)
    star2 = Stars(random.randrange(0,display_width),-345, 2,20,blue, 'down',21)
    star3 = Stars(random.randrange(0,display_width),-452, 2,20,blue, 'down',8)
    star4 = Stars(random.randrange(0,display_width),-542, 2,27,blue, 'down',12)
    star5 = Stars(random.randrange(0,display_width),-645, 2,29,blue, 'down',16)
    star6 = Stars(random.randrange(0,display_width),-732, 2,23,blue, 'down',15)

    back_button = DisplayText('',black,14)
    settings = DisplayText('',black,14)

    while how_to_play:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.show()
        back_button.buttons( 0, 0, 40, 38, blue, white,14,MenuScreen)
        gameDisplay.blit(back_icon,(10,10))
        star1.move()
        star3.move()
        star4.move()
        star2.move()
        star5.move()
        star6.move()

        settings.buttons(760, 0, 40, 38, blue, white,14, SettingsScreen)
        gameDisplay.blit(settings_icon,(772,10))
        pygame.display.update()
        fps.tick(60)

#Displays the gender screen

def GenderScreen():
    pygame.time.delay(100)
    gender = True
    star1 = Stars(random.randrange(0,display_width),-430, 2,20,blue, 'down',19)
    star2 = Stars(random.randrange(0,display_width),-345, 2,20,blue, 'up',21)
    star3 = Stars(random.randrange(0,display_width),-452, 2,20,blue, 'down',8)
    star4 = Stars(random.randrange(0,display_width),-542, 2,27,blue, 'down',12)
    star5 = Stars(random.randrange(0,display_width),-645, 2,29,blue, 'down',16)
    star6 = Stars(random.randrange(0,display_width),-732, 2,23,blue, 'down',15)
    screen = DisplayScreen(gender_screen)
    male = DisplayText('MALE',black,15)
    female = DisplayText('FEMALE',black,15)
    back = DisplayText('',blue,15)
    settings = DisplayText('',blue,15)

    while gender:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.show()
        star1.move()
        star2.move()
        star3.move()
        star4.move()
        star5.move()
        star6.move()

        male.buttons(126,300,203,64,blue,white,15,CharMaleScreen)
        female.buttons(494, 300, 203, 64,blue,white,15,CharFemaleScreen)
        back.buttons(0, 0, 40, 38, blue, white,14, MenuScreen)
        gameDisplay.blit(back_icon,(10,10))

        settings.buttons(760, 0, 40, 38, blue, white,14, SettingsScreen)
        gameDisplay.blit(settings_icon,(772,10))
        pygame.display.update()
        fps.tick(60)

#Displays the name selection screen

def NameScreen():
    selection = False
    pygame.time.delay(50)
    DisplayScreen(name_screen)
    back = DisplayText('blue',blue,14)
    settings = DisplayText('',blue,14)

    back.buttons(0, 0, 40, 38, blue, white,14, MenuScreen)

    gameDisplay.blit(back_icon,(10,10))

    settings.buttons(760, 0, 40, 38, blue, white,14, settings)
    gameDisplay.blit(settings_icon,(772,10))
    global username
    username = inputbox.ask(gameDisplay, '')
    pygame.display.update()

#Displays the character male screen
def CharMaleScreen():
    pygame.time.delay(100)
    selection = True
    star1 = Stars(random.randrange(0,display_width),-430, 2,20,blue, 'down',19)
    star2 = Stars(random.randrange(0,display_width),-345, 2,20,blue, 'down',21)
    star3 = Stars(random.randrange(0,display_width),-452, 2,20,blue, 'down',8)
    star4 = Stars(random.randrange(0,display_width),-542, 2,27,blue, 'down',12)
    star5 = Stars(random.randrange(0,display_width),-645, 2,29,blue, 'down',16)
    star6 = Stars(random.randrange(0,display_width),-732, 2,23,blue, 'down',15)
    screen = DisplayScreen(character_maleimg)
    choice1 = DisplayText('CHOOSE ME',black,12)
    choice2 = DisplayText('CHOOSE ME',black,12)
    choice3 = DisplayText('CHOOSE ME',black,12)
    back = DisplayText('',black,12)
    settings = DisplayText('',black,12)
    while selection:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.show()
        star1.move()
        star2.move()
        star3.move()
        star4.move()
        star5.move()
        star6.move()

        choice1.buttons(127, 357, 134, 36, blue, dark_blue, 12, char_1)
        choice2.buttons(333, 359, 134, 36, blue, dark_blue, 12, char_2)
        choice3.buttons(539, 357, 134, 36, blue, dark_blue, 12, char_3)
        back.buttons(0, 0, 40, 38, blue, white,14, GenderScreen)
        gameDisplay.blit(back_icon,(10,10))

        settings.buttons(760, 0, 40, 38, blue, white,14, SettingsScreen)
        gameDisplay.blit(settings_icon,(772,10))
        pygame.display.update()
        fps.tick(60)

#Displays the character_female screen
def CharFemaleScreen():
    pygame.time.delay(100)
    selection = True
    star1 = Stars(random.randrange(0,display_width),-430, 2,20,blue, 'down',19)
    star2 = Stars(random.randrange(0,display_width),-345, 2,20,blue, 'down',21)
    star3 = Stars(random.randrange(0,display_width),-452, 2,20,blue, 'down',8)
    star4 = Stars(random.randrange(0,display_width),-542, 2,27,blue, 'down',12)
    star5 = Stars(random.randrange(0,display_width),-645, 2,29,blue, 'down',16)
    star6 = Stars(random.randrange(0,display_width),-732, 2,23,blue, 'down',15)

    screen = DisplayScreen(character_femaleimg)
    choice1 = DisplayText('CHOOSE ME',black,12)
    choice2 = DisplayText('CHOOSE ME',black,12)
    choice3 = DisplayText('CHOOSE ME',black,12)
    back = DisplayText('',black,12)
    settings = DisplayText('',black,12)

    while selection:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.show()
        star1.move()
        star2.move()
        star3.move()
        star4.move()
        star5.move()
        star6.move()

        choice1.buttons(127, 357, 134, 36, blue, dark_blue, 12, char_4)
        choice2.buttons(333, 359, 134, 36, blue, dark_blue, 12, char_5)
        choice3.buttons(539, 357, 134, 36, blue, dark_blue, 12, char_6)
        back.buttons(0, 0, 40, 38, blue, white,14, GenderScreen)
        gameDisplay.blit(back_icon,(10,10))

        settings.buttons(760, 0, 40, 38, blue, white,14, SettingsScreen)
        gameDisplay.blit(settings_icon,(772,10))
        pygame.display.update()
        fps.tick(60)

#Displays the high score screen
def HighscoreScreen():
    temp_image = None
    file = open('highscores.txt','r')
    for line in file:
        print(line)
    if line[0] == '1':
        temp_image = character_1
    if line[0] == '2':
        temp_image = character_2
    if line[0] == '3':
        temp_image = character_3
    if line[0] == '4':
        temp_image = character_4
    if line[0] == '5':
        temp_image = character_5
    if line[0] == '6':
        temp_image = character_6

    pygame.time.delay(100)
    global running
    running = True
    star1 = Stars(random.randrange(0,display_width),-430, 2,20,blue, 'down',19)
    star2 = Stars(random.randrange(0,display_width),-345, 2,20,blue, 'down',21)
    star3 = Stars(random.randrange(0,display_width),-452, 2,20,blue, 'down',8)
    star4 = Stars(random.randrange(0,display_width),-542, 2,27,blue, 'down',12)
    star5 = Stars(random.randrange(0,display_width),-645, 2,29,blue, 'down',16)
    star6 = Stars(random.randrange(0,display_width),-732, 2,23,blue, 'down',15)
    screen = DisplayScreen(highscore_screen)
    back = DisplayText('',black,14)
    settings = DisplayText('',black,14)

    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.show()
        star1.move()
        star2.move()
        star3.move()
        star4.move()
        star5.move()
        star6.move()


        back.buttons(0, 0, 40, 38, blue, white,14, not_highscore)
        gameDisplay.blit(back_icon,(10,10))
        settings.buttons(760, 0, 40, 38, blue, white,14, settings)
        gameDisplay.blit(settings_icon,(772,10))
        gameDisplay.blit(temp_image,(550,401))
        pygame.display.update()
        fps.tick(60)

#Displays every function below is to change the current character image.
def char_1():
    global character_img
    global current_charnum
    current_charnum = 1
    character_img = character_1
    NameScreen()
def char_2():
    global character_img
    global current_charnum
    current_charnum = 2
    character_img = character_2
    NameScreen()
def char_3():
    global character_img
    global current_charnum
    current_charnum = 3
    character_img = character_3
    NameScreen()
def char_4():
    global character_img
    global current_charnum
    current_charnum = 4
    character_img = character_4
    NameScreen()
def char_5():
    global character_img
    global current_charnum
    current_charnum = 5
    character_img = character_5
    NameScreen()
def char_6():
    global character_img
    global current_charnum
    current_charnum = 6
    character_img = character_6
    NameScreen()

#Displays the soaceship
def spaceship(spaceship,x,y):
    height = 32
    width = 32
    gameDisplay.blit(spaceship,(x,y),(random.randrange(0,4) * width, 0, width, height))

#Displays the settings screen

def SettingsScreen():
    global run_settings
    run_settings = True
    star1 = Stars(random.randrange(0,display_width),-430, 2,20,blue, 'down',19)
    star2 = Stars(random.randrange(0,display_width),-345, 2,20,blue, 'up',21)
    star3 = Stars(random.randrange(0,display_width),-452, 2,20,blue, 'down',8)
    star4 = Stars(random.randrange(0,display_width),-542, 2,27,blue, 'down',12)
    star5 = Stars(random.randrange(0,display_width),-645, 2,29,blue, 'down',16)
    star6 = Stars(random.randrange(0,display_width),-732, 2,23,blue, 'down',15)
    screen = DisplayScreen(settings_screen)
    sound_off = DisplayText('Sound Off',black,12)
    sound_on = DisplayText('Sound On',black,12)
    website = DisplayText('Website',black,12)
    back = DisplayText('',black,14)

    while run_settings:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.show()
        star1.move()
        star2.move()
        star3.move()
        star4.move()
        star5.move()
        star6.move()

        sound_off.buttons(400, 206, 100, 36, blue, dark_blue, 12, sound_off)
        sound_on.buttons(500, 206, 100, 36, blue, dark_blue, 12, sound_on)
        website.buttons(400, 280, 150, 36, blue, dark_blue, 12)
        back.buttons(0, 0, 40, 38, blue, white,14, not_settings)
        gameDisplay.blit(back_icon,(10,10))
        pygame.display.update()
        fps.tick(60)

#Displays the game over screen

def game_over():
    file = open('highscores.txt', 'a')
    file.write( str(current_charnum)  + ' ' + username + ' ' + str(score))
    star1 = Stars(random.randrange(0,display_width),-430, 2,20,blue, 'down',19)
    star2 = Stars(random.randrange(0,display_width),-345, 2,20,blue, 'down',21)
    star3 = Stars(random.randrange(0,display_width),-452, 2,20,blue, 'down',8)
    star4 = Stars(random.randrange(0,display_width),-542, 2,27,blue, 'down',12)
    star5 = Stars(random.randrange(0,display_width),-645, 2,29,blue, 'down',16)
    star6 = Stars(random.randrange(0,display_width),-732, 2,23,blue, 'down',15)
    screen = DisplayScreen(gameover_screen)
    back = DisplayText('Back To Main Menu',blue,white)
    game_over = True
    intro_music.stop()
    menu_music.stop()
    game_music.stop()
    while game_over:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.show()
        star1.move()
        star2.move()
        star3.move()
        star4.move()
        star5.move()
        star6.move()

        back.buttons(295, 383, 212, 52, blue, white,14, MenuScreen)
        pygame.display.update()
        fps.tick(60)

#Switches on sound

def sound_on():
    intro_music.stop()
    menu_music.play()
    game_music.stop()

#Switches off sound
def sound_off():
    intro_music.stop()
    menu_music.stop()
    game_music.stop()

#Displays obstacles
def obstacle(obstacle,obx,oby):
    gameDisplay.blit(obstacle,(obx,oby))


#displays the highscore
def highscore(score):
    font = pygame.font.Font('fonts/Montserrat-Regular.otf', 15)
    text = font.render(str(score), True, white)
    if score <= 1:
        gameDisplay.blit(text,(395,40))
    if score <= 10 and score > 1:
        gameDisplay.blit(text,(395,40))
    if score > 10 and score < 100:
        gameDisplay.blit(text,(390,40))
    if score >= 100 and score < 1000:
        gameDisplay.blit(text,(385,40))
    if score > 1000 and score < 10000:
        gameDisplay.blit(text,(380,40))

#displays the character image
def character(image,name,health,color):
    font = pygame.font.Font('fonts/Montserrat-Hairline.otf', 15)
    text = font.render(str(name), True, white)
    score = font.render(('SCORE'), True, white)
    if health >= 60:
        color = green
    if health <= 60 and health > 30:
        color = amber
    if health <= 30:
        color = red
    if health <= 0:
        health = 0
    text2 = font.render(str(health) + ' %', True, color)
    gameDisplay.blit(text,(65,9))
    gameDisplay.blit(score, (370,8))
    gameDisplay.blit(text2,(255,9))
    gameDisplay.blit(image,(10,4))


#displays the moving stars

#executes the actual game function
def game():
    # initiates the name selection function after the game begins
    NameScreen()
    menu_music.stop()
    game_music.play(-1)

    #sets the x coordinates and y coordinates for the spaceship
    x = 384
    y = (display_height * 0.8)

    # y & x change are variables needed to move the spaceship when button is pressed
    x_change = 0
    y_change = 0

    #condition loops
    EXIT = False #checks to see if exit button has been pressed
    begin = False #checks to see if the game has begun
    paused = False #checks to see if the game has been paused

    #current score
    score = 0

    #Mine - First obstacle
    mine1_x = random.randrange(0,display_width)
    mine1_y = -3200
    mine1_speed = 4

    #Mine2 - Second Obstacle
    mine2_x = random.randrange(0,display_width)
    mine2_y = -3900
    mine2_speed = 5

    #Mine3 - Third Obstacle
    mine3_x = random.randrange(0,display_width)
    mine3_y = -4100
    mine3_speed = 7

    #star 1 - Movement effects of the first star
    star_X = random.randrange(0,display_width)
    star_Y = - 349
    star_width = 2
    star_height = 20

    #star 2 - Movement effects of the second star
    star_X2 = random.randrange(0,display_width)
    star_Y2 = - 500
    star_width2 = 1
    star_height2 = 19

    #star 3 - Movement effects of the third star
    star_X3 = random.randrange(0,display_width)
    star_Y3 = - 154
    star_width3 = 3
    star_height3 = 10

    #star 4 - Movement effects of the fourth star
    star_X4 = random.randrange(0,display_width)
    star_Y4 = - 590
    star_width4 = 1
    star_height4 = 15

    #asteroid - the fifth asteroid
    asteroid_X = 900
    asteroid_Y = random.randrange(0,display_height - 133)

    # Character

    # Character - Health
    health = 100
    health_x = random.randrange(0,display_width)
    health_y = random.randrange(3000, 10000)
    health_y = health_y * -1

    speed_x = random.randrange(0, display_width)
    speed_y = random.randrange(3000, 10000)

    #if the exit button isn't pressed, then continue running the game
    while not EXIT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #moves the spaceship or pause the game when some buttons are pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    y_change = 5
                if event.key == pygame.K_p:
                    pausedd()
            #stops all movement of the spaceship in the game
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    y_change = 0


        # Moves spaceship by the value of  x_ or y_ change dependent on what was de
        x += x_change
        y += y_change

        #Moves spaceship once that game screen is displayed, shows the users that spaceships are movable
        if begin == False:
            y -= 1
            if y < 400:
                y += y_change
                begin = True


        #Displays the gaming screen (background)
        DisplayScreen(gaming_screen)

        #Detects whether spaceship collided with border
        if x > display_width - 32:
            x_change = 0
        if x <0:
            x_change = 0
        if y > display_height - 64:
            y_change = 0
        if y < 90:
            y_change = 0

        #Detects if the first obstacle as crashed with the spaceship
        if y < mine1_y + 48 and y > mine1_y - 48:
            print ('Ship has crossed the Mines In Y')
            if x > mine1_x and x < mine1_x + 48 or x + 32 > mine1_x and x + 32 < mine1_x + 32:
                crashed.play()
                mine1_y = - 900
                mine1_x = random.randrange(0,display_width)
                mine1_speed += 0.5
                mine1_y += mine1_speed
                score -= 15
                health = health - 3

        #Detects if the second obstacle as crashed with the spaceship
        if y < mine2_y + 48 and y > mine2_y - 48:
            print ('Ship has crossed the Mines In Y')
            if x > mine2_x and x < mine2_x + 48 or x + 32 > mine2_x and x + 32 < mine2_x + 32:
                crashed.play()
                mine2_y = - 900
                mine2_x = random.randrange(0,display_width)
                mine2_speed += 0.5
                mine2_y += mine2_speed
                score -= 25
                health = health - 5

        #Detects if the third obstacle as crashed with the spaceship
        if y < mine3_y + 48 and y > mine3_y - 48:
            print ('Ship has crossed the Mines In Y')
            if x > mine3_x and x < mine3_x + 48 or x + 32 > mine3_x and x + 32 < mine3_x + 32:
                crashed.play()
                mine3_y = - 900
                mine3_x = random.randrange(0,display_width)
                mine3_speed += 0.5
                mine3_y += mine3_speed
                score += 5
                health = health - 1
        #Displays the spacehip onto the screen
        spaceship(spaceship2,x,y)



        obstacle(mine1,mine1_x,mine1_y) #creates first obstacle
        obstacle(mine2,mine2_x,mine2_y)#creates second obstacle
        obstacle(mine3,mine3_x,mine3_y)#creates third obstacle

        mine1_y += mine1_speed # Moves first obstacle
        mine2_y += mine2_speed # Moves second obstacle
        mine3_y += mine3_speed # Moves third obstacle

        # checks to see if any of the three obstacles are greater than the display
        # height, if they are then they are position to the top of the screen'
        if mine1_y > display_height:
            mine1_y = - 900
            mine1_x = random.randrange(0,display_width)
            mine1_speed += 0.2
            mine1_y += mine1_speed
            score += 15


        if mine2_y > display_height:
            mine2_y = - 500
            mine2_x = random.randrange(0,display_width)
            mine2_speed += 0.2
            mine2_y += mine2_speed
            score += 15

        if mine3_y > display_height:
            mine3_y = - 500
            mine3_x = random.randrange(0,display_width)
            mine3_speed += 0.2
            mine3_y += mine3_speed
            score += 15


        star(star_X,star_Y,star_width,star_height,blue) #creation of the first star
        star(star_X2,star_Y2,star_width2,star_height2,blue) #creation of the second star
        star(star_X3,star_Y3,star_width3,star_height3,blue) #creation of the third star
        star(star_X4,star_Y4,star_width4,star_height4,blue) #creation of the fourth star

        # The code below is concerned with moving each star down the screen by 25 pixels
        star_Y += 25
        star_Y2 += 25
        star_Y3 += 25
        star_Y4 += 25

        #This code checks to see if the star is greater than the display_height
        if star_Y > display_height:
            star_Y = -50
            star_X = random.randrange(0,display_width)
        if star_Y2 > display_height:
            star_Y2 = -150
            star_X = random.randrange(0,display_width)
        if star_Y3 > display_height:
            star_Y3 = -200
            star_X3 = random.randrange(0,display_width)
        if star_Y4 > display_height:
            star_Y4 = -300
            star_X4 = random.randrange(0,display_width)

        #This code checks to see if the players score is above or equaled to 500
        #if yes then a new obstacle is introduced... The asteroid.
        if score >= 500:
           obstacle(asteroid,asteroid_X,asteroid_Y) # Creates asteroid
           asteroid_X -= 6 # Asteroid is moved horizontally by 6pixels
           #the line below checks to see if the y coordinates of the spaceship and
           #asteroid has crossed
           if y < asteroid_Y + 114 and y > asteroid_Y - 114:
                #checks to see if the x cooridinates of the spaceship and asteroid are crossed
               if x > asteroid_X and x < asteroid_X + 42 or x + 32 > asteroid_X and x + 32 < asteroid_X + 32:
                    crashed.play() #plays crashed sound
                    asteroid_X = random.randint(display_width,1000) #resets x position of  asteroid
                    asteroid_Y = random.randrange(0,display_height-133) #resets y position of asteroid
                    health = health - 25 # decreases health
           elif asteroid_X <= 0 - 133: # checks to see if asteroid made it to other side of the screen
            asteroid_X = random.randint(display_width,1000) # resets x position of asteroid
            asteroid_Y = random.randrange(0,display_height-133)# resets y position of asteroid


        obstacle(health_powerup,health_x,health_y) # creates health powerup
        health_y += 5  #moves health down by 5 pixels

        #checks to see if and y coordinate of spaceship and powerup are crossed
        if y < health_y + 42 and y > health_y - 42:
            if x > health_x and x < health_x + 42 or x + 32 > health_x and x + 32 < health_x + 32:
                powerup.play() #plays powerup sound
                health_y = random.randrange(5000, 10000) #resets position of health_y
                health_y = health_y * -1 #Makes it negative so it's at the top
                health_x = random.randrange(0,display_width-32) #places health_x in a new location
                health = health + 25 #increases health
                if health > 100: # makes sure that health never goes above 0
                    health = 100

        obstacle(speed_powerup,speed_x,speed_y) #creates speed powerup
        speed_y += 5 #moves speed powerup down by 5 pixels

        #checks to see if and y coordinate of spaceship and powerup are crossed
        if y < speed_y + 42 and y > speed_y - 42:
            if x > speed_x and x < speed_x + 42 or x + 32 > speed_x and x + 32 < speed_x + 32:
                powerup.play() #plays powerup sound
                speed_y = random.randrange(5000, 10000) #resets position of speed_y
                speed_y = health_y * -1 #Makes it negative so it's at the top
                speed_x = random.randrange(0, display_width - 42) #places speed_x in a new location
                x_change += 5 #speeds up spaceship by 5 pixels

        display_screen(dashboard,0,0) # displays dashboard at the top of the screen
        #Displays character image,name, and health to he top of the screen
        character(character_img, (username[0].upper()+username[1:]),health, None)
        #displays button for paused screen
        buttons('', 760, 0, 40, 38, blue, white,14, pausedd)
        gameDisplay.blit(settings_icon,(772,10))
        #displays current score to the top of the screen above the dashboard
        highscore(score)

        # if the score is smaller than 1 then it's equalleed to 0
        # This stops any negative number being created'
        if score < 1:
            score = 0
        if health <= 0:
            game_over() #calls the gameover function


menu_music.play(-1)
MenuScreen()
pygame.quit()
quit()