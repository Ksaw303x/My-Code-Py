import time
import threading
import pyautogui


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                pyautogui.keyDown(self.button)
                print('press')
                time.sleep(0.2)
                pyautogui.keyUp(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)


if __name__ == '__main__':

    click_thread = ClickMouse(0.3, 'space')
    click_thread.start()

    time.sleep(3)
    click_thread.start_clicking()

    start_stop_key = 's'
    exit_key = 'e'


    def on_press(key):
        if key == start_stop_key:
            if click_thread.running:
                click_thread.stop_clicking()
            else:
                click_thread.start_clicking()
        elif key == exit_key:
            click_thread.exit()
            # listener.stop()
