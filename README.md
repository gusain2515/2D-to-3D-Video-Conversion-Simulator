# 2D to 3D Video Conversion Simulator

This project is a Python-based simulator that converts a 2D video into a stereoscopic 3D video using synthetic depth estimation and anaglyph techniques. The output video can be viewed with red-cyan anaglyph glasses for a 3D effect.

## Overview

The project performs the following steps for each frame of an input 2D video:

1. **Depth Estimation:**  
   A synthetic depth map is generated using a basic method (either a simple vertical gradient or a gradient-based method with Sobel operators).

2. **Stereo View Generation:**  
   The depth map is used to offset pixels horizontally, creating left and right stereo views.

3. **Anaglyph Creation:**  
   The left and right views are combined into a single red-cyan anaglyph image.

4. **Video Processing:**  
   All processed frames are compiled into a new video file representing the 3D conversion.

A composite visualization is also provided, showing the original frame, the synthetic depth map, the left/right views, and the final anaglyph image.

## Features

- **Input/Output:**  
  Reads a 2D video (e.g., .mp4 or .avi) and outputs an anaglyph 3D video.

- **Synthetic Depth Estimation:**  
  Offers a basic vertical gradient method or a gradient-based method using Sobel operators.

- **Stereo View Generation:**  
  Shifts pixels horizontally based on the depth map to simulate left and right eye perspectives.

- **Anaglyph Video Creation:**  
  Combines left and right views into a red-cyan anaglyph image for 3D viewing.

- **Composite Visualization:**  
  Displays a composite image of the original frame, depth map, stereo views, and anaglyph for debugging and demonstration purposes.

- **Adjustable Depth Effect:**  
  The intensity of the depth effect can be controlled via the `max_disparity` parameter.


