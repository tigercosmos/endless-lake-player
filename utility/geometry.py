import math

import utility.config

def distance(lhs, rhs):
    (x1, y1) = (lhs["x"], lhs["y"])
    (x2, y2) = (rhs["x"], rhs["y"])

    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

def rects_intersect(lhs, rhs):
    return (lhs["x1"] < rhs["x2"] and rhs["x1"] < lhs["x2"]) and (lhs["y1"] < rhs["y2"] and rhs["y1"] < lhs["y2"])

def rects_overlap(lhs, rhs):
    return distance(lhs["center"], rhs["center"]) < utility.config.conflict_overlap_distance

def calculate_actions(matches):
    # Separate matches by type
    character_matches = [m for m in matches if m["type"] == "character"]
    jump_matches = [m for m in matches if m["type"] == "jump"]

    # Determine possible actions
    possible_actions = []

    for c_match in character_matches:
        for j_match in jump_matches:
            (x1, y1) = (c_match["center"]["x"], c_match["center"]["y"])
            (x2, y2) = (j_match["center"]["x"], j_match["center"]["y"])

            if y1 >= y2:
                # Eliminate because character passed jump
                continue

            # Calculate distance
            result = {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "distance": distance(c_match["center"], j_match["center"]),
                "action": j_match["action"]
            }

            # Save result
            possible_actions.append(result)

    # Sort possible actions
    def sort_fn(lhs, rhs):
        if lhs["action"] == "double" and rhs["action"] == "single":
            # Prioritize double over single jumps
            return -1

        if lhs["action"] == "single" and rhs["action"] == "double":
            # Prioritize double over single jumps
            return 1

        # Sort by lowest distance first for same action
        if lhs["distance"] < rhs["distance"]:
            return -1
        else:
            return 1

    possible_actions.sort(sort_fn)

    return possible_actions
