from numpy import radians, cos, sin, array
from matplotlib.pyplot import subplots, title, show
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull

# Define a function to rotate points around a pivot point
def rotate_points(points, angle_deg, pivot=(0, 0)):
    angle_rad = radians(angle_deg)
    cos_angle, sin_angle = cos(angle_rad), sin(angle_rad)
    rotated_points = []

    for x, y in points:
        # Translate points to origin
        x_shifted, y_shifted = x - pivot[0], y - pivot[1]
        # Rotate points
        x_rotated = x_shifted * cos_angle - y_shifted * sin_angle + pivot[0]
        y_rotated = x_shifted * sin_angle + y_shifted * cos_angle + pivot[1]
        rotated_points.append((x_rotated, y_rotated))

    return rotated_points

# Define the original "feet" rectangles
left_foot = ((1, 1), (3, 1), (3, 2), (1, 2))
right_foot = ((5, 1), (7, 1), (7, 2), (5, 2))

# Define rotation angles and pivot points for each foot
angle_left_foot = 115  # degrees
angle_right_foot = 245 #-115 degrees
pivot_left_foot = (2, 1.5)
pivot_right_foot = (6, 1.5)

# Rotate the points
left_foot_rotated = rotate_points(left_foot, angle_left_foot, pivot_left_foot)
right_foot_rotated = rotate_points(right_foot, angle_right_foot, pivot_right_foot)

# Combine vertices from rotated feet for equilibrium area calculation
all_rotated_vertices = left_foot_rotated + right_foot_rotated
rotated_vertices = array(all_rotated_vertices)

# Calculate the convex hull of the rotated points to get the true equilibrium area
hull = ConvexHull(rotated_vertices)

# Extract the points that form the convex hull (outer boundary of the equilibrium area)
equilibrium_polygon_convex_hull = [rotated_vertices[vertex] for vertex in hull.vertices]

# Plot the rotated feet and the true equilibrium area using the convex hull
fig, ax = subplots()
left_foot_rect_rotated = Polygon(left_foot_rotated, closed=True, fill=True, color="blue", alpha=0.3, label="Left Foot")
right_foot_rect_rotated = Polygon(right_foot_rotated, closed=True, fill=True, color="green", alpha=0.3, label="Right Foot")
ax.add_patch(left_foot_rect_rotated)
ax.add_patch(right_foot_rect_rotated)

# Plot the true equilibrium area based on the convex hull
equilibrium_polygon_shape_convex_hull = Polygon(equilibrium_polygon_convex_hull,
                                                closed=True,
                                                fill=False,
                                                edgecolor="red",
                                                linestyle="--",
                                                linewidth=2,
                                                label="Equilibrium Area")
ax.add_patch(equilibrium_polygon_shape_convex_hull)

# Set plot limits and labels
ax.set_xlim(0, 8)
ax.set_ylim(0, 4)
ax.set_aspect('equal', 'box') #para q NO se deforme
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()
title("Feet Placement and Equilibrium Area (Convex Hull)")
#plt.grid(True)
show()
