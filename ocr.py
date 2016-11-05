#!/usr/bin/python
# -*- coding: <encoding name> -*-

from PIL import Image

PIXEL_COLOR_BACKGROUND = (8,8,31), 80, 160
PIXEL_COLOR_BORDER_BACKGROUND = (9,33,34), 14, 14
PIXEL_COLOR_TEXT_CS = (255,248,140), 55, 65
PIXEL_COLOR_TEXT_KDA = (204,204,204), 50, 70
PIXEL_COLOR_TEXT_TEAM_KILLS = (1, 150, 220), 28, 45
PIXEL_COLOR_TEXT_TEAM_DEATHS = (232, 6, 6), 25, 55
PIXEL_COLOR_ICON = (171, 171, 144), 45, 50

# 1 = 1 match needed
# 2 = 2 matches needed
# 3+ = minimum difference needed between prev pixel
PIXEL_COLOR_SKIP_BOTTOM = [
    ((111,92,45), 9, 2),
    ((96,89,60), 5, 2),
    ((34,42,33), 5, 40),
    ((152,152,152), 5, 1),
    ((87,82,56), 5, 1),
    ((75,77,60), 5, 2),
    ((92,86,69), 7, 1),
]
PIXEL_COLOR_SKIP_TOP = [
    ((204,204,204), 50, 2),
    ((99,99,99), 5, 50),
]

PIXEL_COLOR_TEXT_TEAM_KILLS_BOUNDS = PIXEL_COLOR_TEXT_TEAM_KILLS[0], 7, 7
PIXEL_COLOR_TEXT_TEAM_KILLS_NEARBY = (1, 150, 220), 80, 120

def pixel_match_fuzzy(template, input, forgiving=False):
    values = template[0]
    max_variance = template[2 if forgiving else 1]
    for index, value in enumerate(values):
        if abs(input[index] - value) > max_variance:
            return False
    return True

def pixel_diff(a, b):
    return sum([ b[i]-a[i] for i in range(3) ])

def pixel_diff_abs(a, b):
    return sum([ abs(b[i]-a[i]) for i in range(3) ])

def validate_pixels_y(screenshot, bounding_box, color, min_fill=0.82):
    min_y, max_x, max_y, min_x = bounding_box
    height = max_y - min_y

    y = min_y
    matches = 0
    while y <= max_y:
        x = min_x
        matched = False
        while x <= max_x:
            if pixel_match_fuzzy(color, screenshot.pixel(x,y)):
                matches += 1
                break
            x += 1
        y += 1

    return matches >= int(min_fill*height)

