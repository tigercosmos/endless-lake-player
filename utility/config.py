# Screenshot parameters
screenshot_region = {
    "x": 170,
    "y": 180,
    "width": 440,
    "height": 360
}

# Scale image down before processing
image_scale = 0.15

# Adjust vertical center for character type towards bottom
character_vertical_center = 0.75

# Action distances for jumps
single_jump_action_distance = 82.5 * image_scale
double_jump_action_distance = 125 * image_scale

# Multi match template parameters
multi_match_max_overlap = 0.25  # Max 25% overlap
multi_match_max_matches = 5  # Max 5 matches with same template

# Distance between match centers to be considered a conflict
conflict_overlap_distance = 30 * image_scale
