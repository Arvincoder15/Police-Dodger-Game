#---------------------------------------------------------------------------------------------------------------
# Program: Tkinter and Police Dodger Game Program 
# Authors: Arvin Askari
# Date: Wednesday, June 12, 2024
#
# Description: This program contains a Tkinter-based timer application and a Pygame-based police 
#   dodger game. The game involves dodging police cars while navigating a road until the car crashes
#   either into a wall or the police car. The Tkinter application serves as a timer. Users can start, 
#   stop, reset the timer, and even close the timer. In the game, there are controls within the game 
#   to pause, restart, or quit the game. The Tkinter timer can also be used as a stopwatch to track
#   how long the user has been playing the game or how long they are able to survive by avoiding 
#   the police car. The main intent of the police dodger game is to avoid the police car while trying
#   reach and beat the user's personal high score every time the user plays the game. The game will run
#   forever until the user decides to quit the game or if the user crashes into a wall or the police car.
#
# Input: The user inputs if they would like to start the timer. Once that is started, user can input the 
#   the instructions button to read how the game works then prompt the user to start the game. Once the
#   user decides to start the game, the game will begin and the user will be prompted to uses keybo and inputs 
#   to control the car (arrow keys or WASD) and mouse inputs for button  interactions. The Tkinter timer 
#   uses button inputs for start, stop, reset, and exit actions. Lastly, the user can input 'p' to pause
#   the game or when the game is finished to exit or restart the game with the buttons on the screen.
#--------------------------------------------------------------------------------------------------------------

# Imports tkinter, multiprocessing, pygame, random, time, sys, and pygame.locals
import tkinter as tk
from multiprocessing import Process, Value
import pygame
import random
import time
import sys
from pygame.locals import *

# Initializes a global flag to determine if the game is paused.
game_paused = False

# A function in order to run the Tkinter timer application that creates the main tkinter window, while
#   initializing the 'TimerApp' with the tkinter window and the 'stop_flag' to stop the timer. Lastly,
#   the function runs the Tkinter timer application and tarts the main loop of the Tkinter timer application.
def run_tkinter(stop_flag):
    root = tk.Tk()
    app = TimerApp(root, stop_flag)
    root.mainloop()

