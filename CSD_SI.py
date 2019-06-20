import cv2
import numpy as np
import rasterio



def cloud_shadow_detection(input_ms_file, output_cloud_mask_file, output_cloud_shadow_mask_file, R, G, B, NIR, T1, t2, t3, t4, 
                           T5, T6, T7, T8):
    """
    This function is used to implement the Cloud/Shadow Detection based on Spectral Indices (CSD - SI) algorithm that is 
    proposed in the paper 'Cloud/shadow Detection Based on Spectral Indices for Multi/Hyperspectral Optical Remote Sensing 
    Imagery' by Zhai H., Zhang H., Zhang L., Li P. (2018).
    
    Please note that this particular implementation is specifically designed for multispectral images, and that changes 
    should be made to this code for use with hyperspectral images.
    
    Inputs:
    - input_ms_file: Path of multispectral file for the detection of clouds and cloud shadows
    - output_cloud_mask_file: Path of cloud mask file to be saved
    - output_cloud_shadow_mask_file: Path of cloud shadow mask file to be saved
    - R: Band number of red band
    - G: Band number of green band
    - B: Band number of blue band
    - NIR: Band number of near - infrared band
    - T1: Threshold value for the threshold T1
    - t2: Adjusting coefficient for threshold T2
    - t3: Adjusting coefficient for threshold T3
    - t4: Adjusting coefficient for threshold T4
    - T5: Height of local search window for spatial matching
    - T6: Width of local search window for spatial matching
    - T7: Kernel size for median filter to be applied to preliminary cloud mask
    - T8: Kernel size for median filter to be appied to refined cloud shadow mask
    
    
    Outputs:
    - final_cloud_mask: Binary array indicating the presence of clouds
    - final_cloud_shadow_mask: Binary array indicating the presence of cloud shadows
    
    """
    
    with rasterio.open(input_ms_file) as f:
        metadata = f.profile
        img = np.transpose(f.read(tuple(np.arange(metadata['count']) + 1)), [1, 2, 0])
    
    
    
    ci_1 = (3 * img[:, :, (NIR - 1)]) / (img[:, :, (R - 1)] + img[:, :, (G - 1)] + img[:, :, (B - 1)] + 1)
    ci_2 = (img[:, :, (R - 1)] + img[:, :, (G - 1)] + img[:, :, (B - 1)] + img[:, :, (NIR - 1)]) / 4
    
    
    
    T2 = np.mean(ci_2) + (t2 * (np.max(ci_2) - np.mean(ci_2)))
    
    prelim_cloud_mask = np.uint8(np.logical_and(np.abs(ci_1 - 1) < T1, ci_2 > T2))
    final_cloud_mask = cv2.medianBlur(prelim_cloud_mask, T7)
    final_cloud_mask = np.uint8(np.expand_dims(final_cloud_mask, axis = 2))
    
    
    
    T3 = np.min(img[:, :, (NIR - 1)]) + (t3 * (np.mean(img[:, :, (NIR - 1)]) - np.min(img[:, :, (NIR - 1)])))
    T4 = np.min(img[:, :, (B - 1)]) + (t4 * (np.mean(img[:, :, (B - 1)]) - np.min(img[:, :, (B - 1)])))
    
    prelim_cloud_shadow_mask = np.uint8(np.logical_and(img[:, :, (NIR - 1)] < T3, img[:, :, (B - 1)] < T4))
    
    spatial_search_kernel = np.ones((T5, T6))
    non_pseudo_cloud_shadow_position_mask = np.uint8(cv2.filter2D(final_cloud_mask, -1, spatial_search_kernel) > 0)
    
    refined_cloud_shadow_mask = prelim_cloud_shadow_mask * non_pseudo_cloud_shadow_position_mask
    final_cloud_shadow_mask = cv2.medianBlur(refined_cloud_shadow_mask, T8)
    final_cloud_shadow_mask = np.expand_dims(final_cloud_shadow_mask, axis = 2)
    
    
    metadata['dtype'] = 'uint8'
    metadata['count'] = 1
    
    with rasterio.open(output_cloud_mask_file, 'w', **metadata) as dst:
        dst.write(np.transpose(final_cloud_mask, [2, 0, 1]))
        
    with rasterio.open(output_cloud_shadow_mask_file, 'w', **metadata) as dst2:
        dst2.write(np.transpose(final_cloud_shadow_mask, [2, 0, 1]))
        
    return final_cloud_mask, final_cloud_shadow_mask
