from os import system, name
from logging import basicConfig, ERROR, getLogger
from time import sleep
from sys import stdin
from termios import tcflush, TCIFLUSH
from shutil import get_terminal_size
from sys import exit

basicConfig(level=ERROR)

try:
    from pynput import keyboard  # pyright: ignore[reportMissingModuleSource
    getLogger('pynput.keyboard.Listener').setLevel(ERROR)
except Exception:
    keyboard = None

class UI:
    def __init__(self, exit_func = exit):
        self.exit_func = exit_func
    def clear(self):
        system("cls" if name == 'nt' else 'clear')

    def exit_game(self):
        tcflush(stdin.fileno(), TCIFLUSH)
        self.exit_func(0)

    def wait(self, game):
        if game.wait_between_turns:    
            self.clear()

            if keyboard is None:
                return

            state = {'interrupted': False}

            def on_press(key):
                state['interrupted'] = True
                return False
            
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            for i in range(10):
                sleep(0.5)
                print(f'{10-i}...')
                if state['interrupted']:
                    tcflush(stdin.fileno(), TCIFLUSH)
                    listener.stop()
                    listener.join()
                    return False

    def show_title(self):        
        self.clear()

        width = get_terminal_size().columns
        margin = int((width-5)/2)
        print(' '*margin + "POKER" + ' '*margin + "_"*(width) + '\n')

    def enter(self): 
        input("Press ENTER: ")
        self.clear()
    
    def play_again(self, players):
        again = input("Do you want to play again? (y/n): ").strip().lower()
        while again != 'n' and again != 'y':
            again = input("Do you want to play again? (y/n): ").strip().lower()

        if again == 'n':
            winner = max(players, key = lambda player: player.money)
            print(f'{winner.id} wins!')
            self.exit_game()