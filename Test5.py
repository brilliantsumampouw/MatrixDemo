import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Define the original shape: a square
original_points = np.array([
    [0, 0],
    [1, 0],
    [1, 1],
    [0, 1],
    [0, 0]  # Close the square
])

def apply_transformation(points, transformation_matrix):
    # Convert points to homogeneous coordinates (add a column of 1s)
    homogeneous_points = np.column_stack((points, np.ones(len(points))))
    
    # Apply transformation: P' = P @ T
    # FIX APPLIED: Removed .T (transpose) to correctly use the column-major transformation matrices defined below.
    transformed_homogeneous = homogeneous_points @ transformation_matrix
    
    # Convert back to 2D (discard the third column which should still be 1)
    transformed_points = transformed_homogeneous[:, :2]
    return transformed_points

def plot_shapes(original, transformed):
    fig, ax = plt.subplots(figsize=(8, 8))
    # Set limits based on the extent of the shapes
    all_points = np.concatenate([original, transformed])
    min_val = np.min(all_points) - 1
    max_val = np.max(all_points) + 1
    
    ax.plot(original[:, 0], original[:, 1], 'b-', label='Original', linewidth=2)
    ax.plot(transformed[:, 0], transformed[:, 1], 'r-', label='Transformed', linewidth=2)
    
    ax.set_aspect('equal')
    ax.grid(True)
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim(min_val, max_val) # Set dynamic limits
    ax.set_ylim(min_val, max_val)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_title('2D Matrix Transformations')
    return fig

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

if st.session_state.page == 'welcome':
    st.title("Matrix Transformation Demo")
    st.write("This interactive app allows you to explore 2D matrix transformations on a geometric shape (a square).")
    st.write("Use the sidebar to select and apply transformations like translation, scaling, rotation, shearing, and reflection.")
    st.write("Click Below To Start")
    
    if st.button("Start Demo"):
        st.session_state.page = 'demo'
        st.rerun()

elif st.session_state.page == 'demo':
    st.title("2D Matrix Transformations Demo")

    st.sidebar.header("Select Transformation")

    transformation = st.sidebar.selectbox(
        "Choose a transformation:",
        ["None", "Translation", "Scaling", "Rotation", "Shearing", "Reflection"]
    )

    transformed_points = original_points.copy()
    current_matrix_display = None

    # --- Transformation Logic ---
    if transformation == "Translation":
        tx = st.sidebar.number_input("X Shift (tₓ)", value=1.0, step=0.1)
        ty = st.sidebar.number_input("Y Shift (tᵧ)", value=1.0, step=0.1)
        # Standard Translation Matrix (Column-Major)
        T = np.array([[1, 0, tx], 
                      [0, 1, ty], 
                      [0, 0, 1]])
        transformed_points = apply_transformation(original_points, T)
        current_matrix_display = T

    elif transformation == "Scaling":
        sx = st.sidebar.number_input("X Scale Factor (sₓ)", value=1.0, step=0.1, min_value=0.1)
        sy = st.sidebar.number_input("Y Scale Factor (sᵧ)", value=1.0, step=0.1, min_value=0.1)
        # Standard Scaling Matrix
        S = np.array([[sx, 0, 0], 
                      [0, sy, 0], 
                      [0, 0, 1]])
        transformed_points = apply_transformation(original_points, S)
        current_matrix_display = S

    elif transformation == "Rotation":
        angle_deg = st.sidebar.number_input("Angle (degrees) θ", value=45.0, step=1.0)
        angle_rad = np.radians(angle_deg)
        c, s = np.cos(angle_rad), np.sin(angle_rad)
        # Standard Rotation Matrix (around origin)
        R = np.array([[c, -s, 0],
                      [s, c, 0],
                      [0, 0, 1]])
        transformed_points = apply_transformation(original_points, R)
        current_matrix_display = R

    elif transformation == "Shearing":
        shx = st.sidebar.number_input("X Shear Factor (hₓ)", value=0.0, step=0.1)
        shy = st.sidebar.number_input("Y Shear Factor (hᵧ)", value=0.0, step=0.1)
        # Standard Shearing Matrix
        Sh = np.array([[1, shx, 0], 
                       [shy, 1, 0], 
                       [0, 0, 1]])
        transformed_points = apply_transformation(original_points, Sh)
        current_matrix_display = Sh

    elif transformation == "Reflection":
        axis = st.sidebar.selectbox("Choose axis:", ["X-axis", "Y-axis", "Line y=x"])
        if axis == "X-axis":
            # Reflection across X-axis (y -> -y)
            Ref = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        elif axis == "Y-axis":
            # Reflection across Y-axis (x -> -x)
            Ref = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
        elif axis == "Line y=x":
            # Reflection across y=x (swap x and y)
            Ref = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
        transformed_points = apply_transformation(original_points, Ref)
        current_matrix_display = Ref
        
    elif transformation == "None":
        current_matrix_display = np.identity(3)

    # --- Plotting and Display ---
    fig = plot_shapes(original_points, transformed_points)
    st.pyplot(fig)

    if current_matrix_display is not None:
        st.subheader("Homogeneous Transformation Matrix ($\mathbf{T}$)")
        st.markdown("The $3 \\times 3$ matrix used for this transformation, where points $\mathbf{P}$ are row vectors ($\mathbf{P}' = \mathbf{P} \mathbf{T}$):")
        
        # Display the matrix using st.table for a clean view
        st.dataframe(current_matrix_display, hide_index=True)