import os
import math
import time as tm
import pyautogui as control
from datetime import datetime
from PIL import ImageGrab as Grabber


def getPrintableTime(Days, Hours, Minutes, Seconds):
    toReturn = ''
    if Days != 0:
        toReturn = '%d Days, ' % Days
    if Hours != 0:
        toReturn += '%d Hours, ' % Hours
    if Minutes != 0:
        toReturn += '%d Minutes' % Minutes
    if Seconds != 0 and Minutes != 0:
        toReturn += ', %d Seconds ' % Seconds
    elif Minutes == 0:
        toReturn += ' %d Seconds' % Seconds
    return toReturn


def time_left(timeOut):
    try:
        return _extracted_from_time_left(timeOut)
    except:
        return ''


def floor(foo):
    return math.floor(foo)


def _extracted_from_time_left(timeout):
    current_time, seconds_in_day = datetime.now(), 24 * 60 * 60
    difference = timeout - current_time
    remaining = divmod(difference.days * seconds_in_day + difference.seconds, 60)
    seconds, minutes, hours, days = int(remaining[1]), int(remaining[0] % 60), int(remaining[0] / 60) % 24, int(
        remaining[0] / (60 * 24))
    return getPrintableTime(days, hours, minutes,
                            seconds + 1) + 'remaining of the holiday\nCurrent time: ' + current_time.strftime(
        "%H:%M:%S")


def sleep(timeout, t):
    t = int(t)
    for i in range(t):
        if (t - i) % 1 == 0:
            os.system('clear')
            time = t - i
            days = int(time / (24 * 3600))
            time %= (24 * 3600)
            hour = int(time / 3600) + (24 * days)
            time %= 3600
            minutes = int(time / 60)
            time %= 60
            seconds = time
            print(str(time_left(timeout)))
            print('Sleeping for' + getPrintableTime(0, hour, minutes, seconds))
        tm.sleep(1)


class youtube_tv:

    def set_positions(self):
        xvalue = 1000
        for i in range(1080, 2519, 200):
            self.positions.append([xvalue, i])

    def getColors(self):
        os.system('clear')
        print('Getting colors')
        return [control.pixel(i[0], i[1]) for i in self.positions]

    def isRunning(self):
        print('Simulating space press')
        self.simulate_space()
        sleep(self.timeOut, 60 * 60)

    def simulate_space(self):
        control.press('space')
        sleep(self.timeOut, 0.1)
        control.press('space')
        control.scroll(10)

    def isPaused(self, prev_colors):
        print('Video is paused')
        control.press('space')
        sleep(self.timeOut, 5)
        current_colors = self.getColors()
        if self.check_if_colors_match(prev_colors, current_colors):
            self.simulate_space()
        else:
            control.press('space')

    def check_if_colors_match(self, prev_colors, current_colors):
        return any(
            prev_colors[i] != current_colors[i] for i in range(len(prev_colors))
        )  # Returns true if they do not match

    def __init__(self, timeout):
        self.positions = []
        self.timeOut = timeout
        self.set_positions()

    def restart_show(self):
        os.system('clear')
        print('Disconnecting from VPN')
        os.system("expressvpn disconnect")
        print('Connecting to VPN')
        os.system("expressvpn connect \"USA - New Jersey - 3\"")
        print('Connected to VPN')
        print('Reloading show')
        control.hotkey('ctrl', 'r')
        sleep(self.timeOut, 10)
        control.move(3397, 1194)
        control.click()
        sleep(self.timeOut, 1)
        control.move(1770, 1770)
        control.click()
        sleep(self.timeOut, 1)
        control.click()

    def run(self):
        sleep(self.timeOut, 10)
        prev_colors, paused_run = self.getColors(), 0
        while True:
            os.system('clear')
            print('sleeping')
            sleep(self.timeOut, 3)
            current_colors = self.getColors()
            if self.check_if_colors_match(prev_colors, current_colors):
                paused_run = 0
                self.isRunning()
            else:
                paused_run += 1
                if paused_run == 5:
                    self.restart_show()
                    paused_run = 0
                self.isPaused(prev_colors)

            prev_colors = current_colors


