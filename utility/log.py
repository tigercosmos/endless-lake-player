import multiprocessing
import json
import time

import utility.image

def info(label):
    print "[" + str(trace_counter) + "] " + label

def performance(label, start):
    duration = time.time() - start

    duration_ms_str = str(round(duration * 1000))
    duration_fps_str = str(round(1 / duration))

    print "[" + str(trace_counter) + "] " + label + ": " + duration_ms_str + " ms (" + duration_fps_str + " fps)"

def trace_async(trace_counter, directory, screenshot_original, screenshot_highlighted, template_matches, possible_actions):
    utility.image.save(directory + "/screenshot_original_" + str(trace_counter) + ".png", screenshot_original)
    utility.image.save(directory + "/screenshot_highlighted_" + str(trace_counter) + ".png", screenshot_highlighted)

    with open(directory + "/template_trace_" + str(trace_counter) + ".json", "w") as trace_file:
        template_trace = {
            "template_matches": template_matches,
            "possible_actions": possible_actions
        }
        json.dump(template_trace, trace_file, sort_keys=True, indent=4)

def trace(directory, screenshot_original, screenshot_highlighted, template_matches, possible_actions):
    pool.apply_async(trace_async, (trace_counter, directory, screenshot_original, screenshot_highlighted, template_matches, possible_actions))

def separator():
    print "----"

    # Iterate trace counter
    global trace_counter
    trace_counter += 1

# Create single process pool for async writing
pool = multiprocessing.Pool(1)

# Relate logs together with iteration counter
trace_counter = 0
