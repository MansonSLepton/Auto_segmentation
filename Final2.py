import trimesh
import numpy as np

# Ask the user if the model is upper or lower tooth
tooth_type = input("Is this an upper tooth or lower tooth? (Enter 'upper' or 'lower'): ").strip().lower()

# Load the tooth STL file
input_path = r"D:\Eastman\Patient016\001001002 Unnamed Series_Segmentation_Segment_1.stl"
tooth_mesh = trimesh.load(input_path)

# Get the Z-axis bounds of the model
z_min, z_max = tooth_mesh.bounds[:, 2]

# Step 1: Add a 2cm stick
stick_length = 20.0  # Length 20mm (2cm)
stick_radius = 0.5   # Radius 0.5mm

# Create the stick
stick = trimesh.creation.cylinder(
    radius=stick_radius,
    height=stick_length,
    sections=32
)

# Position the stick based on tooth type
tooth_center = tooth_mesh.bounds.mean(axis=0)  # Model center point
if tooth_type == 'upper':
    # For upper teeth, stick is placed below the model
    stick_center_z = z_min - stick_length / 2 + 5  # Stick starts 5mm below the model's lowest point
elif tooth_type == 'lower':
    # For lower teeth, stick is placed above the model
    stick_center_z = z_max + stick_length / 2 - 5  # Stick starts 5mm above the model's highest point
else:
    raise ValueError("Invalid input! Please enter 'upper' or 'lower'.")

stick.apply_translation([
    tooth_center[0],  # Align with the X-axis center
    tooth_center[1],  # Align with the Y-axis center
    stick_center_z    # Adjusted Z-axis coordinate
])

# Merge the tooth and the stick
combined_mesh = trimesh.util.concatenate([tooth_mesh, stick])

# Step 2: Enlarge and extend the root region based on tooth type
vertices = combined_mesh.vertices.copy()
if tooth_type == 'upper':
    # For upper teeth, enlarge the Z-axis back half (closer to z_max)
    root_threshold = z_min + (z_max - z_min) * 0.75
    root_indices = np.where(vertices[:, 2] >= root_threshold)[0]  # Back half (root region)
else:
    # For lower teeth, enlarge the Z-axis front half (closer to z_min)
    root_threshold = z_min + (z_max - z_min) * 0.75
    root_indices = np.where(vertices[:, 2] <= root_threshold)[0]  # Front half (root region)

# Enlarge the root region by 10%
root_center = vertices[root_indices].mean(axis=0)
vertices[root_indices] = root_center + (vertices[root_indices] - root_center) * 1.1

# Move the root region based on tooth type
if tooth_type == 'upper':
    vertices[root_indices, 2] += 1  # For upper teeth, move upward
else:
    vertices[root_indices, 2] -= 1  # For lower teeth, move downward

# Smoothly interpolate and fill the gap using non-linear interpolation
transition_range = 10  # Extend the transition range to 10mm
transition_indices = np.where(
    (vertices[:, 2] >= root_threshold - transition_range) & (vertices[:, 2] < root_threshold)
)[0]

for idx in transition_indices:
    # Calculate the distance to the transition boundary
    distance_to_threshold = (vertices[idx, 2] - (root_threshold - transition_range)) / transition_range
    # Use a quadratic function for smooth transition
    weight = distance_to_threshold**2  # Quadratic interpolation
    vertices[idx] = (1 - weight) * vertices[idx] + weight * (
        root_center + (vertices[idx] - root_center) * 1.1
    )
    if tooth_type == 'upper':
        vertices[idx, 2] += weight * 1  # Adjust for upper teeth
    else:
        vertices[idx, 2] -= weight * 1  # Adjust for lower teeth

# Reconstruct the mesh with the modified vertices
final_mesh = trimesh.Trimesh(vertices=vertices, faces=combined_mesh.faces)

# Save the final STL file
if tooth_type == 'upper':
    output_path = r"D:\Eastman\Patient016\UR5_upper_tooth_NEW.stl"
else:
    output_path = r"D:\Eastman\Patient016\UR5_lower_tooth_NEW.stl"

final_mesh.export(output_path, file_type='stl')
print(f"The final modified model has been saved to {output_path}")
