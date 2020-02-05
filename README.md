# Cloud-Shadow-Detection-Based-on-Spectral-Indices
Python implementation of cloud and cloud shadow detection algorithm proposed in academia

This repository contains functions to detect clouds and their corresponding shadows in multispectral images, based on the Cloud Shadow
Detection based on Spectral Indices (CSD - SI) algorithm proposed in the paper 'Cloud/Shadow Detection Based on Spectral Indices for 
Multi/Hyperspectral Optical Remote Sensing Imagery' by Zhai H., Zhang H., Zhang L., Li P. (2018).

Note that this function is mainly designed for use with multispectral images. As such, the source code must be changed in order to be
applied to hyperspectral images.

Requirements:
- cv2
- numpy
- rasterio

The following images illustrate the algorithm in action, using generic parameter values. As such, it is expected that the performance of the algorithm might improve after fine - tuning the parameters.



Sentinel - 2 Test Image (Courtesy of European Space Agency Copernicus Open Access Hub):
![alt text](https://github.com/ThomasWangWeiHong/Cloud-Shadow-Detection-Based-on-Spectral-Indices/blob/master/Test_Image.JPG)


Cloud Mask:
![alt text](https://github.com/ThomasWangWeiHong/Cloud-Shadow-Detection-Based-on-Spectral-Indices/blob/master/Cloud_Mask_Image.JPG)
