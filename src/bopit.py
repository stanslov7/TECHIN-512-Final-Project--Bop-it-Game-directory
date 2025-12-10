import time
import random
# import math
# import board
# import busio
# import neopixel
# import adafruit_adxl34x

# Setup accelerometer (assuming CircuitPython or compatible environment)
# i2c = busio.I2C(board.SCL, board.SDA)
# accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Game and other Parameters

EMA_ALPHA = 0.2        # Smoothing factor for low-pass filtering
THRESHOLD = 1.5        # m/s^2 required to consider "real" movement
PERSISTENCE = 4        # Must detect movement in same direction N times
DIFFICULTY = 1         # Defaul difficulty

directions = ['up', 'down', 'left', 'right', 'forward', 'back']
# x: -left +right; y: +forward -back; z: +up -down; 
#g = 9.81  # m/s^2

#=== for emulated debubbing, replace with real analogue on board
# === replace prints with display to OLED
def print_oled(text, line):
    # line- OLED line to print to
    print(line, ":", text)


# === dummy neopixel emulator, replace with real color output to neo pixel
def neopixel(color):
    print("Color: " + color)

# === replace with getting reading from rotary switch to get difficulty
# Get difficulty
def getdiff():
    difficulty = int(input("Select difficulty (1: easy, 2: medium, 3: hard): "))
    return difficulty

# === replace with button press
def button_press():
    input("Press Enter to play again") 
    return


# === replace with accelerometer.acceleration
def get_acceleration():
    raw_x = float(input("Input X: "))
    raw_y = float(input("Input Y: "))
    raw_z = float(input("Input Z: "))
    return (raw_x, raw_y, raw_z)
# === end emulations




# Use "Improved Direction Detection" procedure from the assignment
def detect_movement(accel, level):
    x, y, z = accel
    devs = (x, y, z)  # raw detected values 
    abs_devs = tuple(abs(d) for d in devs)
    
    thresh = 2 + 0.5 * (level - 1)  # Progression: 2 to 6.5 m/s^2
    max_abs = max(abs_devs)
    if max_abs < thresh:
        return None
    
    sorted_abs = sorted(abs_devs, reverse=True)
    accuracy_ratio = 1.5 + 0.5 * (level - 1)  # Progression: 1.5 to 6
    if sorted_abs[0] < accuracy_ratio * sorted_abs[1]:
        return 'inaccurate'
    
    max_idx = abs_devs.index(max_abs)
    sign = 1 if devs[max_idx] > 0 else -1
    if max_idx == 0:  # x
        return 'right' if sign > 0 else 'left'
    elif max_idx == 1:  # y
        return 'forward' if sign > 0 else 'back'
    elif max_idx == 2:  # z
        return 'up' if sign > 0 else 'down'

# Main Game Loop
# Change print -> print_oled()
# Use Pixel -> neopixel()

# Main Game Loop
while True:
    # Select difficulty
    difficulty = DIFFICULTY # default

    # Replaced with difficulty selection from rotary switch
    # commenting out after debugging
    # diff_str = input("Select difficulty (1: easy, 2: medium, 3: hard): ")
    # difficulty = int(diff_str)
    difficulty =  getdiff()

    if difficulty == 1:
        lives = 5
    elif difficulty == 2:
        lives = 3
    else:
        lives = 1
    
    print_oled("Get ready...", 1)
    for i in range(3, 0, -1):
        print_oled(i, 1)
        if i == 1:
            neopixel("GREEN")
        elif i == 2:
            neopixel("YELLOW")
        else:
            neopixel("RED")
        time.sleep(1)
    print_oled("Play!", 3)
    neopixel("OFF")
    time.sleep(1)
    print_oled("CLEAR ALL", 1)

    game_over = False
    level = 1
    while level <= 10 and not game_over:
        time_per_move = 6 - (4 / 9) * (level - 1)  # Time to input move decreases with difficulty from 6s to 2s
        
        for move_num in range(10): # 10 moves per level
            if lives <= 0:
                game_over = True
                break
            
            dir = random.choice(directions)
            print_oled(f"D{difficulty} L{level} R{lives}: {dir.upper()}!", 1) # display Difficulty (D), Level (L), Rest (R) - lives left
            # later can print moves, lives, and level on different lines
            
            move_start = time.time()
            responded = False
            while not responded and time.time() - move_start < time_per_move:
                # accel = accelerometer.acceleration()
                accel = get_acceleration()
                detected = detect_movement(accel, level)
                if detected:
                    responded = True
                    if detected == dir:
                        print_oled("Correct!", 1)
                        neopixel("GREEN")
                    else:
                        # print_oled("Incorrect!" if detected != 'inaccurate' else "Not accurate enough!")
                        if detected == 'inaccurate':
                            print_oled("Incorrect!", 1)
                            neopixel("RED")
                        else:
                            print_oled("Not Accurate!", 1)
                            neopixel("YELLOW")
                        lives -= 1
                        if lives <= 0:
                            game_over = True
                            break
                time.sleep(0.01)
            
            if not responded and not game_over:
                print_oled("Too slow!", 1)
                neopixel("YELLOW")
                lives -= 1
                if lives <= 0:
                    game_over = True
        
        if not game_over:
            print_oled("Next Level!", 1)
            level += 1
    
    if level > 10:
        print_oled("You completed all levels!", 1)
    print_oled("Game Over", 1)
    print_oled("Play Again?", 1)
    # input("Press Enter to play again") # replace with button press
    button_press()
    