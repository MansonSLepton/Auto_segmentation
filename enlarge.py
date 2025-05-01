import trimesh
import numpy as np

# Load the tooth STL file
input_path = r"D:\Eastman\Patient017\SLZ000.dcm_Segmentation_UR8.stl"
tooth_mesh = trimesh.load(input_path)

# Get the Z-axis bounds of the model
z_min, z_max = tooth_mesh.bounds[:, 2]

# Define the root region as the top 30% of the Z-axis
root_threshold = z_max - (z_max - z_min) * 0.5

# Separate the vertices into root and non-root regions
vertices = tooth_mesh.vertices.copy()
root_indices = np.where(vertices[:, 2] >= root_threshold)[0]  # Root region vertices
non_root_indices = np.where(vertices[:, 2] < root_threshold)[0]  # Non-root region vertices

# Enlarge the root region by 10%
# Compute the center of the root region for scaling
root_center = vertices[root_indices].mean(axis=0)
vertices[root_indices] = root_center + (vertices[root_indices] - root_center) * 1.1

# Reconstruct the mesh with the modified vertices
enlarged_tooth = trimesh.Trimesh(vertices=vertices, faces=tooth_mesh.faces)

# Save the new STL file
output_path = r"D:\Eastman\Patient017\UR8_root_enlarged.stl"
enlarged_tooth.export(output_path, file_type='stl')

print(f"The tooth model with an enlarged root has been saved to {output_path}")