# Returns top, right, bottom, left - or None
def stats_box_find(screenshot):
    half_width = int(screenshot.width/2)
    two_third_width = int(screenshot.width*2/3)
    x = screenshot.width-3
    y = 1

    minY, maxX, maxY, minX = 0, screenshot.width, None, None

    # First find the bottom
    last_pixel = screenshot.pixel(x, 0)
    while y < 200:
        pixel = screenshot.pixel(x, y)
        diff = pixel_diff(pixel, last_pixel)

        if diff < -30:
            maxY = y
            break

        y += 1

    if maxY is None:
        return None

    # Then find the left area
    y = int((maxY - minY) / 2)
    match_color = None
    matched_kills = False
    matched_deaths = False
    while x > two_third_width:
        if not matched_kills:
            matched_kills = pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_KILLS_BOUNDS, screenshot.pixel(x,y)) or \
                            pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_KILLS_BOUNDS, screenshot.pixel(x,y+5)) or \
                            pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_KILLS_BOUNDS, screenshot.pixel(x,y-5))
            if matched_kills and matched_deaths:
                match_color = PIXEL_COLOR_TEXT_TEAM_KILLS_BOUNDS
                break

        if not matched_deaths:
            matched_deaths = pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_DEATHS, screenshot.pixel(x,y)) or \
                            pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_DEATHS, screenshot.pixel(x,y+5)) or \
                            pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_DEATHS, screenshot.pixel(x,y-5))
            if matched_kills and matched_deaths:
                match_color = PIXEL_COLOR_TEXT_TEAM_DEATHS
                break

        x -= 1

    if not match_color:
        return None
        
    # Then find the left border
    misses = 0
    while x > half_width:
        y = minY
        matched = False
        while y < maxY:
            matched = pixel_match_fuzzy(match_color, screenshot.pixel(x,y), forgiving=True)
            if matched:
                misses = 0
                break
            y += 1

        if not matched:
            misses += 1
            if misses > 9:
                minX = x + misses
                break

        x -= 1
        if not x > half_width:
            return None

    # If the team kills is surrounded by a similar 
    # color that makes it hard to read, bail out
    if match_color == PIXEL_COLOR_TEXT_TEAM_KILLS_BOUNDS:
        height = maxY-minY
        half_y = int(minY+height/2)
        third_y = int(minY+height/3)
        if pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_KILLS_NEARBY, screenshot.pixel(minX-2, half_y)) or \
            pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_KILLS_NEARBY, screenshot.pixel(minX-2, third_y)) or \
            pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_KILLS_NEARBY, screenshot.pixel(minX-2, third_y*2)) or \
            pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_KILLS_NEARBY, screenshot.pixel(minX+5, maxY+1)):
            return None

    # Now scan the bottom + top
    # If we find any open tooltip or shop window border color,
    # don't even try reading this
    x = minX-8
    y_top = minY+4
    y_bottom = maxY-4
    xMidLeft = int(minX + (maxX-minX) * 0.3)


    pixel_bottom_last = None
    pixel_top_last = None
    while x < xMidLeft:
        pixel_bottom = screenshot.pixel(x,y_bottom)
        pixel_top = screenshot.pixel(x,y_top)

        for index, color in enumerate(PIXEL_COLOR_SKIP_BOTTOM):
            if pixel_match_fuzzy(color, pixel_bottom):
                match_type_switch = color[2]
                if match_type_switch == 1:
                    #print("   - fuckb 1 {}".format(index))
                    return None
                elif pixel_bottom_last and pixel_diff_abs(pixel_bottom, pixel_bottom_last) >= match_type_switch:
                    #print("   - fuckb 2 {}".format(index))
                    return None

        total_bottom = len(PIXEL_COLOR_SKIP_BOTTOM)
        for index, color in enumerate(PIXEL_COLOR_SKIP_TOP):
            if pixel_match_fuzzy(color, pixel_top):
                match_type_switch = color[2]
                if match_type_switch == 1:
                    #print("   - fuckt 1 {}".format(index))
                    return None
                elif pixel_top_last and pixel_diff_abs(pixel_bottom, pixel_top_last) >= match_type_switch:
                    #print("   - fuckt 2 {}".format(index))
                    return None

        pixel_bottom_last = pixel_bottom
        pixel_top_last = pixel_top

        x += 1
    
    while x < maxX:
        matched = pixel_match_fuzzy(PIXEL_COLOR_BACKGROUND, screenshot.pixel(x,y))
        if not matched:
            return None
        x += 1
        
    return minY, maxX, maxY, minX

# trims a stats box by looking for kills and using that as the bounding height
def stats_box_trim(screenshot, bounding_box):
    min_y, max_x, max_y, min_x = bounding_box

    new_min_y = None
    new_max_y = None

    # Go through vertically and find the deaths
    found_ever = False
    x = min_x
    while x <= max_x:
        found_this_iteration = False

        y = min_y
        while y <= max_y:
            matched = pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_DEATHS, screenshot.pixel(x,y), forgiving=True)
            if matched:
                if new_min_y is None or y < new_min_y:
                    new_min_y = y
                if new_max_y is None or y > new_max_y:
                    new_max_y = y

                if not found_ever:
                    found_ever = True
                if not found_this_iteration:
                    found_this_iteration = True

            y += 1

        # If we found it before and never found it this time, we've passed it, return
        if found_ever and not found_this_iteration:
            return new_min_y, max_x, new_max_y, min_x

        x += 1

    return None

def get_numbers(screenshot, bounding_box, x_bounds, pixel_color):

    box_width = bounding_box[1] - bounding_box[3]
    y_min = bounding_box[0]
    y_max = bounding_box[2]
    x_min, x_max = x_bounds

    out_debug(screenshot, (y_min, x_max, y_max, x_min), 'chunk')

    found = False
    found_last_iteration = False
    x = x_min
    x_start = None
    text_to_number_list = []
    while x <= x_max+1:
        y = y_min
        while y <= y_max:
            found = pixel_match_fuzzy(pixel_color, screenshot.pixel(x, y))
            if found:
                break
            y += 1

        if found and x <= x_max:
            if not found_last_iteration:
                x_start = x
        else:
            if found_last_iteration:
                #print("DO OCR")
                text_to_number = get_number_ocr(screenshot, (y_min, x-1, y_max, x_start), pixel_color)
                text_to_number_list.extend(text_to_number)
                #print(" -- {}".format(text_to_number))

        found_last_iteration = found
        x += 1

    #return text_to_number_list
    return int("".join([str(num) for num in text_to_number_list]))

