#! /usr/bin/ipython3

import numpy as np
import random
from time import sleep
import graphics

from gpiozero import DistanceSensor

from pythonosc import osc_message_builder
from pythonosc import udp_client

# Define main method
def main_game():
    (win, circ, message, sensor) = initialize()
    keep_playing = play_query(win)
    while keep_playing:
        balloon_game(win, circ, message, sensor)
        set_defaults(win, circ, message)
        keep_playing = play_query(win)
    end_cleanup(win, circ, message, sensor)
    
# Initializes graphics display
def initialize():
    # Graphics defaults
    WIN_DIMEN_X = 700
    WIN_DIMEN_Y = 440
    CIRC_DIAM = 20

    (win, circ, message, sensor) = createobjects(WIN_DIMEN_X, WIN_DIMEN_Y, CIRC_DIAM)
    set_defaults(win, circ, message)
    return win, circ, message, sensor

# Creates graphics objects
def createobjects(WIN_DIMEN_X, WIN_DIMEN_Y, CIRC_DIAM):
    win = graphics.GraphWin("game", WIN_DIMEN_X, WIN_DIMEN_Y)
    win.setCoords(0, 0, WIN_DIMEN_X, WIN_DIMEN_Y)
    ctr_pt = graphics.Point(WIN_DIMEN_X / 2, WIN_DIMEN_Y / 2)
    circ = graphics.Circle(ctr_pt, CIRC_DIAM)
    circ.setFill("black")
    circ.setOutline("orange")
    circ.setWidth(3)
    message = graphics.Text(graphics.Point(WIN_DIMEN_X / 2, 0.219 * WIN_DIMEN_X), "")
    message.draw(win)
    sensor = DistanceSensor(echo = 17, trigger = 4)
    circ.draw(win)
    return win, circ, message, sensor


# Randomizes circle diameter, border color, and inner color
def set_defaults(win, circ, message):
    message.setText("DO yU plAy? now\nYes  No")            
    winheight = win.getHeight()
    endctr = circ.getCenter()
    dy = (winheight / 2) - endctr.y
    circ.move(0, dy)

    randwidth = random.randint(1,20)

    colors = np.array(["red", "black", "orange", "yellow", "purple", "tan", "pink", "violet", "teal", "turquoise",
                       "brown","grey", "blue", "light blue", "darkblue", "green", "light green", "dark green", "white", "olive"])

    circ.setFill(np.random.choice(colors))
    circ.setOutline(np.random.choice(colors))
    circ.setWidth(randwidth)
    win.setBackground("black")
    message.setTextColor(np.random.choice(colors))

# Reads whether the user selected yes or no
def play_query(win):
    keep_playing = False
    click_pt = win.getMouse()
    # Yes
    if((click_pt.x <= WIN_DIMEN_X / 2) and (click_pt.y <= WIN_DIMEN_Y/2)):
        keep_playing = True
    return keep_playing
    
# What to do if the user selects "No"
def end_cleanup(win, circ, message, sensor):
    sensor.close()
    del sensor
    circ.undraw()
    del circ
    win.close()
    del win
    del message


# Defines motion of the circle and what to do when the circle touches the top or bottom of the screen
def balloon_game(win, circ, message, sensor):
    radius = circ.getRadius()
    repetitions = 10000
    gravity = 100
    win_top = win.getHeight()
    vi = 0.
    t = 0.01
    dx = 0
    a = -1.0*gravity
    for i in range(repetitions):

        distance_change = gethandmotion(sensor)
        print(distance_change)

        message.setText("Score: %s" % (i / 100.))
 
        # Circle velocity
        vf = vi + a * t
        dy = (vf * t)# / 0.00043333 this is m/pixel
        vi = vf + (distance_change * 500)
        
        circ.move(dx, dy + distance_change)

        # Touching top and bottom borders
        ctr = circ.getCenter()
        
        # At window bottom
        if(ctr.y - radius <= 0):
            message.setText("You Lose!\nScore: %s" % (i / 100))
            sleep(3)
            return
        # At window top
        elif(ctr.y + radius >= win_top):
            message.setText("You Lose!\nScore: %s" % (i / 100))
            sleep(3)
            return
        if(i == repetitions):
            message.setText("You Win!\nScore: %s" % (i / 100))
            sleep(3)
            return

# Used by main method to read the motion in front of the ultrasonic sensor
def gethandmotion(sensor):
    i = True
    while i == True:
        sensor_distance1 = sensor.distance
        sleep(0.01)
        sensor_distance2 = sensor.distance
        distance_change = sensor_distance2 - sensor_distance1
        if(distance_change > 0.01):
            return distance_change
        else:
            return 0.0

# Call main function
main_game()


