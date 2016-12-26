import cv2
import numpy
import Quartz.CoreGraphics as CG

import utility.config

def screenshot():
    region = utility.config.screenshot_region

    rect = CG.CGRectMake(region["x"], region["y"], region["width"], region["height"])

    # Take screenshot
    cg_image = CG.CGWindowListCreateImage(rect, CG.kCGWindowListOptionOnScreenOnly, CG.kCGNullWindowID, CG.kCGWindowImageDefault)

    # Load data from image reference
    cg_image_data = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(cg_image))

    # Transform array into 3 dimensions [height, width, [Blue, Green, Red, Alpha]]
    screenshot = numpy.frombuffer(cg_image_data, dtype=numpy.uint8).reshape((CG.CGImageGetHeight(cg_image), CG.CGImageGetWidth(cg_image), 4))

    # Drop alpha channel
    screenshot = screenshot[:, :, :3]

    return screenshot

def downscale(image):
    return cv2.resize(image, None, fx=utility.config.image_scale, fy=utility.config.image_scale)

def flip_horizontal(image):
    return cv2.flip(image, 1)

def eliminate_region(image, region_rect):
    composite_image = image.copy()

    # Set pixels in region to black
    for y in range(region_rect["y1"], region_rect["y2"]):
        for x in range(region_rect["x1"], region_rect["x2"]):
            composite_image[y][x] = [0, 0, 0]  # Blue, Green, Red

    return composite_image

def highlight_regions(image, region_rects):
    # Darken image with mask
    composite_image = cv2.addWeighted(image, 0.50, numpy.zeros(image.shape, dtype="uint8"), 0.50, 0)

    # Highlight region_of_interest
    for rect in region_rects:
        (x1, x2, y1, y2) = (rect["x1"], rect["x2"], rect["y1"], rect["y2"])
        composite_image[y1:y2, x1:x2] = image[y1:y2, x1:x2]

    return composite_image

def save(path, image):
    cv2.imwrite(path, image)

def show(image):
    cv2.imshow("Monitor", image)
    cv2.waitKey(1)