def get_number_ocr(screenshot, bounding_box, pixel_color):
    y_min, x_max, y_max, x_min = bounding_box
    height = float(y_max - y_min)+1
    width = float(x_max - x_min)+1

    #print("OCR {} {} {}".format(width, height, height/width))

    # merged character 3x check
    if height/width < .55:
        chunk_width = int(width/3.45)
        chunk_separator = int((width - chunk_width*3) / 2)
        return get_number_ocr(screenshot, (y_min, x_min+chunk_width, y_max, x_min), pixel_color) + \
                get_number_ocr(screenshot, (y_min, x_min+chunk_width*2+chunk_separator, y_max, x_min+chunk_width+chunk_separator), pixel_color) + \
                get_number_ocr(screenshot, (y_min, x_max, y_max, x_max-chunk_width), pixel_color)

    # merged character 2x check
    if height/width < 1:
        half_width = int(width/2.3)
        return get_number_ocr(screenshot, (y_min, x_min+half_width, y_max, x_min), pixel_color) + \
                get_number_ocr(screenshot, (y_min, x_max, y_max, x_max-half_width), pixel_color)

    #out_debug(screenshot, (y_min, x_max, y_max, x_min), 'piece', force=True)

    # Trim the top and bottom
    found_trim_point = False
    y = y_min
    while y <= y_max and not found_trim_point:
        x = x_min
        while x <= x_max and not found_trim_point:
            if pixel_match_fuzzy(pixel_color, screenshot.pixel(x, y)):
                found_trim_point = True
                y_min = y
            x += 1   
        y += 1 

    found_trim_point = False
    y = y_max
    while y >= y_min and not found_trim_point:
        x = x_min
        while x <= x_max and not found_trim_point:
            if pixel_match_fuzzy(pixel_color, screenshot.pixel(x, y)):
                found_trim_point = True
                y_max = y
            x += 1   
        y -= 1 

    height = float(y_max - y_min)+1

    out_debug(screenshot, (y_min, x_max, y_max, x_min), 'piece-trimmed')

    # =====> 1 <=====
    if height/width > 2.1:
        return [1]

    mid_center_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.5)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.6)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.45)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.38)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.6), y_min+int(height*0.6)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.62)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.7)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.30), y_min+int(height*0.5)), forgiving=True)
 
    # =====> 0 <=====
    if not mid_center_match:
        return [0]

    bottom_left_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_max))
    bottom_right_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_max))
    bottom_left_match = bottom_left_match_strict or pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_max), forgiving=True) \
                                                 or pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_max-int(height*0.1)), forgiving=True)
    bottom_right_match = bottom_right_match_strict or pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max-1, y_max), forgiving=True)

    bottom_mid_center_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.7)))
    mid_left_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min+int(height*0.5)), forgiving=True)

    #print(" stat {}-{} {}-{} {}".format(bottom_left_match_strict, bottom_left_match, bottom_right_match_strict, bottom_right_match, bottom_mid_center_match))


    top_left_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min)) or \
                            pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.1), y_min+int(height*0.1)))
    top_right_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_min))
    top_left_match = top_left_match_strict or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.05), y_min+int(height*0.05)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.15), y_min), forgiving=True)
    top_right_match = top_right_match_strict or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_min), forgiving=True)
    top_mid_left_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min+int(height*0.25)), forgiving=True)  or \
                            pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.2), y_min+int(height*0.25)), forgiving=True)
    #print(" stat2 {} {}".format(top_left_match, top_right_match))

    top_mid_center_right_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.75), y_min+int(height*0.25)), forgiving=True)

    # =====> 4 <=====
    if not bottom_left_match and not top_left_match and top_mid_center_right_match and not top_mid_left_match:
        return [4]

    #print(" stat4 {} {} {} {}".format(bottom_left_match, top_left_match, bottom_right_match, top_right_match))
    bottom_mid_right_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_min+int(height*0.75))) or \
                             pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max-int(width*0.2), y_min+int(height*0.75))) or \
                             pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max-int(width*0.1), y_min+int(height*0.8)))

    # =====> 2 <=====
    if not bottom_mid_right_match and bottom_right_match:
        return [2]

    # =====> 7 <=====
    if not bottom_mid_right_match and not top_mid_left_match and top_left_match_strict:
        return [7]

    #print(" stat7 {} {} {} {} {}".format(bottom_left_match, top_left_match, bottom_right_match, top_right_match, top_mid_left_match))


    top_mid_left_center_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.15), y_min+int(height*0.4)))

    # =====> 3 <=====
    if not top_mid_left_match and not top_mid_left_center_match:
        return [3]

    top_mid_right_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_min+int(height*0.25)), forgiving=True)

    bottom_mid_left_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+1, y_min+int(height*0.75)-1)) or \
                            pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min+int(height*0.8)-1))

    #print(" stat3 {} {} {} {}".format(mid_center_match, top_mid_left_match, bottom_mid_left_match, top_mid_left_center_match))

    # =====> 6 <=====
    if not top_mid_right_match:
        if bottom_mid_left_match:
            return [6]
        else:
            return [5]

    # =====> 8 <=====
    if bottom_mid_left_match:
         return [8]

    # =====> 9 <=====
    return [9]

