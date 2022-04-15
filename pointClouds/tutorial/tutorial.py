import open3d as o3d
import numpy as np
import laspy as lp
import pptk

PATH = r"C:\Users\troy.denning\Repositories\Design For Making\Math + CV\pointClouds\tutorial"
point_cloud=lp.file.File(PATH + r"\2020_Drone_M.las", mode="r")

points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
colors = np.vstack((point_cloud.red, point_cloud.green, point_cloud.blue)).transpose()

factor=10
decimated_points_random = points[::factor]

v = pptk.viewer(points)
v.attributes(colors/65535)

while True:
    selection=v.get('selected')
    if selection.size > 0:
        print(selection)
    