def get_printable_time(total_seconds):
    seconds_in_day, seconds_in_hour, seconds_in_minute = 60 * 60 * 24, 60 * 60, 60
    days = floor(total_seconds / seconds_in_day)
    hours = floor((total_seconds - (days * seconds_in_day)) / seconds_in_hour)
    minutes = floor((total_seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) / seconds_in_minute)
    remaining_seconds = total_seconds - (
            (days * seconds_in_day) + (hours * seconds_in_hour) + (minutes * seconds_in_minute))
    if days < 0 or hours < 0 or minutes < 0 or remaining_seconds < 0:
        return None
    formatted_time_remaining = ''
    if days != 0:
        formatted_time_remaining += f'{days} day'
        if days != 1:
            formatted_time_remaining += 's'
    if hours != 0:
        if days != 0:
            formatted_time_remaining += ', '
        formatted_time_remaining += f'{hours} hour'
        if hours != 1:
            formatted_time_remaining += 's'
    if minutes != 0:
        if hours != 0 or days != 0:
            formatted_time_remaining += ', '
        formatted_time_remaining += f'{minutes} minute'
        if minutes != 1:
            formatted_time_remaining += 's'
    if remaining_seconds != 0:
        if minutes != 0 or hours != 0 or days != 0:
            formatted_time_remaining += ', and '
        formatted_time_remaining += f'{remaining_seconds} second'
        if remaining_seconds != 1:
            formatted_time_remaining += 's'

    return formatted_time_remaining


####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################
####################################################################################################################################################################################

class netflix:

    def __init__(self, timeout):
        self.timeOut, self.current_colors = timeout, []
        self.arrow_position, self.pause_text_position = [[965, 1811], [965, 1791], [977, 1801]], [3090, 2354]
        self.arrow_colors, self.paused_text_colors = [255, 255, 255], [204, 204, 204]
        self.position_for_autoplay_precheck = (self.arrow_position[0][0], self.arrow_position[0][1])
        self.position_for_paused_precheck = (self.pause_text_position[0], self.pause_text_position[1])
        self.line_breaker = '-' * 67

    def start_process(self):
        self.sleep(15, extra='Starting Process')
        while True:
            if self.check_if_autoplay_failed():
                self.sleep(2, extra='Passed first autoplay test')
                if self.check_if_autoplay_failed():
                    self.sleep(2, extra='Passed second autoplay test')
                    control.moveTo(self.arrow_position[0][0], self.arrow_position[0][1])
                    control.click()
            self.sleep(8, extra='Waiting for pause text to appear')
            if self.check_if_paused():
                self.sleep(2, extra='Passed first pause test')
                if self.check_if_paused():
                    os.system('clear')
                    self.sleep(2, extra='Passed second pause test')
                    tm.sleep(1)
                    control.press('space')
            else:
                self.sleep(2, extra='No issue detected')
                self.sleep(5 * 60)

    def sleep(self, seconds, extra=''):
        for i in range(seconds):
            os.system('clear')
            if extra != '':
                print(f'{self.line_breaker}\n|{extra}|')
            print(self.line_breaker)
            if seconds - i >= 5:
                print(f'Sleeping for {get_printable_time(seconds - i)}')
            print(f'Current time:\t{datetime.now().strftime("%H:%M:%S")}')
            delta_seconds = math.ceil((self.timeOut - datetime.now()).total_seconds())
            if delta_seconds < 0:
                print('The holiday is out')
            else:
                print(f'{get_printable_time(delta_seconds)} of the holiday remaining')
            print(self.line_breaker)
            tm.sleep(1)

    def check_color_match(self, colors_to_check):
        for current_color in self.current_colors:
            for i in range(len(current_color)):
                if current_color[i] != colors_to_check[i]:
                    return False
        return True

    def check_if_autoplay_failed(self):
        first_pixel_data = Grabber.grab().getpixel(self.position_for_autoplay_precheck)
        self.sleep(2, extra='Waiting to take a second screenshot')
        second_pixel_data = Grabber.grab().getpixel(self.position_for_autoplay_precheck)
        if not any(first_pixel_data[i] == second_pixel_data[i] for i in range(3)):
            return
        control.moveTo(self.position_for_autoplay_precheck)
        self.sleep(1, extra='Retrieving colors')
        image = Grabber.grab()
        self.current_colors = [image.getpixel((pos[0], pos[1])) for pos in self.arrow_position]
        return self.check_color_match(self.arrow_colors)

    def check_if_paused(self):
        self.sleep(1, extra='Checking if the video is paused')
        image = Grabber.grab()
        self.current_colors = [image.getpixel(self.position_for_paused_precheck)]
        return self.check_color_match(self.paused_text_colors)
