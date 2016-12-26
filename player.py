import functools
import itertools
import json
import multiprocessing
import os
import shutil
import sys
import time

import cv2
import numpy

import utility.config
import utility.cv
import utility.geometry
import utility.gui
import utility.image
import utility.log

# Explicitly disable OpenCL. Querying for OpenCL support breaks when multiprocessing.
cv2.ocl.setUseOpenCL(False)

# Create multiprocessing pool. Uses `multiprocessing.cpu_count()` processes by default.
pool = multiprocessing.Pool()

# Load all templates
template_refs = utility.cv.load_template_refs()
template_game_over = utility.cv.load_template_game_over()

# Setup empty trace directory
trace_directory = "trace"

if os.path.exists(trace_directory):
    shutil.rmtree(trace_directory)

os.mkdir(trace_directory)

# Wait for game to start
while True:
    screenshot = utility.image.downscale(utility.image.screenshot())

    if utility.cv.match_template(screenshot, template_game_over)["score"] < 0.5:
        # Game over screen cleared
        utility.log.separator()
        break

    utility.log.info("Waiting for game to start...")
    time.sleep(1)

# Begin player run loop
while True:
    start = time.time()

    # Grab screenshot
    screenshot_original = utility.image.screenshot()
    screenshot = utility.image.downscale(screenshot_original)
    utility.log.performance("screenshot", start)

    # Calculate character and jump matches
    #
    # See http://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool
    matches = []

    map_fn = functools.partial(utility.cv.multi_match_template, screenshot)
    map_args = template_refs
    map_results = pool.map_async(map_fn, map_args).get(1)

    utility.log.performance("multi_match_template", start)

    for (idx, match_template_multiple_results) in enumerate(map_results):
        for result in match_template_multiple_results:
            # Adjust vertical center for character type towards bottom
            if result["type"] == "character":
                result["center"] = {
                    "x": result["center"]["x"],
                    "y": result["y1"] + ((result["y2"] - result["y1"]) * utility.config.character_vertical_center)
                }

            # Filter any conflicts from existing matches
            conflicting_matches = []

            def keep(match):
                if match["type"] != result["type"]:
                    # Not conflicting by type
                    return True

                if match["type"] == "jump" and match["action"] != result["action"]:
                    # Not conflicting by jump action
                    return True

                if not utility.geometry.rects_overlap(match, result):
                    # Not conflicting by overlap
                    return True

                # Conflicts with result
                return False

            matches = [m for m in matches if keep(m)]

            # Determine best match to keep
            best_match = result

            for match in conflicting_matches:
                if match["score"] > best_match["score"]:
                    # Conflicting match has higher score
                    best_match = match
                    continue

            # Save best match
            matches.append(best_match)

    utility.log.performance("matches", start)

    # Determine action
    possible_actions = utility.geometry.calculate_actions(matches)
    utility.log.performance("calculate_actions", start)

    for action in possible_actions:
        if action["action"] == "double" and action["distance"] <= utility.config.double_jump_action_distance:
            # Double jump
            utility.log.info("double click")
            utility.gui.mouse_double_click()
            break
        elif action["action"] == "single" and action["distance"] <= utility.config.single_jump_action_distance:
            # Single jump
            utility.log.info("single click")
            utility.gui.mouse_click()
            break
        else:
            # Try next action
            continue

    utility.log.performance("execute action", start)

    # Highlight results
    composite_image = utility.image.highlight_regions(screenshot, matches)
    utility.log.performance("highlight_regions", start)

    # Present composite image
    # utility.image.show(composite_image)
    # utility.log.performance("show", start)

    # Log trace
    utility.log.trace(trace_directory, screenshot_original, composite_image, matches, possible_actions)
    utility.log.performance("trace", start)

    # Match game over
    game_over = (len(matches) == 0 and utility.cv.match_template(screenshot, template_game_over)["score"] > 0.5)

    # Log total
    utility.log.performance("total", start)
    utility.log.separator()

    # Check exit condition
    if game_over:
        # Game ended
        break
