import numpy as np
import nibabel as nib
from scipy.ndimage import affine_transform
from skimage.metrics import normalized_mutual_information as nmi

def load_mri_image(filepath):
    """Load and normalize a 2D slice from a 3D MRI image in NIfTI format"""
    
    try: data = nib.load(filepath).get_fdata()
    except FileNotFoundError: raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e: raise RuntimeError(f"Error loading NIfTI file: {e}")

    # Extract the middle slice and normalize intensities to [0, 1]
    slice_2d = data[:, :, data.shape[2] // 2]
    slice_2d = (slice_2d - np.min(slice_2d)) / (np.max(slice_2d) - np.min(slice_2d))
    return slice_2d

def apply_affine(image, angle, scale, tx, ty):
    """Apply an affine transformation to an image"""
    transform_matrix = np.array([
        [scale * np.cos(angle), -scale * np.sin(angle), tx],
        [scale * np.sin(angle),  scale * np.cos(angle), ty]
    ])
    return affine_transform(image, transform_matrix[:2, :2], offset=(tx, ty))

def simulated_annealing(fixed, moving, initial_params, max_iter=2500, T_init=1.0, cooling_rate=0.95):
    """
    Optimize the alignment of the moving image to the fixed image using simulated annealing.
    Args:
        fixed: Fixed reference image.
        moving: Moving image to align.
        initial_params: Initial guess for transformation parameters (angle, scale, tx, ty).
        max_iter: Maximum number of iterations.
        T_init: Initial temperature for annealing.
        cooling_rate: Cooling schedule (fraction by which temperature decreases).
    Returns:
        Best transformation parameters and similarity score.
    """
    def random_perturbation(params):
        """Tune the parameters randomly within a defined range."""
        return {
            'angle': params['angle'] + np.random.uniform(-np.radians(5), np.radians(5)),
            'scale': params['scale'] * np.random.uniform(0.95, 1.05),
            'tx': params['tx'] + np.random.uniform(-5, 5),
            'ty': params['ty'] + np.random.uniform(-5, 5)
        }

    current_params = initial_params.copy()
    current_image = apply_affine(moving, **current_params)
    current_score = nmi(fixed, current_image)
    best_params = current_params.copy()
    best_score = current_score
    T = T_init

    for i in range(max_iter):
        # Generate a new candidate solution
        new_params = random_perturbation(current_params)
        new_image = apply_affine(moving, **new_params)
        new_score = nmi(fixed, new_image)

        # Accept or reject the new solution based on the annealing probability
        if new_score > current_score or np.random.rand() < np.exp((new_score - current_score) / T):
            current_params = new_params
            current_score = new_score
            if new_score > best_score:
                best_params = new_params
                best_score = new_score

        # Cool down the temperature
        T *= cooling_rate
        # Log progress
        if i % 100 == 0:
            print(f"Iteration {i}: Best NMI = {best_score:.4f}")
                    
    return best_params, best_score

# Main function
if __name__ == "__main__":
    # Load the reference image (NIfTI format)
    fixed = load_mri_image('avg152T1_LR_nifti.nii.gz')
    
    # Create an artificially transformed moving image for testing the implementation
    true_params = {'angle': np.radians(15), 'scale': 1.1, 'tx': 10, 'ty': -20}
    moving = apply_affine(fixed, **true_params)
    
    # Initialize parameters for simulated annealing
    initial_params = {'angle': 0.0, 'scale': 1.0, 'tx': 0.0, 'ty': 0.0}

    # Optimize the alignment using simulated annealing
    best_params, best_score = simulated_annealing(fixed, moving, initial_params)

    # Apply the optimized transformation to the moving image
    aligned_image = apply_affine(moving, **best_params)

    # Results
    print(f"True Parameters: {true_params}")
    print(f"Optimized Parameters: {best_params}")