# A function in order to run the Pygame police dodger game that creates the main pygame window, while
#   initailizes the pygame and its imported modules, and initalizes the pygame mixer module to be able
#   to play sound effects and music.
def run_pygame(stop_flag):
    pygame.init()
    pygame.mixer.init()

    # Initializes the variables and values for each colour.
    WHITE = (255, 255, 255)
    LIGHT_RED = (255, 0, 0)
    DARK_RED = (150, 0, 0)
    LIGHT_GREEN = (0, 255, 0)
    DARK_GREEN = (0, 150, 0)
    YELLOW = (255, 229, 10)
    LIGHT_YELLOW = (212, 255, 10)
    BLACK = (0, 0, 0)
    ROAD_COLOR = (47, 47, 47)

    # Intializes and loads images in order for pygame to be able to load it in png's.
    car_image = pygame.image.load("car.png")
    road_image = pygame.image.load("road1.jpg")
    tree_image1 = pygame.image.load("longbush3.png")
    tree_image2 = pygame.image.load("longbush4.png")
    police_image = pygame.image.load("police.png")
    icon_image = pygame.image.load("policeIcon.png")
    game_over_image = pygame.image.load('gameover.png')

    # Initializes the pygame window and sets its size and title while changing the icon of pygame application
    #   to a police car image.
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Police Dodger by Arvin Askari")
    pygame.display.set_icon(icon_image)

    # Declares global variables for lives and game over while initializing the lives to 2 and game over to false,
    #   indicating that the game is over.
    global lives, game_over
    lives = 2
    game_over = False

    # Initializes the variables for music, sound effects, and clock.
    crash_sound = pygame.mixer.Sound('shot.ogg')
    game_over_sound = pygame.mixer.Sound('gameover.ogg')
    clock = pygame.time.Clock()

    # Loads the background music for the game and runs it indefinitely until the game (loop) is over.
    pygame.mixer.music.load('gamemusic.mp3')
    pygame.mixer.music.play(-1)

    # The 'game_objects' class is used to create the game objects for the game and designed to manage them
    #   and their interactions. This class maintains methods to handle drawing the game objects, managing 
    #   the police cars, displaying the score, and displaying the lives.
    class game_objects:
        # This construction method is used ot initialize the 'game_objects' instance with the pygame display.
        #   surface, in which the game objects will be drawn.
        def __init__(self, display):
            self.display = display

        # Method that blits an image on the game screen at their specified x and y coordinates.
        def blit_image(self, image, x, y):
            self.display.blit(image, (x, y))

        # Method that reutns a random police car image and its dimensions. It then load and scales the
        #   police car images. The list of the opponent cars which are all the same in this case is then created.
        #   Also, a list of dimensions for the police cars is also created. This method hen selects a random police
        #   car from the list and then returns the police car and its dimensions.
        def opponent_cars(self):
            police_car = pygame.image.load("policecar4.png")
            police_car = pygame.transform.scale(police_car, (65, 104))
            opp_cars = [police_car, police_car, police_car]
            opp_car_hw = [(65, 104), (65, 104), (65, 104)]
            random_number = random.randrange(0, 3)
            current_car = opp_cars[random_number]
            current_w, current_h = opp_car_hw[random_number]
            return current_car, current_w, current_h

        # This method is used to generate random starting coordinates for the police cars. 
        def opponent_car_coordinates(self, road_r):
            ocar_startx = random.randrange(200, road_r - 64)
            ocar_starty = random.choice([-10, -20, -15, -12, -23])
            return ocar_startx, ocar_starty

        # This method is used ot display the current score on the game screen.
        def display_score(self, count):
            score_obj = pygame.font.SysFont("calibri", 30)
            score_surf = score_obj.render("Score:" + str(count), True, WHITE)
            self.display.blit(score_surf, (0, 0))

        # This method displays the game over image on the game screen when the game is over.
        def game_over(self):
            self.display.blit(game_over_image, (100, 200))
            pygame.display.update()
            time.sleep(2)

        # This method saves the current score of the game to a text file called 'highscore.txt'.
        def enter_current_score(self, c_score):
            with open("highscore.txt", 'a') as write:
                write.write('\n')
                write.write(str(c_score))

        # This method reads the high scores from the file, sorts them, and displays the highest score.
        def previous_score(self):
            with open("highscore.txt", 'r') as read:
                score = read.readlines()
            score = [int(x.strip()) for x in score]
            score.sort()
            self.show_previous_score(score[-1])

        # This method displays the previous high score on the game screen.
        def show_previous_score(self, pscore):
            dscore_obj = pygame.font.SysFont("calibri", 20)
            dscore_surf = dscore_obj.render("Previous High Score:" + str(pscore), True, WHITE)
            self.display.blit(dscore_surf, (0, 575))

        # This method displays the current lives left on the game screen.
        def display_life(self, life):
            life_obj = pygame.font.SysFont("calibri", 30)
            life_surf = life_obj.render("Lives Left:" + str(life), True, WHITE)
            self.display.blit(life_surf, (620, 0))

        # This method draws a circle that represents traffic lights, on the screen at the specified 
        #   coordinates with its given radius and colour.
        def lights(self, center_x, center_y, radius, color):
            pygame.draw.circle(self.display, color, (center_x, center_y), radius)

    # The 'display_message' function main intent is to display a message on the game screen. It starts by
    #   creating a font object with the specified font name and size. It then renders the text to be displayed
    #   on the game screen with the specified colour. It then gets the rect of the rendered text and centers it
    #   at the specified x and y coordinates. Finally, it blits the rendered text to the game screen.
    def display_message(text, size, x, y, color):
        font = pygame.font.SysFont("calibri", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)
        pygame.display.update()

    # The 'handle_crash' function is used to handle the event of a collision in the game. It starts by
    #   creating an instance of the 'game_objects' class. It then plays the crash sound effect and displays
    #   the explosion image on the game screen at the specified coordinates. It then calls the 'enter_current_score'
    #   method of the 'game_objects' class to save the current score of the game to a text file. It then calls the
    #   'decrement_lives' method of the 'game_objects' class to decrement the number of lives left by 1. Finally,
    #   it sleeps for 2 seconds and calls the'main_game' method of the 'game_objects' class.
    def handle_crash(opponent_x, opponent_y, score):
        score_handler = game_objects(screen)
        crash_sound.play()
        show_explosion(opponent_x, opponent_y)
        score_handler.enter_current_score(score)
        decrement_lives()
        time.sleep(2)
        if not game_over:
            main_game()

    # The 'show_explosion' function is used to display the explosion animation on the game screen by loading
    #   the explosion image and blitting it to the game screen at the specified coordinates and continues to
    #   update the display to show the changes being made. 
    def show_explosion(x, y):
        explosion_image = pygame.image.load('explosion.gif')
        screen.blit(explosion_image, (x, y))
        pygame.display.update()

    # 'The decrement_lives' function is used to decrement the number of lives and handle the game over scenario
    #   should the number of lives reach 0. It stats by declaring lives and game_over as global variables by 
    #   modifiying them. This then leads to the leaves decreasing by 1. It then checks if the number of lives has
    #   reaches -1, indicating the game is over. It then calls the 'game_over' method of the 'game_objects' and 
    #   displays the game over image on the game screen, while stopping the background muisc and plays the game 
    #   over sound effect and also stops the tkinter timer. Lastly, sets game_over to true to show the game has 
    #   ended and the restart screen is displayed allowng the user to choose their next action.
    def decrement_lives():
        global lives, game_over
        lives -= 1
        if lives == -1:
            game_over_instance = game_objects(screen)
            game_over_instance.game_over()
            pygame.mixer.music.stop()
            game_over_sound.play()
            stop_flag.value = 1  # Set the flag to stop the timer
            game_over = True
            show_restart_screen()

    # The 'show_restart_screen' function dislays the restart screen on the game screen and handles user 
    #   interactions. It starts by declaring game_over as a global variable by modifying it. The loop wil
    #   then continuue as long as the 'game_over' variable is true, waiting until the user makes a choice.
    #   If the user clicks the 'Restart' button, it calls the 'reset_game' method of the 'game_objects' class
    #   to reset the game. It then calls the 'enter_game' method of the 'game_objects' class to enter the game.
    #   It then calls the'main_game' method of the 'game_objects' class to start the game. If the user clicks
    #   the 'Quit' button, it calls the'stop_flag' method of the 'game_objects' class to signal the tkinter 
    #   process to stop. It then calls the 'pygame.quit' method to quit the game. It then calls the'sys.exit'
    #   method to ensure the program exits completely. Finally, it sets the 'game_over' variable to false to 
    #   indicate the game has not ended and the restart screen is no longer displayed.
    def show_restart_screen():
        global game_over
        while game_over:
            if create_button(250, 450, 20, DARK_GREEN, LIGHT_GREEN, "Restart"):
                reset_game()
                enter_game()
                main_game()
            if create_button(550, 450, 20, DARK_RED, LIGHT_RED, "Quit"):
                stop_flag.value = 1  # Signal the tkinter process to stop
                pygame.quit()
                sys.exit()  # Ensure the program exits completely
            pygame.display.update()
            clock.tick(15)

    # The 'pause_game' function pauses the game and displays a pause menu with two options to continue the game
    #   or quit the game. It starts by declaring game_paused as a global variable by modifying it. The loop
    #   will then continue as long as the 'game_paused' variable is true, waiting until the user makes a choice.
    #   If the user clicks the 'Continue' button, it sets the 'game_paused' variable to false to indicate the 
    #   game is no longer paused. It then calls the 'pygame.mixer.music.unpause' method to unpause the background
    #   music. If the user clicks the 'Quit' button, it calls the'stop_flag' method of the 'game_objects' class
    #   to signal the tkinter process to stop. It then calls the 'pygame.quit' method to quit the game. It then
    #   calls the'sys.exit' method to ensure the program exits completely. Finally, it sets the 'game_paused'
    #   variable to false to indicate the game is no longer paused.
    def pause_game():
        global game_paused
        pygame.mixer.music.pause()
        game_paused = True
        while game_paused:
            display_message("PAUSED", 100, 800 // 2, 600 // 2, WHITE)
            if create_button(250, 450, 20, DARK_GREEN, LIGHT_GREEN, "Continue"):
                game_paused = False
                pygame.mixer.music.unpause()
            if create_button(550, 450, 20, DARK_RED, LIGHT_RED, "Quit"):
                stop_flag.value = 1  # Signal the tkinter process to stop
                pygame.quit()
                sys.exit()  # Ensure the program exits completely
            pygame.display.update()
            clock.tick(30)

    # Creates an instance of the 'game_objects' class where it is initiaized with the game screen as an argument.
    game_instance = game_objects(screen)

    # The 'show_entry_screen' function displays the entry screen and handles user interactions. Starts off by
    #   declaring mouse_clicked as a global variable by modifiying it. Also, sets mouse_clicked to false, creates a
    #   flag to keep the entry screen active and makes the background of the screen white. When the entry screen
    #   is active, it will enter the loop and starts by iterating throuhg the events in the pygame event queue. If
    #   the user decides to quit the game, the program will exit. This then signals the tkinter process to stop, while
    #   ensuring the entire program exits completely. This function also displays the game title on the screen
    #   and an image of a police car.If the user clicks the 'Start' button, it will start the main game loop and
    #   will enter the game screen. If the user clicks the 'Instructions' button, it will display the instructions.
    #   Lastly, it will update the display to show the changes being made. Finally, it will set the 'entry_active' 
    #   variable to false to indicate the entry screen is no longer active.
    def show_entry_screen():
        global mouse_clicked
        mouse_clicked = False
        entry_active = True
        screen.fill(WHITE)
        while entry_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    stop_flag.value = 1  
                    pygame.quit()
                    sys.exit()  # 
                if event.type == MOUSEBUTTONDOWN:
                    mouse_clicked = True
            display_message("Police Dodger", 80, 420, 100, BLACK)
            game_instance.blit_image(police_image, 100, 60)
            button_action = create_button(250, 450, 20, DARK_GREEN, LIGHT_GREEN, "Start")
            if button_action == "start":
                enter_game()
                main_game()
            button_action = create_button(400, 450, 20, YELLOW, LIGHT_YELLOW, "Instructions")
            if button_action == "instructions":
                instructions_screen()
            button_action = create_button(550, 450, 20, DARK_RED, LIGHT_RED, "Quit")
            if button_action == "quit":
                stop_flag.value = 1  # Signal the tkinter process to stop
                pygame.quit()
                sys.exit()  # Ensure the program exits completely
            pygame.display.update()
            clock.tick(30)

    # The 'instructions_screen' function displays the instructions screen and handles user interactions. 
    #   It starts off by declaring mouse_clicked as a global variable by modifiying it. Also, sets mouse_clicked
    #    to false indicating no mouse has been clicked. Creates a flag to keep the instructions screen active and sets
    #   the screen to have a white background. When the instructions screen is active, it will enter the loop and
    #   will iterate through the events in the pygame event queue. If the user decides to quit the game, the 
    #   program will exit. This then signals the tkinter process to stop, while ensuring the entire program 
    #   exits completely. This function also displays the instructions title on the screen and displays a message
    #   on how the game works and what controls the user can use to play and control the game. It also creates
    #   a button that takes the user back to the home screen so they can start the game. It will continue to update
    #   pygame and control the frame rate of the loop to 30 frames per second. 
    def instructions_screen():
        global mouse_clicked
        mouse_clicked = False
        instructions = True
        screen.fill(WHITE)
        while instructions:
            for event in pygame.event.get():
                if event.type == QUIT:
                    stop_flag.value = 1  # Signal the tkinter process to stop
                    pygame.quit()
                    sys.exit()  # Ensure the program exits completely
                if event.type == MOUSEBUTTONDOWN:
                    mouse_clicked = True
            display_message("Instructions", 60, 400, 70, BLACK)
            display_message("Use arrow keys or WASD to move your car.", 30, 400, 150, BLACK)
            display_message("Tip: Using the top arrow or 'W' makes the car move faster.", 30, 400, 200, BLACK)
            display_message("Avoid police cars and stay on the road.", 30, 400, 250, BLACK)
            game_instance.blit_image(police_image, 100, 180)
            button_action = create_button(400, 520, 20, DARK_GREEN, LIGHT_GREEN, "Back To Home Screen")
            if button_action == "back":
                instructions = False
                show_entry_screen()
            pygame.display.update()
            clock.tick(30)

    # The 'create_button' function creates an interactive button on the screen in which the user can click and
    #   pick their desired option. This function takes center_x, center_y, radius, inactive_color, active_color, and
    #   message as parameters. The function will return the message of the button that the user has clicked.
    #   This function also takes in the mouse position and the mouse click position. If the mouse is within the
    #   bounding circle of the button, it will change the colour of the button to the active colour and display the
    #   message on the button. If the mouse is clicked on the button, it will return the message of the button.
    #   It will then update the display to show the changes being made by drawing the button with the inactive colour
    #   and then display it. Lastly, if no action is taken, it will return None.
    def create_button(center_x, center_y, radius, inactive_color, active_color, message):
        global mouse_x, mouse_y, click_x, click_y, mouse_clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click_x, click_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                click_x, click_y = event.pos
                mouse_clicked = True
            elif event.type == MOUSEBUTTONUP:
                click_x, click_y = event.pos
                mouse_clicked = True

        left_x = center_x - radius
        left_y = center_y - radius
        width_c = height_c = 2 * radius  

        button_hovered = left_x <= mouse_x <= (left_x + width_c) and left_y <= mouse_y <= (left_y + height_c)
        button_clicked = button_hovered and left_x <= click_x <= (left_x + width_c) and left_y <= click_y <= (left_y + height_c) and mouse_clicked

        if button_hovered:
            game_instance.lights(center_x, center_y, radius, active_color)
            display_message(message, 20, center_x, center_y + 50, BLACK)
            if button_clicked:
                mouse_clicked = False
                if message == "Start":
                    return "start"
                elif message == "Instructions":
                    return "instructions"
                elif message == "Quit":
                    return "quit"
                elif message == "Continue":
                    return "continue"
                elif message == "Back To Home Screen":
                    return "back"
                elif message == "Restart":
                    return "restart"
        else:
            game_instance.lights(center_x, center_y, radius, inactive_color)
            display_message(message, 20, center_x, center_y + 50, BLACK)
        return None

    # The 'enter_game' function initializes the game and displays the game entry screen starting with a countdown
    #   from 3 to 0. It will then display the road and trees on the screen. It will then display the countdown message
    #   on the screen. It will then update the display to show the changes being made by drawing the road and trees on
    #   the screen. It will constantly update to display and shwo the changes while also waiting a second before the
    #   next countdown message. This will then lead to the beginning of the game and the user can start controlling
    #   the car and play the game.
    def enter_game():
        screen.fill(ROAD_COLOR)
        road_x, road_y = 200, -580
        tree1_x, tree1_y = 0, 0
        tree2_x, tree2_y = 605, 0
        start_screen = game_objects(screen)
        countdown = 3
        while countdown >= 0:
            start_screen.blit_image(road_image, road_x, road_y)
            start_screen.blit_image(tree_image1, tree1_x, tree1_y)
            start_screen.blit_image(tree_image2, tree2_x, tree2_y)
            if countdown == 0:
                display_message("GO!", 150, 800 // 2, 600 // 2, WHITE)
            else:
                display_message(str(countdown), 150, 800 // 2, 600 // 2, WHITE)
            countdown -= 1
            pygame.display.update()
            time.sleep(1)  

    # The 'main_game' function is the core function of this program, that is responsible for the running of the
    #   the main game loop. 
    def main_game():
        # Declares global variables for game_over and lives and initializes game_over flag to False saying that
        #   the game is not over.
        global game_over, lives
        game_over = False

        # Creates instances of game_objects for the user's car, police car, and life_display.
        car_obj1 = game_objects(screen)
        car_obj2 = game_objects(screen)
        life_display = game_objects(screen)
        
        # Initializes variables for the user's car position and dimensions. 
        car_x, car_y = 800 * 0.4, 600 * 0.8
        car_width, car_height = 64, 104

        # Initializes the movement variables for the user's car, define the boundry of the read, and initalizes
        #   the speeds of the police car and the base speed of the game. 
        x_change, y_change = 0, 0
        road_right_end = 600
        opponent_speed1, opponent_speed2 = 7, 7
        base_speed = 5

        # Intializes the positions for the road and the trees/bushes on the screen in order to create the
        #   scrolling background effect. Also sets the initial movement speeds for the road and trees/bushes. Lastly,
        #   initializes the score and up_press_count variables.
        road_x, road_y = 200, -580
        tree1_x, tree1_y, tree2_x, tree2_y = 0, -580, 605, -580
        move_road_speed, move_tree1_speed, move_tree2_speed = base_speed, base_speed, base_speed
        score, up_press_count = 0, 1

        # Intializes the first police car and its position and dimensions.
        opponent_car1, opponent_car1_width, opponent_car1_height = car_obj1.opponent_cars()
        opponent_car1_x, opponent_car1_y = car_obj1.opponent_car_coordinates(road_right_end)
        
        # Initializes the second police car and its position and dimensions that will arrive later on in the game.
        opponent_car2, opponent_car2_width, opponent_car2_height = None, None, None
        opponent_car2_x, opponent_car2_y = None, None

        # Start of main game loop.
        while not game_over:
            # Fills the screen with the road colour and updates the positions for the road and trees to create
            #   the scolling effect as the car moves across the road.
            screen.fill(ROAD_COLOR)
            road_y += move_road_speed
            tree1_y += move_tree1_speed
            tree2_y += move_tree2_speed

            # Resets the positions if it moves off the screen.
            if road_y > 10:
                road_y = -580
            if tree1_y > 10:
                tree1_y, tree2_y = -580, -580

            # Blits the image of the road and tress on the screen at their specified positions.
            car_obj1.blit_image(road_image, road_x, road_y)
            car_obj1.blit_image(tree_image1, tree1_x, tree1_y)
            car_obj1.blit_image(tree_image2, tree2_x, tree2_y)

            # Pygame event handling loop that iterates through the events that occur.
            for event in pygame.event.get():
                # Checkst to see if the event type is pygame.QUIT. If it is, then the game is over.
                if event.type == pygame.QUIT or stop_flag.value == 1:
                    stop_flag.value = 1  
                    pygame.quit()
                    sys.exit()  

                # Checks to see if the event type is pygame.KEYUP. If the released key is escape or q, 
                #   then the game is over as it sets the stop_flag to 1. If the released key is p, it calls
                #   the 'pause_game' function ot pause the game.
                if event.type == KEYUP:
                    if event.key in [K_ESCAPE, K_q]:
                        stop_flag.value = 1  
                        pygame.quit()
                        sys.exit()  
                    elif event.key == K_p:
                        pause_game()

                # Checks to see if the event type is pygame.KEYDOWN. If the user presses left arrow or 'a', 
                #   then it makes the car move -6 to left. if the user presses right arrow or 'd', then the car
                #   will move 6 to the right. If the user presses 'w' or up arrow, then car will increase its
                #   speed and if the score is greater or equal to 10 then the speed for both the car and the police
                #   cars will increase at higher speeds. Lastly, if the user presses the down arrow or 's', then
                #   the car will move 5 down.
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        x_change = -6
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        x_change = 6
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        if up_press_count == 1:
                            car_y -= 15
                        up_press_count += 1
                        move_road_speed = move_tree1_speed = move_tree2_speed = 10
                        opponent_speed1 = 14
                        if score >= 10:
                            opponent_speed2 = 17
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        y_change = 5

                # Checks for any 'KEYUP' events related to the movement of the user's car. If the key is released 
                #   (not including 'W' or top arrow), then it resets the cars x and y change variables to 0. If 
                #   the user releases from the 'W' or up arrow then it resets the car, road, and police car back to their original speed.
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d, pygame.K_DOWN, pygame.K_s]:
                        x_change, y_change = 0, 0
                    elif event.key in [pygame.K_UP, pygame.K_w] and up_press_count > 1:
                        car_y += 15
                        up_press_count = 1
                        move_road_speed = move_tree1_speed = move_tree2_speed = base_speed
                        opponent_speed1 = 7
                        if score >= 10:
                            opponent_speed2 = 7

            # Updates the user's car x-position based on the x_change variable. It will then update the first
            #   police car's y-poisition based on its speed.
            car_x += x_change
            opponent_car1_y += opponent_speed1

            # Blits the user's car and the first police car on the screen.
            car_obj1.blit_image(car_image, car_x, car_y)
            car_obj1.blit_image(opponent_car1, opponent_car1_x, opponent_car1_y)

            # Checks to see if the score is greater than or equal to 10 and if the second police car has not been intiailized.
            if score >= 10 and opponent_car2 is None:
                opponent_car2, opponent_car2_width, opponent_car2_height = car_obj2.opponent_cars()
                opponent_car2_x, opponent_car2_y = car_obj2.opponent_car_coordinates(road_right_end)
        
            # Updates and manges the second police car if it is present and moves the second police car
            #   down the screen.
            if opponent_car2 is not None:
                opponent_car2_y += opponent_speed2
                
                # Resets the second police car's position and updates the speed and score if it moves off the screen,
                #   It will also keep on increasing the police car's speed for every additional score increment above 10. 
                if opponent_car2_y > 600:
                    opponent_car2, opponent_car2_width, opponent_car2_height = car_obj2.opponent_cars()
                    opponent_car2_x, opponent_car2_y = car_obj2.opponent_car_coordinates(road_right_end)
                    score += 1
                    increment = min(score - 10, 10)
                    opponent_speed1 += 0.005 + 0.2 * increment
                    opponent_speed2 += 0.006 + 0.2 * increment
                    move_road_speed += 0.004 + 0.2 * increment
                    move_tree1_speed += 0.004 + 0.2 * increment
                    move_tree2_speed += 0.004 + 0.2 * increment

                # Blits the second police car on the screen.
                car_obj2.blit_image(opponent_car2, opponent_car2_x, opponent_car2_y)

            # Displays the current score, previous high score, and number of lives left on the screen.
            car_obj1.display_score(score)
            car_obj1.previous_score()
            life_display.display_life(lives)

            # Checks for collisons with the game boundries and handles crashes if there are any between the car.
            if car_x < 200 or car_x > (800 - car_width - 200) or car_y + car_height > 600 or car_y < 0:
                handle_crash(car_x, car_y, score)

            # Checks to see if the first police car moves off the screen and if its does, it resets its positon.
            if opponent_car1_y > 600:
                opponent_car1, opponent_car1_width, opponent_car1_height = car_obj1.opponent_cars()
                opponent_car1_x, opponent_car1_y = car_obj1.opponent_car_coordinates(road_right_end)
                score += 1
                opponent_speed1 += 0.005
                move_road_speed += 0.004
                move_tree1_speed += 0.004
                move_tree2_speed += 0.004

            # Checks if the second police car moves off the screen and if its does, it resets its positon.
            if score > 10 and opponent_car2_y > 600:
                opponent_car2, opponent_car2_width, opponent_car2_height = car_obj2.opponent_cars()
                opponent_car2_x, opponent_car2_y = car_obj2.opponent_car_coordinates(road_right_end)
                opponent_speed2 += 0.006
                score += 1

            # Checks for any collisions between the user's car and the first police car. 
            if (car_y < opponent_car1_y + opponent_car1_height and car_y + car_height > opponent_car1_y and
                ((car_x > opponent_car1_x and car_x < opponent_car1_x + opponent_car1_width) or 
                 (car_x + car_width > opponent_car1_x and car_x + car_width < opponent_car1_x + opponent_car1_width))):
                handle_crash(car_x, car_y - 20, score)

            # Checks for any collisions between the user's car and the second police car.
            if score > 10 and opponent_car2 is not None:
                if (car_y < opponent_car2_y + opponent_car2_height and car_y + car_height > opponent_car2_y and
                    ((car_x > opponent_car2_x and car_x < opponent_car2_x + opponent_car2_width) or 
                     (car_x + car_width > opponent_car2_x and car_x + car_width < opponent_car2_x + opponent_car2_width))):
                    handle_crash(car_x, car_y - 20, score)

            # Checks if the stop flag is et to 1, and if it is, then it will exit the game
            if stop_flag.value == 1:
                pygame.quit()
                sys.exit()  

            # Updates the display of the game with the latest changes and controls the frame rate of the game
            #   loop to 40 frames per second.
            pygame.display.update()
            clock.tick(40)

    # The 'reset_game' function resets the game to the initial state. It starts by declaring lives and game_over
    #   as global variables in order to modify them. It then restes the number of lives to 2 and resets the game_over
    #   variable to False to establish a new game and say the game is not over, thus resulting in a new game.
    def reset_game():
        global lives, game_over
        lives = 2
        game_over = False

    # Displays the entry screen for the game and will quit Pygame if the entry screen is closed.
    show_entry_screen()
    pygame.quit()

# The 'TimerApp' class is used to create a Tkinter timer that will be used to time the game at the same time
#   as the pygame is running. The timer comes with a start, stop, reset, and exit buttons that allow the user
#   to interact in many ways while the game is running. 
class TimerApp:
    # The '__init__' method is used to initialize the Tkinter timer. It takes in the master, stop_flag, and self
    #    as attributes. it then initialzies the Tkinter window and stop flag. This initialize function sets the window
    #    title to "Tkinter Timer", sets the time left to 0, and sets the running variable to False. It also creates
    #    the start, stop, reset, and exit buttons and packs them into the Tkinter window.
    def __init__(self, master, stop_flag):
        self.master = master
        self.stop_flag = stop_flag
        self.master.title("Tkinter Timer")

        self.time_left = 0
        self.running = False

        self.label = tk.Label(master, text="00:00:00", font=("Calibri", 48))
        self.label.pack()

        self.start_button = tk.Button(master, text="Start Timer", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_button.pack()

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack()

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_program)
        self.exit_button.pack()

    # The 'start_timer' method starts the timer timer by setting the running variable to True and ensures
    #   that the time left is set to 0. It then calls the 'update_timer' method to update the timer.
    def start_timer(self):
        if not self.running:
            self.running = True
            self.update_timer()

    # The 'stop_timer' method stops the timer by setting the running variable to False.
    def stop_timer(self):
        self.running = False

    # The 'reset_timer' method resets the timer by stopping the timer and by setting the time left to 0.
    def reset_timer(self):
        self.stop_timer()
        self.time_left = 0
        self.label.config(text="00:00:00")

    # The 'exit_program' method quits the Tkinter timer by setting the stop flag to 1 and quits the Tkinter main loop.
    def exit_program(self):
        self.stop_flag.value = 1  
        self.master.quit()  

    # The 'update_timer' method updates the timer display every second if the timer is running and the stop flag
    #   is not set to 1. It will then calculate the hours, minutes, and seconds from the total time left and then 
    #   update the timer label with the formatted time. This method as an increment that will increment the time
    #   left by one second. If the stop flag is set to 1, then the timer is stopped.
    def update_timer(self):
        if self.running and self.stop_flag.value == 0:
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60
            self.label.config(text="{:02}:{:02}:{:02}".format(hours, minutes, seconds))
            self.time_left += 1
            self.master.after(1000, self.update_timer)
        elif self.stop_flag.value == 1:
            self.stop_timer()

# Ensures that the code inside it will run only when it is executed on its own and not when it is imported as 
#   a module. This will then create a shared value for the module and then create and start the Tkinter timer 
#   and its process. Lastly, it will run the pygame in the main process and ensure that the Tkinter process stops.
if __name__ == "__main__":
    stop_flag = Value('i', 0)
    tkinter_process = Process(target=run_tkinter, args=(stop_flag,))
    tkinter_process.start()
    try:
        run_pygame(stop_flag)
    finally:
        stop_flag.value = 1  
        tkinter_process.join()  