def find_block_x(screenshot, bounding_box, minX, color=PIXEL_COLOR_ICON, fails_possible=0, forgiving=True):
    minY, maxX, maxY, _minX = bounding_box
    matchMinX = None
    matchMaxX = None

    found = False
    found_ever = False
    x = minX
    while x < maxX:
        matched = False
        y = minY
        while y < maxY:
            pixel = screenshot.pixel(x, y)
            match = pixel_match_fuzzy(color, pixel, forgiving=forgiving)

            if match:
                matched = True
                break

            y += 1

        if matched:
            fails_left = fails_possible
            found = True

            if not found_ever:
                found_ever = True
                matchMinX = x
        else:
            if found:
                if fails_left == fails_possible:
                    matchMaxX = x-1

                fails_left -= 1
                if fails_left <= 0:
                    return matchMinX, matchMaxX

        x += 1

    return None


ignored_pixels = {}
def set_ignored_pixel(x,y):
    _y = ignored_pixels.get(x)
    if _y is None:
        _y = {}
        ignored_pixels[x] = _y
    _y[y] = True

def is_ignored_pixel(x,y):
    _y = ignored_pixels.get(x)
    if _y is None:
        return False

    return _y.get(x, False)

def remove_object_pixels(screenshot, x, y, color):
    startX = x
    startY = y
    bounds = [y,x,y,x]
    matches = {}

    def check_pixel(x,y):
        _x = matches.get(x)
        if not _x is None:
            if not _x.get(y) is None:
                return
        else:
            _x = {}
            matches[x] = _x

        match = pixel_match_fuzzy(color, screenshot.pixel(x,y), forgiving=False)

        _x[y] = match

        if match:
            if y < bounds[0]:
                bounds[0] = y
            if x > bounds[1]:
                bounds[1] = x
            if y > bounds[2]:
                bounds[2] = y
            if x < bounds[3]:
                bounds[3] = x

            # check top
            check_pixel(x-1,y-1)
            check_pixel(x,y-1)
            check_pixel(x+1,y-1)

            # check mid
            check_pixel(x-1,y)
            check_pixel(x+1,y)

            # check bot
            check_pixel(x-1,y+1)
            check_pixel(x,y+1)
            check_pixel(x+1,y+1)

    check_pixel(x,y)

    return bounds

def find_splitter_x(screenshot, bounding_box, minX, color=PIXEL_COLOR_TEXT_KDA, min_x_matches=5):
    minY, maxX, maxY, _minX = bounding_box
    match_min_x = None
    match_max_x = None
    half_height = int((maxY-minY)/2)
    half_y_point = minY + half_height

    x = minX

    # Detect single bars
    x_matches = 0
    while x < maxX:
        y_touches = 0
        y_matches = 0
        y_match_highest = 0
        y = maxY
        last_match = False

        while y >= minY:
            pixel = screenshot.pixel(x, y)
            match = pixel_match_fuzzy(color, pixel)

            if match:
                y_matches += 1
                if not last_match:
                    y_touches += 1

                if y > y_match_highest:
                    y_match_highest = y

            y -= 1

            last_match = match

        # If we found a match, and it's not a 1 or a 7
        if y_touches == 1 and y_matches < half_height:
            x_matches += 1
            if x_matches >= min_x_matches:
                _minY, _maxX, _maxY, _minX = remove_object_pixels(screenshot, x, y_match_highest, color)
                return _minX, _maxX
        else:
            x_matches = 0

        #print("splitter: {} {}".format(y_touches, x_matches))

        x += 1

    return None

dump_pics = False
current_numbers = {}
def out_debug(screenshot, bounding_box, name='out', force=False):
    if not dump_pics and not force:
        return
    current_number = current_numbers.get(name, 0)
    crop_box = (bounding_box[3], bounding_box[0], bounding_box[1]+1, bounding_box[2]+1)
    screenshot_box = screenshot.image.crop(crop_box)
    screenshot_box.save('output/{}{}.bmp'.format(name, current_number))
    current_numbers[name] = current_number+1

