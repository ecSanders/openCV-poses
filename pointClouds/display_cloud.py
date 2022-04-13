import cv2 as cv
import open3d as o3d
import numpy as np

cloud = o3d.data.PLYPointCloud()
pcd01 = o3d.io.read_point_cloud("data/1.ply")
pcd02 = o3d.io.read_point_cloud("data/2.ply")

o3d.visualization.draw_geometries([pcd01,pcd02])