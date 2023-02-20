import time
import os
import random
from pyfiglet import Figlet

def display_art():
    custom_fig = Figlet()
    art = custom_fig.renderText('Avito Web Scraping Tool')

    for i in range(1):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        art = custom_fig.renderText('Infomineo')

        print('\033[0;34m')  # set the text color to blue
        shake_amount = random.randint(1, 5)  # determine how much to shake the art
        for line in art.split('\n'):
            print(
                ' ' * shake_amount + line)  # print each line of the art, with a random amount of space added to the left to create a shaking effect
        time.sleep(0.5)  # pause for a short amount of time to create a flashing effect

        art = custom_fig.renderText('Avito Web Scraping Tool')

        print('\033[0;31m')  # set the text color to red
        shake_amount = random.randint(1, 5)  # determine how much to shake the art
        for line in art.split('\n'):
            print(
                ' ' * shake_amount + line)  # print each line of the art, with a random amount of space added to the left to create a shaking effect
        time.sleep(0.5)  # pause for a short amount of time to create a flashing effect

        art = custom_fig.renderText('2023')

        print('\033[0;34m')  # set the text color to blue
        shake_amount = random.randint(1, 5)  # determine how much to shake the art
        for line in art.split('\n'):
            print(' ' * shake_amount + line)  # print each line of the art, with a random amount of space added to the left to create a shaking effect



display_art()