def get_stats(screenshot, debug=False):

    bounding_box = stats_box_find(screenshot)
    
    if not bounding_box:
        return None
    if debug:
        print(("Found Box: {}".format(bounding_box)))
        out_debug(screenshot, bounding_box, force=True)

    bounding_box = stats_box_trim(screenshot, bounding_box)
    if not bounding_box:
        return None
    if debug:
        print(("Trim Box: {}".format(bounding_box)))
        out_debug(screenshot, bounding_box, force=True)

    # Find minion kills
    minY, maxX, maxY, minX = bounding_box

    team_kills_x = find_block_x(screenshot, bounding_box, minX, color=PIXEL_COLOR_TEXT_TEAM_KILLS, fails_possible=10)
    team_deaths_x = find_block_x(screenshot, bounding_box, minX, color=PIXEL_COLOR_TEXT_TEAM_DEATHS, fails_possible=10)
    kda_bounds_x = find_block_x(screenshot, bounding_box, team_kills_x[0], color=PIXEL_COLOR_TEXT_KDA, fails_possible=10)
    minion_icon_bounds = find_block_x(screenshot, bounding_box, kda_bounds_x[1]+5, color=PIXEL_COLOR_ICON, fails_possible=3)
    minion_kills_bounds_x = find_block_x(screenshot, bounding_box, minion_icon_bounds[1]+1, color=PIXEL_COLOR_TEXT_CS, fails_possible=10)

    kills_deaths_splitter_bounds_x = find_splitter_x(screenshot, bounding_box, kda_bounds_x[0])
    deaths_assists_splitter_bounds_x = find_splitter_x(screenshot, bounding_box, kills_deaths_splitter_bounds_x[1])

    kills_bounds_x = [kda_bounds_x[0], kills_deaths_splitter_bounds_x[0]-2]
    deaths_bounds_x = [kills_deaths_splitter_bounds_x[1]+2, deaths_assists_splitter_bounds_x[0]-2]
    assists_bounds_x = [deaths_assists_splitter_bounds_x[1]+2, kda_bounds_x[1]]

    if not validate_pixels_y(screenshot, [minY, team_kills_x[1], maxY, team_kills_x[0]], color=PIXEL_COLOR_TEXT_TEAM_KILLS):
        return None

    if debug:
        print("kda {}-{}".format(*kda_bounds_x))
        print("k {}-{}".format(*kills_bounds_x))
        print("s {}-{}".format(*kills_deaths_splitter_bounds_x))
        print("d {}-{}".format(*deaths_bounds_x))
        print("s {}-{}".format(*deaths_assists_splitter_bounds_x))
        print("a {}-{}".format(*assists_bounds_x))

        out_debug(screenshot, [minY, team_kills_x[1], maxY, team_kills_x[0]], force=True)
        out_debug(screenshot, [minY, team_deaths_x[1], maxY, team_deaths_x[0]], force=True)
        out_debug(screenshot, [minY, kda_bounds_x[1], maxY, kda_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, kills_bounds_x[1], maxY, kills_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, kills_deaths_splitter_bounds_x[1], maxY, kills_deaths_splitter_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, deaths_bounds_x[1], maxY, deaths_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, deaths_assists_splitter_bounds_x[1], maxY, deaths_assists_splitter_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, assists_bounds_x[1], maxY, assists_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, minion_icon_bounds[1], maxY, minion_icon_bounds[0]], force=True)
        out_debug(screenshot, [minY, minion_kills_bounds_x[1], maxY, minion_kills_bounds_x[0]], force=True)


    return {
        'team_kills': get_numbers(screenshot, bounding_box, team_kills_x, PIXEL_COLOR_TEXT_TEAM_KILLS),
        'team_deaths': get_numbers(screenshot, bounding_box, team_deaths_x, PIXEL_COLOR_TEXT_TEAM_DEATHS),
        'kills': get_numbers(screenshot, bounding_box, kills_bounds_x, PIXEL_COLOR_TEXT_KDA),
        'deaths': get_numbers(screenshot, bounding_box, deaths_bounds_x, PIXEL_COLOR_TEXT_KDA),
        'assists': get_numbers(screenshot, bounding_box, assists_bounds_x, PIXEL_COLOR_TEXT_KDA),
        'CS': get_numbers(screenshot, bounding_box, minion_kills_bounds_x, PIXEL_COLOR_TEXT_CS),
    }