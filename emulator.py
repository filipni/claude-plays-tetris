from PIL import Image
from pyboy import PyBoy
from pyboy.utils import WindowEvent


class Emulator:
    def __init__(self, rom_path):
        self.pyboy = PyBoy(rom_path)
        assert self.pyboy.cartridge_title == "TETRIS"
        self.tetris = self.pyboy.game_wrapper

    def tick(self, frames):
        for _ in range(frames):
            self.pyboy.tick()

    def initialize(self):
        self.pyboy.set_emulation_speed(0)

        self.tetris.start_game(timer_div=0x00)
        self.pyboy.tick()

        self.pyboy.set_emulation_speed(1)
        self.pyboy.send_input(WindowEvent.SCREEN_RECORDING_TOGGLE)

    def get_screenshot(self):
        return Image.fromarray(self.pyboy.screen.ndarray)

    def press_button(self, button):
        self.pyboy.button_press(button)
        self.tick(10)
        self.pyboy.button_release(button)
        self.tick(10)

    def stop(self):
        self.pyboy.send_input(WindowEvent.SCREEN_RECORDING_TOGGLE)
        self.pyboy.tick()
        self.pyboy.stop()