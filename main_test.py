answers = [[0,0,0,0,0,0],
    [0,0,0,0,0,0],
    None, #[0,0,0,0,0,0],
    [0,0,0,0,0,0],
    None, #[0,0,0,0,0,0],
    None, #[0,0,0,0,0,0],
    [0,0,0,0,0,6],
    [0,0,0,0,0,25],
    None, #[0,0,0,0,0,29],
    [1,0,1,0,0,38],
    [3,0,2,0,0,43],
    [3,1,2,0,0,73],
    None,
    [5,3,4,1,0,95],
    None, #[5,3,4,1,0,95],
    None, #[5,3,4,1,0,95],
    None, #[5,3,4,1,0,95],
    None, #[5,3,4,1,0,95],
    None, #[5,3,4,1,0,95],
    [8,3,5,1,2,97],
    [13,5,10,1,2,106],
    [14,6,11,1,2,112],
    [17,8,14,1,2,126],
    [19,8,16,1,2,139],
    [20,8,17,1,2,143],
    [22,8,19,1,2,148],
    [22,8,19,1,2,157],
    [22,9,19,1,2,169],
    [26,10,23,1,2,186],
    [27,11,24,1,2,200],
    [32,11,25,1,2,221],
    [34,11,26,1,3,226],
    None,
    None,
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,2,0,1,0,26],
    [1,4,0,2,0,50],
    [2,5,0,2,0,62],
    [2,5,0,2,0,62],
    [4,12,1,3,0,81],
    [5,14,2,3,0,89],
    [11,15,5,4,2,105],
    [12,19,5,4,3,118],
    [15,24,8,5,3,135],
    [18,28,11,5,3,168],
    None,
    None,
    [27,36,17,6,4,270],
    [27,36,17,6,4,271],
    [32,40,19,6,5,291],
    [32,41,19,7,5,320],
    [33,43,19,7,5,320],
    [34,45,20,7,5,362],
    [40,46,24,7,6,387],
    [22,14,17,6,1,141],
    None,
    [13,7,8,4,1,120],
    None,
    [2,1,0,0,0,47],
    None,
    [13,7,8,4,1,122],
    [13,7,8,4,1,123],
    [22,14,17,6,1,141],
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    [10,4,7,0,0,133],
    None, #[11,5,8,0,0,170],
    [15,7,12,0,0,224],
    [15,7,12,0,0,224],
    None, #[16,8,13,0,0,228],
    None, #[15,10,12,2,0,93],
    None, #[15,10,12,2,0,93],
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None, #[7,5,6,1,0,62],
    None,
    None,
    None, #[7,5,6,1,0,62],
    [15,11,12,2,2,137],
    [35,17,24,2,3,280],
    None,
    None,
    [25,24,4,7,16,43],
    [35,26,5,7,23,48],
    None, #[25,24,4,7,16,43],
    [35,26,5,7,23,48],
    None, #[13,4,5,2,1,173],
    [16,4,7,2,1,186],
    [17,4,8,2,1,202],
    None, #[13,4,5,2,1,173],
    [17,4,8,2,1,202],
    [16,4,7,2,1,186],
    [30,17,17,2,1,174],
    None, #[5,0,3,0,0,32],
    None, #[5,0,3,0,0,32],
    [27,13,16,1,1,167],
    [29,17,17,2,1,174],
    [30,17,17,2,1,174],
    None,
    None,
    [27,13,16,1,1,167],
    [29,17,17,2,1,174],
    None,
    [8,14,7,1,0,190],
    None,
    None,
    None,
    [15,6,6,0,0,213],
    None,
    [11,12,5,2,1,148],
    None,
    [36,22,20,4,4,326],
    [42,25,26,5,4,381],
    None,
    None,
    None,
    None, #[35,58,14,12,3,436],
    None,
    [0,0,0,0,0,3],
    [2,3,0,0,0,13],
]

import os
from time import sleep, time

from PIL import Image
from capture import Screenshot
import ocr
from ocr import get_stats

def main_test():

    # Testing
    for index, answer in list(enumerate(answers, start=1))[:]:
        screenshot = Screenshot(Image.open('test-newerui\\Screen{0:02}.bmp'.format(index)))
        results = get_stats(screenshot)
        if results:
            results = [results['team_kills'], results['team_deaths'], results['kills'], results['deaths'], results['assists'], results['CS'], ]

        correct = results is None and answer is None or results and answer and not [i for i in range(6) if not answer[i] == results[i]]
        wrong = [] if results is None or answer is None else [(results[i], answer[i]) for i in range(6) if not answer[i] == results[i]]

        if not correct and results:
            print (" -- WRONG {} - {} - {}".format(index, results, u", ".join(["({} instead of {})".format(a,b) for a,b in wrong])))
        elif not correct:
            print ("{} OK-ISH - Got None instead of numbers".format(index))
        else:
            print ("{} OK ({})".format(index, results))

    # X_BOUNDS_TEAM_KILLS = (0.0 / STATS_BOX_WIDTH, 42.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_TEAM_DEATHS = (59.0 / STATS_BOX_WIDTH, 101.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_CS = (299.0 / STATS_BOX_WIDTH, 339.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_KILLS = (127.0 / STATS_BOX_WIDTH, 167.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_DEATHS = (188.0 / STATS_BOX_WIDTH, 228.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_ASSISTS = (243.0 / STATS_BOX_WIDTH, 283.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_TIME = (349.0 / STATS_BOX_WIDTH, 420.0 / STATS_BOX_WIDTH)

def main_screenshot():
    window = _get_windows_bytitle('League of Legends')[0]
    win32gui.SetForegroundWindow(window)
    sleep(0.01)
    screenshot_save(window, "-test-1")
    exit()

def main_test_1(number):
    ocr.dump_pics = True
    screenshot = Screenshot(Image.open('test-newerui\\Screen{0:02}.bmp'.format(number)))
    print (get_stats(screenshot, debug=True))

main_test()
#main_test_1(122)