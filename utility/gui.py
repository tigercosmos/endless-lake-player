import Quartz.CoreGraphics as CG
import time

def post_left_mouse_event(type, x, y):
    CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(None, type, (x, y), CG.kCGMouseButtonLeft))

def mouse_position():
    return CG.CGEventGetLocation(CG.CGEventCreate(None))

def mouse_click():
    # Find current position
    (x, y) = mouse_position()

    # Move and click
    post_left_mouse_event(CG.kCGEventMouseMoved, x, y)
    post_left_mouse_event(CG.kCGEventLeftMouseDown, x, y)
    post_left_mouse_event(CG.kCGEventLeftMouseUp, x, y)

    # Avoid stacking clicks
    time.sleep(0.35)

def mouse_double_click():
    # Find current position
    (x, y) = mouse_position()

    # Move and click
    post_left_mouse_event(CG.kCGEventMouseMoved, x, y)
    post_left_mouse_event(CG.kCGEventLeftMouseDown, x, y)
    post_left_mouse_event(CG.kCGEventLeftMouseUp, x, y)

    time.sleep(0.1)

    post_left_mouse_event(CG.kCGEventLeftMouseDown, x, y)
    post_left_mouse_event(CG.kCGEventLeftMouseUp, x, y)

    # Avoid stacking clicks
    time.sleep(0.35)
