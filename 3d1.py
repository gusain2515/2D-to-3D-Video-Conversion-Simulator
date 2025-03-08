import cv2
import numpy as np

def inspect_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return
    cv2.imshow("First Frame", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    height, width, channels = frame.shape
    print(f"Frame dimensions: {width}x{height}")
    if width == 2 * height:
        print("The video might be in side-by-side 3D format.")
    elif height == 2 * width:
        print("The video might be in top-bottom 3D format.")
    else:
        print("The video does not appear to be in a standard 3D format.")
    cap.release()

def compute_depth_map(frame, max_disparity=10, method='vertical'):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    if method == 'vertical':
        depth_map = np.linspace(0, max_disparity, height, dtype=np.uint8)
        depth_map = np.repeat(depth_map[:, np.newaxis], width, axis=1)
    elif method == 'gradient':
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        gradient_magnitude = cv2.magnitude(sobelx, sobely)
        depth_map = cv2.normalize(gradient_magnitude, None, 0, max_disparity, cv2.NORM_MINMAX)
        depth_map = depth_map.astype(np.uint8)
    else:
        depth_map = np.zeros((gray.shape), dtype=np.uint8)
    return depth_map

def generate_stereo_with_depth(frame, depth_map, method='vertical'):
    height, width, channels = frame.shape
    left_view = np.zeros_like(frame)
    right_view = np.zeros_like(frame)
    if method == 'vertical':
        for i in range(height):
            d = int(depth_map[i, 0])
            if d < width:
                left_view[i, d:] = frame[i, :width - d]
                right_view[i, :width - d] = frame[i, d:]
    else:
        for i in range(height):
            for j in range(width):
                d = int(depth_map[i, j])
                if j + d < width:
                    left_view[i, j + d] = frame[i, j]
                if j - d >= 0:
                    right_view[i, j - d] = frame[i, j]
    return left_view, right_view

def create_anaglyph(left_view, right_view):
    left_b, left_g, left_r = cv2.split(left_view)
    right_b, right_g, right_r = cv2.split(right_view)
    anaglyph = cv2.merge([right_b, right_g, left_r])
    return anaglyph

def process_video(input_path, output_path, max_disparity=10, method='vertical'):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open the input video.")
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        depth_map = compute_depth_map(frame, max_disparity, method)
        left_view, right_view = generate_stereo_with_depth(frame, depth_map, method)
        anaglyph_frame = create_anaglyph(left_view, right_view)
        out.write(anaglyph_frame)
        frame_count += 1
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Processed {frame_count} frames. Video saved to {output_path}")

def display_multiple_frames(input_path, max_disparity=10, method='vertical'):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open the video.")
        return
    ret, frame = cap.read()
    if not ret:
        print("Failed to read the video.")
        return
    depth_map = compute_depth_map(frame, max_disparity, method)
    left_view, right_view = generate_stereo_with_depth(frame, depth_map, method)
    anaglyph_frame = create_anaglyph(left_view, right_view)
    depth_map_color = cv2.applyColorMap(depth_map, cv2.COLORMAP_JET)
    top_row = cv2.hconcat([frame, left_view, right_view])
    bottom_row = cv2.hconcat([depth_map_color, anaglyph_frame, anaglyph_frame])
    final_output = cv2.vconcat([top_row, bottom_row])
    cv2.imshow("Multiple Frames", final_output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    video_path = r'C:\Users\Lenovo\OneDrive\Desktop\rkm\test.mp4'
    inspect_video(video_path)
    output_video_path = r'C:\Users\Lenovo\OneDrive\Desktop\rkm\output_anaglyph_video.avi'
    process_video(video_path, output_video_path, max_disparity=10, method='vertical')
    display_multiple_frames(video_path, max_disparity=10, method='vertical')
