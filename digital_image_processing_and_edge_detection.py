# -*- coding: utf-8 -*-
"""Digital_Image_Processing_And_Edge_Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XQmD-Fb2c1xOmPFiZi_AuZGcB-t8Po3d
"""

from google.colab import drive
drive.mount('/content/drive')

import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(image, title):
    """Display an image with its title."""
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:  # Grayscale
        plt.imshow(image, cmap='gray')
    else:  # RGB
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def add_salt_pepper_noise(image, salt_prob=0.15, pepper_prob=0.15):
    """
    Add salt and pepper noise to an image.
    salt_prob: Probability of adding salt (white) noise
    pepper_prob: Probability of adding pepper (black) noise
    """
    noisy_image = np.copy(image)
    # Salt noise (white spots)
    salt_mask = np.random.random(image.shape) < salt_prob
    noisy_image[salt_mask] = 255

    # Pepper noise (black spots)
    pepper_mask = np.random.random(image.shape) < pepper_prob
    noisy_image[pepper_mask] = 0

    return noisy_image

def adaptive_median_filter(image, initial_window=3, max_window=7):
    """
    Apply adaptive median filter to remove salt and pepper noise.
    initial_window: Starting window size
    max_window: Maximum window size
    """
    filtered_image = np.copy(image)
    height, width = image.shape
    padding = max_window // 2

    # Pad the image to handle border pixels
    padded_image = np.pad(image, padding, mode='reflect')

    for i in range(height):
        for j in range(width):
            window_size = initial_window
            while window_size <= max_window:
                half_window = window_size // 2

                # Extract window centered around current pixel
                window = padded_image[i:i+2*half_window+1, j:j+2*half_window+1]

                # Compute window statistics
                z_min = np.min(window)
                z_max = np.max(window)
                z_med = np.median(window)
                z_xy = padded_image[i+padding, j+padding]  # Center pixel

                # Stage A: Check if median is between min and max
                if z_med > z_min and z_med < z_max:
                    # Stage B: Check if pixel is not noise
                    if z_xy > z_min and z_xy < z_max:
                        filtered_image[i, j] = z_xy  # Not noise, keep original
                    else:
                        filtered_image[i, j] = z_med  # Noise, replace with median
                    break
                else:
                    # Increase window size and try again
                    window_size += 2
                    if window_size > max_window:
                        filtered_image[i, j] = z_med  # Use median as last resort

    return filtered_image

def main():
    # Step 1: Load the image (replace with your image path)
    image_path = "https://github.com/namanjain-codin/Adaptive-Median-Filter-Edge-Detection/blob/main/City_Skyline.avif"  # Replace with your image path
    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Error: Could not load image from {image_path}")
        return

    display_image(original_image, "Original Image")

    # Step 2: Convert RGB to Grayscale
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    display_image(gray_image, "Grayscale Image")

    # Step 3: Add 30% Salt and Pepper noise (15% salt, 15% pepper)
    noisy_image = add_salt_pepper_noise(gray_image, salt_prob=0.15, pepper_prob=0.15)
    display_image(noisy_image, "Image with 30% Salt and Pepper Noise")

    # Step 4: Remove noise using Adaptive Median Filter
    denoised_image = adaptive_median_filter(noisy_image)
    display_image(denoised_image, "Denoised Image using Adaptive Median Filter")

    # Step 5: Perform Canny Edge Detection
    edges = cv2.Canny(denoised_image, threshold1=30, threshold2=100)
    display_image(edges, "Canny Edge Detection")

    # Step 6: Apply Otsu's Thresholding
    _, binary_image = cv2.threshold(denoised_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    threshold_value = _  # The threshold value determined by Otsu's method

    print(f"Otsu's Threshold Value: {threshold_value}")
    display_image(binary_image, f"Binary Image (Otsu's Threshold = {threshold_value})")

    # Save results
    cv2.imwrite("grayscale_image.jpg", gray_image)
    cv2.imwrite("noisy_image.jpg", noisy_image)
    cv2.imwrite("denoised_image.jpg", denoised_image)
    cv2.imwrite("canny_edges.jpg", edges)
    cv2.imwrite("binary_image.jpg", binary_image)

    print("All processing steps completed successfully!")

if __name__ == "__main__":
    main()

