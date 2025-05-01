import trimesh
import numpy as np

# Corrected file path
input_path = r"D:\Eastman\Patient017\SLZ000.dcm_Segmentation_UL8.stl"
tooth_mesh = trimesh.load(input_path)

# Create a cylinder (stick)
stick_length = 21.0  # Length 20mm (2cm)
stick_radius = 0.5   # Radius 0.5mm

stick = trimesh.creation.cylinder(
    radius=stick_radius,
    height=stick_length,
    sections=32
)

# Position the cylinder below the model, starting from the center
# Get the center point of the model
tooth_center = tooth_mesh.bounds.mean(axis=0)  # Model center point

# Calculate the position of the stick
# Align the bottom of the cylinder with the lowest point of the model, then move it up by 5mm
tooth_min_z = tooth_mesh.bounds[0][2]  # Lowest Z coordinate of the model
stick_center_z = tooth_min_z - stick_length / 2 + 6  # Move the stick 5mm upward

# Translate the cylinder to start from the model's bottom center and move upward
stick.apply_translation([
    tooth_center[0],  # Align with the X-axis center
    tooth_center[1],  # Align with the Y-axis center
    stick_center_z    # Z-axis coordinate moved 5mm upward
])

# Merge the two meshes
combined_mesh = trimesh.util.concatenate([tooth_mesh, stick])

# Save the combined STL file
output_path = r"D:\Eastman\Patient017\UL8_with_stick.stl"
combined_mesh.export(output_path, file_type='stl')

print(f"The new model has been saved to {output_path}")
