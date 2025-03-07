#import math
import os
from math import sin, cos, radians
from time import sleep

# blok deklaracji "stałych"
GRAVITY = 9.81
DISTANCE = 40
RADIUS = 0.3
ROWS = 24
COLS = 80

# funkcje
def calculate_impact(velocity, angle):
    return velocity**2 * sin(2 * radians(angle)) / GRAVITY

def get_input():
    velocity = float(input("Podaj prędkość "))
    angle = None
    while not angle or not 0 <= angle <= 90:
        angle = float(input("Podaj kąt "))
    return velocity, angle

def shoot(position, velocity, angle):
    impact_pos = calculate_impact(velocity, angle)
    print(impact_pos)
    return abs(impact_pos - position) < RADIUS

def draw_scene(x, y):
    for _ in range(y-1): # od 0 do y-2
        print()
    for _ in range(x-1):
        print(" ", end="")
    print("o")
    for _ in range(y+1, ROWS-1):
        print()
    for _ in range(COLS):
        print("_", end="")

def draw_scene_adjusted(x,y):
    aspect_ratio = COLS/ROWS
    new_x = x * aspect_ratio
    # new_y = (ROWS * 2 - y * aspect_ratio) / 2
    new_y = ROWS - (y * aspect_ratio / 2)
    draw_scene(int(new_x),int(new_y))
    # draw_scene(round(new_x),round(new_y))

def animated_shot(velocity, angle):
    t_max = 2 * velocity * sin(radians(angle)) / GRAVITY
    t = 0
    dt = 0.05
    v_x = cos(radians(angle)) * velocity
    v_y = sin(radians(angle)) * velocity
    while t < t_max:
        x = v_x * t
        y = v_y * t - (GRAVITY * t**2) / 2
        draw_scene_adjusted(x,y)
        t+= dt
        sleep(dt)
        clear()

def clear():
    os.system("clear")

def main():
    turn = 1
    while True:
        print(f"Gracz {turn}")
        velocity, angle = get_input()
        animated_shot(velocity, angle)
        if turn == 1:
            shot = shoot(DISTANCE,velocity, angle)
        else:
            shot = shoot(0, velocity, angle - 180)
        if shot:
            print(f"Gracz {turn} wygrał")
            return
        turn = 3 - turn



if __name__ == '__main__':
    main()
    #draw_scene_adjusted(10,10)