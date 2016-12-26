# endless-lake-player

[![Gameplay Video](/assets/gameplay_video_thumbnail.png)](https://youtu.be/w7zgnHlbEHc)

The `endless-lake-player` is a computer vision program that plays [Endless Lake](https://www.facebook.com/EndlessLakeGame), a mini-game recently added to Facebook Messenger. The main run loop takes a screenshot, identifies the positions of characters and jumps in the image, and triggers mouse clicks when a character is within a certain distance from a jump. The goal is to make something that would play as well as a human player but with a robotic endurance to achieve a high score.

Overall I'm happy with the end result. I think I would need to take a different, much more in-depth approach, to solve the game. This code would translate well to solving a simpler game such as Flappy Bird (fewer dynamically generated gameplay elements). In fact, I came across one of those implementations, [flappy-bird-player](https://github.com/troq/flappy-bird-player), which became my inspiration for the name of this program.

## Implementation

The main component is the [OpenCV](http://opencv.org/) library which provides a collection of image processing (computer vision) tools. In particular, it makes use of the [Match Template](http://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching/template_matching.html) function to track the location of characters and jumps on screen based on sample template images. These templates are cropped screenshots of those elements in various states of the game.

![Template Collage](/assets/template_collage.png)

## Setup

Here's the general setup steps:

1. Execute [`brew install opencv3 --HEAD`](http://www.pyimagesearch.com/2016/12/19/install-opencv-3-on-macos-with-homebrew-the-easy-way)
2. Execute `echo /usr/local/opt/opencv3/lib/python2.7/site-packages >> /usr/local/lib/python2.7/site-packages/opencv3.pth`
3. Execute `pip install numpy pyobjc`
4. Execute `python player.py`
5. Change `utility/config.py > screenshot_region` to contain the upper half of the game window

The result should be something that plays generally well but not particularly high scoring. On average, it achieves a score of around 200 (up to 600 on occasion). A human player can learn to play this well within a few minutes of practice.

## Limitations

The program's ability is limited by the complexity of Endless Lake. In particular, the game will generate unique path configurations which are difficult to account for. There are also additional decorative elements on screen that will break the template matching confidence. For example, a bird or a flag is often seen blocking a jump from view.

These situations can be solved for using the match template technique by adding more templates. The problem is each additional template slows down the performance of the program which needs to maintain a fairly high frame processing rate to time jumps correctly.

We can attempt to solve the performance bottlenecks by moving processing to the GPU. That would take a decent amount of effort to workaround GPU performance characteristics such as overcoming baseline costs. In addition, we would need to switch to the C++ version of OpenCV which provides more hooks to GPU computing.

Another approach would be to schedule actions in advance based on the character's constant movement speed. That would decouple us from the frame processing rate. I didn't end up going down this road because it would mean rewriting most of the program.
