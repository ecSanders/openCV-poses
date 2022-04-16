import pyrealsense2 as rs
import numpy as np
import open3d as o3d
import math as m


def get_image():
    # Define some constants
    resolution_width = 1280  # pixels
    resolution_height = 720  # pixels
    frame_rate = 15  # fps

    # Create a pipeline
    pipeline = rs.pipeline()

    # Enable depth, infrared, color streams
    config = rs.config()
    config.enable_stream(rs.stream.depth)  # , resolution_width, resolution_height, rs.format.z16, frame_rate)
    config.enable_stream(rs.stream.infrared)  # , 1, resolution_width, resolution_height, rs.format.y8, frame_rate)
    config.enable_stream(rs.stream.color)  # , resolution_width, resolution_height, rs.format.bgr8, frame_rate)

    pc = rs.pointcloud()
    pipeline.start(config)

    colorizer = rs.colorizer()
    align_to = rs.stream.color
    align = rs.align(align_to)

    colorizer = rs.colorizer()

    align = rs.align(rs.stream.depth)

    # skip the fist Frames
    for i in range(10):
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()

    aligned = align.process(frames)
    color_aligned_to_depth = aligned.first(rs.stream.color)

    depth_frame = frames.first(rs.stream.depth)
    color_frame = aligned.get_color_frame()

    # Apply filters
    filters = [rs.disparity_transform(),
               rs.spatial_filter(),
               rs.temporal_filter(),
               rs.disparity_transform(False)]
    for f in filters:
        depth_frame = f.process(depth_frame)

    color = np.asanyarray(color_frame.get_data())
    points = pc.calculate(depth_frame)
    w = rs.video_frame(depth_frame).width
    h = rs.video_frame(depth_frame).height
    print('h: ' + str(h) + 'w: ' + str(w))
    vertices = np.asanyarray(points.get_vertices()).view(np.float32).reshape(h, w, 3)

    # Stop pipeline
    pipeline.stop()
    return color, vertices

color_image, verts = get_image()

xmin, xmax, ymin, ymax = 410, 860, 300, 540  # Bounding Box

roi = verts[ymin:ymax, xmin:xmax, :]

# Pass xyz to Open3D.o3d.geometry.PointCloud 
reshaped_roi = np.reshape(roi, (-1, 3))
print(reshaped_roi.shape)
reshaped_verts = np.reshape(verts, (-1, 3))

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(reshaped_roi)
o3d.io.write_point_cloud("reshaped_roi.ply", pcd)  # Red in the second picture

pcd_verts = o3d.geometry.PointCloud()
pcd_verts.points = o3d.utility.Vector3dVector(reshaped_verts)
o3d.io.write_point_cloud("reshaped_verts.ply", pcd_verts) #