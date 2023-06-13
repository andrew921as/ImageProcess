#import SimpleITK as sitk
from ants import get_ants_data, image_read, resample_image, get_mask, registration, apply_transforms, from_numpy, image_write
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib

def rigid_register(fixedImagePath, movingImagePath, type="Rigid"):
    fixed_image = image_read(fixedImagePath)
    moving_image = image_read(movingImagePath)

    # Perform rigid registration
    transform = registration(fixed=fixed_image, moving=moving_image, type_of_transform='Rigid')

    # Apply the transformation to the moving image
    registered_image = apply_transforms(fixed=fixed_image, moving=moving_image, transformlist=transform['fwdtransforms'])
    
    image_write(registered_image, "registered_image.nii.gz")
    
    return "./registered_image.nii.gz"
    # Convert the registered image to a NumPy array

    # Plot the registered image using plt.imshow()

# def rigid_register(fixed_image_path, moving_image_path,moving_seg_image_path):
#     # Load fixed and moving images
#     fixed_image = sitk.ReadImage(fixed_image_path)
#     moving_image = sitk.ReadImage(moving_image_path)
#     moving_seg_image=sitk.ReadImage(moving_seg_image_path)

#     # Convert image types
#     fixed_image = sitk.Cast(fixed_image, sitk.sitkFloat32)
#     moving_image = sitk.Cast(moving_image, sitk.sitkFloat32)
#     moving_seg_image= sitk.Cast(moving_seg_image, sitk.sitkFloat32)
#     # Define the registration components
#     registration_method = sitk.ImageRegistrationMethod()

#     # Similarity metric - Mutual Information
#     registration_method.SetMetricAsMattesMutualInformation()

#     # Interpolator
#     registration_method.SetInterpolator(sitk.sitkNearestNeighbor)

#     # Optimizer - Gradient Descent
#     registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,estimateLearningRate=registration_method.EachIteration)

#     # Initial transform - Identity
#     initial_transform = sitk.Transform()
#     registration_method.SetInitialTransform(initial_transform)

#     # Setup for the registration process
#     registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
#     registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
#     registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

#     # Perform registration
#     final_transform = registration_method.Execute(fixed_image, moving_seg_image)

#     # Resample the moving image to match the fixed image dimensions and orientation
#     reference_image = fixed_image
#     interpolator = sitk.sitkNearestNeighbor
#     default_pixel_value = 0.0
#     resampled_image = sitk.Resample( moving_image,reference_image, final_transform,interpolator, default_pixel_value)

#     # Convert the resampled image to Numpy array
#     resampled_array = sitk.GetArrayFromImage(resampled_image)

#     # Save the resampled image as NIfTI
#     output_image_path = 'Registered_FLAIR.nii.gz'
#     sitk.WriteImage(resampled_image, output_image_path)

#     return output_image_path