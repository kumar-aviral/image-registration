
---

## Simulated Annealing for Medical Image Registration

### Overview
This project implements a **simulated annealing-based image registration algorithm** for aligning two medical images. The algorithm uses affine transformations (translation, rotation, and scaling) to align a "moving" MRI image with a "fixed" reference image. The similarity between the two images is evaluated using **Normalized Mutual Information (NMI)**, a robust metric commonly used in medical imaging.

### Problem Statement
Medical image registration is a critical task in computational health, enabling the alignment of images for motion correction, multi-modal image fusion, and longitudinal studies. This implementation demonstrates the application of **simulated annealing**, a global optimization algorithm, to achieve robust alignment in the presence of complex similarity metric landscapes. 
**This implementation is for learning purposes only**.

### Features
- **Affine Transformations**: Supports translation, rotation, and scaling.
- **Global Optimization**: Uses simulated annealing to explore the parameter space and avoid local minima.
- **Similarity Metric**: Evaluates alignment using NMI, ensuring robust performance for both intra-modality and multi-modality images.
---

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/kumar-aviral/image-registration.git
   cd image-registration
   ```

2. Install dependencies:
   ```bash
   pip install numpy nibabel scipy matplotlib scikit-image
   ```
---

### Usage
1. Replace `'avg152T1_LR_nifti.nii.gz'` in the code with the path to your NIfTI image file.
2. Or download `'avg152T1_LR_nifti.nii.gz'` from `'https://nifti.nimh.nih.gov/nifti-1/data/'`
3. Run the script:
   ```bash
   python image-registration-SA.py
   ```
4. The script outputs:
   - The true and optimized transformation parameters.
   - The best NMI score.
   - A convergence plot of the NMI score.
---

### Example Output
- **True Parameters**: `{angle: 15°, scale: 1.1, tx: 10, ty: -20}`
- **Optimized Parameters**: `{angle: ~-15°, scale: ~-0.9, tx: ~0.3, ty: ~19}`
- **Best NMI Score**: `1.1673`

---
### Dependencies
- Python 3.7+
- `numpy`
- `nibabel`
- `scipy`
- `matplotlib`
- `scikit-image`

---

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Contact
For questions or feedback, feel free to contact me at: **[aviralk@alumni.cmu.edu]**

---
