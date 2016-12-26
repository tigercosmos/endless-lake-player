import cv2
import glob

import utility.config
import utility.image

def template_id(template_path):
    return template_path.split("/")[-1]

def load_template_refs():
    template_refs = []

    # Character templates
    for template_path in glob.glob("templates/character/template-down-*.png"):
        template_refs.append({
            "id": template_id(template_path),
            "type": "character",
            "min_score": 0.75,
            "template": utility.image.downscale(cv2.imread(template_path))
        })

    for template_path in glob.glob("templates/character/template-side-*.png"):
        template = utility.image.downscale(cv2.imread(template_path))

        template_refs.append({
            "id": template_id(template_path),
            "type": "character",
            "min_score": 0.75,
            "template": template
        })

        template_refs.append({
            "id": template_id(template_path),
            "type": "character",
            "min_score": 0.75,
            "template": utility.image.flip_horizontal(template)
        })

    # Single jump template references
    for template_path in glob.glob("templates/jumps/single/template-down-*.png"):
        template_refs.append({
            "id": template_id(template_path),
            "type": "jump",
            "action": "single",
            "min_score": 0.8,
            "template": utility.image.downscale(cv2.imread(template_path))
        })

    for template_path in glob.glob("templates/jumps/single/template-side-*.png"):
        template = utility.image.downscale(cv2.imread(template_path))

        template_refs.append({
            "id": template_id(template_path),
            "type": "jump",
            "action": "single",
            "min_score": 0.8,
            "template": template
        })

        template_refs.append({
            "id": template_id(template_path),
            "type": "jump",
            "action": "single",
            "min_score": 0.8,
            "template": utility.image.flip_horizontal(template)
        })

    # Double jump template references
    for template_path in glob.glob("templates/jumps/double/template-down-*.png"):
        template_refs.append({
            "id": template_id(template_path),
            "type": "jump",
            "action": "double",
            "min_score": 0.8,
            "template": utility.image.downscale(cv2.imread(template_path))
        })

    for template_path in glob.glob("templates/jumps/double/template-side-*.png"):
        template = utility.image.downscale(cv2.imread(template_path))

        template_refs.append({
            "id": template_id(template_path),
            "type": "jump",
            "action": "double",
            "min_score": 0.8,
            "template": template
        })

        template_refs.append({
            "id": template_id(template_path),
            "type": "jump",
            "action": "double",
            "min_score": 0.8,
            "template": utility.image.flip_horizontal(template)
        })

    return template_refs

def load_template_game_over():
    return utility.image.downscale(cv2.imread("templates/game_over.png"))

def match_template(screenshot, template):
    # Perform match template calculation
    matches = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Survey results
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(matches)

    # Load template size
    (template_height, template_width) = template.shape[:2]

    return {
        "x1": max_loc[0],
        "y1": max_loc[1],
        "x2": max_loc[0] + template_width,
        "y2": max_loc[1] + template_height,
        "center": {
            "x": max_loc[0] + (template_width / 2),
            "y": max_loc[1] + (template_height / 2)
        },
        "score": max_val
    }

def multi_match_template(screenshot, template_ref):
    results = []

    # Find best matches
    composite_image = screenshot

    for i in range(utility.config.multi_match_max_matches):
        match = match_template(composite_image, template_ref["template"])

        if match["score"] < template_ref["min_score"]:
            # This and further matches will be too low in score
            break

        # Decorate match with template_ref properties
        for prop_name in ["id", "type", "action", "min_score"]:
            if template_ref.get(prop_name) is not None:
                match[prop_name] = template_ref[prop_name]

        # Save match
        results.append(match)

        # Eliminate approximate matched region
        matched_region = {
            "x1": match["x1"] + int((match["x2"] - match["x1"]) * utility.config.multi_match_max_overlap / 2),
            "x2": match["x2"] - int((match["x2"] - match["x1"]) * utility.config.multi_match_max_overlap / 2),
            "y1": match["y1"] + int((match["y2"] - match["y1"]) * utility.config.multi_match_max_overlap / 2),
            "y2": match["y2"] - int((match["y2"] - match["y1"]) * utility.config.multi_match_max_overlap / 2)
        }

        composite_image = utility.image.eliminate_region(composite_image, matched_region)

    return results
