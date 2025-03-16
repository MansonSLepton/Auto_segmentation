import open3d as o3d
import numpy as np

# 1️⃣ **计算 Dice Similarity Coefficient (DSC)**
def compute_dice_coefficient(stl_path1, stl_path2, voxel_size=0.5):
    """ 计算 STL 之间的 Dice Similarity Coefficient (DSC) """
    mesh1 = o3d.io.read_triangle_mesh(stl_path1)
    mesh2 = o3d.io.read_triangle_mesh(stl_path2)

    if mesh1.is_empty() or mesh2.is_empty():
        print("❌ 错误：STL 文件无法加载，请检查路径是否正确。")
        return None

    print(f"▶️ 计算 STL 体素化 (voxel_size={voxel_size})")

    voxel_grid1 = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh1, voxel_size)
    voxel_grid2 = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh2, voxel_size)

    voxels1 = set(tuple(v.grid_index) for v in voxel_grid1.get_voxels())
    voxels2 = set(tuple(v.grid_index) for v in voxel_grid2.get_voxels())

    intersection = len(voxels1 & voxels2)
    dice_score = (2.0 * intersection) / (len(voxels1) + len(voxels2)) if (len(voxels1) + len(voxels2)) > 0 else 0.0

    return dice_score

# 2️⃣ **计算 IoU (Intersection over Union)**
def compute_iou(stl_path1, stl_path2, voxel_size=0.5):
    """ 计算 STL 之间的 Intersection over Union (IoU) """
    mesh1 = o3d.io.read_triangle_mesh(stl_path1)
    mesh2 = o3d.io.read_triangle_mesh(stl_path2)

    voxel_grid1 = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh1, voxel_size)
    voxel_grid2 = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh2, voxel_size)

    voxels1 = set(tuple(v.grid_index) for v in voxel_grid1.get_voxels())
    voxels2 = set(tuple(v.grid_index) for v in voxel_grid2.get_voxels())

    intersection = len(voxels1 & voxels2)
    union = len(voxels1 | voxels2)

    iou_score = intersection / union if union > 0 else 0.0
    return iou_score

# 3️⃣ **计算 Mean Absolute Error (MAE)**
def compute_mae(stl_path1, stl_path2):
    """ 计算 STL 之间的 Mean Absolute Error (MAE) """
    mesh1 = o3d.io.read_triangle_mesh(stl_path1)
    mesh2 = o3d.io.read_triangle_mesh(stl_path2)

    pcd1 = mesh1.sample_points_uniformly(number_of_points=10000)
    pcd2 = mesh2.sample_points_uniformly(number_of_points=10000)

    pcd1_points = np.asarray(pcd1.points)
    pcd2_points = np.asarray(pcd2.points)

    if pcd1_points.shape != pcd2_points.shape:
        print("⚠️ 警告：STL 点云数量不同，可能影响 MAE 计算")
        min_size = min(len(pcd1_points), len(pcd2_points))
        pcd1_points = pcd1_points[:min_size]
        pcd2_points = pcd2_points[:min_size]

    mae = np.mean(np.abs(pcd1_points - pcd2_points))
    return mae

# **STL 文件路径**
stl_path1 = r"D:\Eastman\Patient010\LR5_1_stick.stl"  # 你的 STL
stl_path2 = r"D:\Eastman\Patient010\PRINT\LR5.stl"   # 参考 STL

# **主程序**
if __name__ == "__main__":
    # **计算 DSC**
    dsc = compute_dice_coefficient(stl_path1, stl_path2, voxel_size=0.5)
    print(f"🎯 Dice Similarity Coefficient (DSC): {dsc:.4f}")

    # **计算 IoU**
    iou = compute_iou(stl_path1, stl_path2, voxel_size=0.5)
    print(f"📊 Intersection over Union (IoU): {iou:.4f}")

    # **计算 MAE**
    mae = compute_mae(stl_path1, stl_path2)
    print(f"📏 Mean Absolute Error (MAE): {mae:.6f}")
