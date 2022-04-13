import cv2
import copy
import open3d as o3d
import numpy as np

def display_clouds_matrix(source, target, matrix):
    temp_source = copy.deepcopy(source)
    temp_source.transform(matrix)
    o3d.visualization.draw_geometries([source,target])

tranformation = np.identity(4)
target = o3d.io.read_point_cloud("data/2.ply")
source = o3d.io.read_point_cloud("data/1.ply")

display_clouds_matrix(source,target,tranformation)

res_icp = o3d.pipelines.registration.registration_icp(
    source,
    target,
    0.02,
    tranformation,
    o3d.pipelines.registration.TransformationEstimationPointToPoint()
)
print(res_icp)

display_clouds_matrix(source,target,res_icp.transformation)

# colored pointcloud registration
# This is implementation of following paper
# J. Park, Q.-Y. Zhou, V. Koltun,
# Colored Point Cloud Registration Revisited, ICCV 2017
voxel_radius = [0.04, 0.02, 0.01]
max_iter = [50, 30, 14]
current_transformation = np.identity(4)
print("3. Colored point cloud registration")
for scale in range(3):
    iter = max_iter[scale]
    radius = voxel_radius[scale]
    print([iter, radius, scale])

    print("3-1. Downsample with a voxel size %.2f" % radius)
    source_down = source.voxel_down_sample(radius)
    target_down = target.voxel_down_sample(radius)

    print("3-2. Estimate normal.")
    source_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))
    target_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))

    print("3-3. Applying colored point cloud registration")
    result_icp = o3d.pipelines.registration.registration_colored_icp(
        source_down, target_down, radius, current_transformation,
        o3d.pipelines.registration.TransformationEstimationForColoredICP(),
        o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=1e-6,
                                                          relative_rmse=1e-6,
                                                          max_iteration=iter))
    current_transformation = result_icp.transformation
    print(result_icp)
display_clouds_matrix(source, target,result_icp.transformation)