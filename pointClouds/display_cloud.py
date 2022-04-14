import cv2 as cv
import open3d as o3d
import numpy as np

cloud = o3d.data.PLYPointCloud()
pcd01 = o3d.io.read_point_cloud("data/exp01.ply")
pcd02 = o3d.io.read_point_cloud("data/rs02.ply")

o3d.visualization.draw_geometries([pcd01])