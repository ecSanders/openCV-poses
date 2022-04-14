# First import the library
import pyrealsense2 as rs
import cv2 as cv
import open3d as o3d
import numpy as np
import time


pc = rs.pointcloud()
points = rs.points()

pipe = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth)
config.enable_stream(rs.stream.color)

pipe.start(config)
colorizer = rs.colorizer()
try:
    frames = pipe.wait_for_frames()

    color = frames.get_color_frame()

    pc.map_to(color)

    depth = frames.get_depth_frame()

    points = pc.calculate(depth)

    colorized = colorizer.process()

    ply = rs.save_to_ply("data/exp01.ply")
    ply.set_option(rs.save_to_ply.option_ply_binary, False)
    ply.set_option(rs.save_to_ply.option_ply_normals, True)
    ply.process(colorized)
finally:
    pipe.stop()

pcd = o3d.io.read_point_cloud("data/exp01.ply")
o3d.visualization.draw_geometries([pcd])