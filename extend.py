import trimesh
import numpy as np

# Load the tooth STL file
input_path = r"D:\Eastman\Patient017\SLZ000.dcm_Segmentation_UR8.stl"
tooth_mesh = trimesh.load(input_path)

# Get the Z-axis bounds of the model
z_min, z_max = tooth_mesh.bounds[:, 2]

# Define the root region as the top 50% of the Z-axis
root_threshold = z_max - (z_max - z_min) * 0.5

# Separate vertices into root and non-root regions
vertices = tooth_mesh.vertices.copy()
root_indices = np.where(vertices[:, 2] >= root_threshold)[0]  # Root region vertices

# Move the root region upward by 1mm
vertices[root_indices, 2] += 1

# Smoothly interpolate and fill the gap
# Identify the transition vertices (close to the threshold)
transition_indices = np.where(
    (vertices[:, 2] >= root_threshold - 5) & (vertices[:, 2] < root_threshold)
)[0]

# Perform linear interpolation to create smooth transition
for idx in transition_indices:
    distance_to_threshold = (vertices[idx, 2] - (root_threshold - 5)) / 5
    vertices[idx, 2] += distance_to_threshold * 1  # Adjust for 1mm upward movement

# Reconstruct the mesh with the modified vertices
modified_tooth = trimesh.Trimesh(vertices=vertices, faces=tooth_mesh.faces)

# Save the new STL file
output_path = r"D:\Eastman\Patient017\UR8_root_moved_and_filled.stl"
modified_tooth.export(output_path, file_type='stl')

print(f"The modified tooth model has been saved to {output_path}")
