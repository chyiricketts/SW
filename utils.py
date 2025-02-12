import numpy as np
import os
import imageio.v3 as iio
import matplotlib.pyplot as plt


def masks_to_png(bmp_file, npy_file, save_path, crop_size = 150):

    # Load the NPY mask file
    mask_data = np.load(npy_file, allow_pickle=True).item()
    masks = mask_data['masks']

    # Read the BMP image
    img = iio.imread(bmp_file)  # Reads BMP into a NumPy array

    # Convert BMP image to grayscale if it's RGB
    if img.ndim == 3 and img.shape[2] == 3:
        img = np.mean(img, axis=2).astype(np.uint8)  # Convert to grayscale

    # Get unique cell labels (excluding background, usually 0)
    cell_labels = np.unique(masks)
    cell_labels = cell_labels[cell_labels > 0]

    images = []

    for label in cell_labels:
        # Find coordinates of the current cell
        cell_coords = np.column_stack(np.where(masks == label))  # (row, col) positions
        r_min, c_min = cell_coords.min(axis=0)
        r_max, c_max = cell_coords.max(axis=0)

        # Compute center of the cell
        center_r, center_c = (r_min + r_max) // 2, (c_min + c_max) // 2

        # Define cropping window
        half_crop = crop_size // 2
        r_start, r_end = max(0, center_r - half_crop), min(img.shape[0], center_r + half_crop)
        c_start, c_end = max(0, center_c - half_crop), min(img.shape[1], center_c + half_crop)

        # Extract cropped image
        cropped_img = img[r_start:r_end, c_start:c_end]

        # Ensure output folder exists
        os.makedirs(save_path, exist_ok=True)

        # Save the extracted cell image
        filename = f"{os.path.basename(bmp_file).replace('.bmp', '')}_cell_{label}.png"
        plt.imsave(os.path.join(save_path, filename), cropped_img, cmap='gray')

        # Store metadata
        images.append({
            "filename": filename,
            "label": label,
            "center": (center_r, center_c)
        })

    return images