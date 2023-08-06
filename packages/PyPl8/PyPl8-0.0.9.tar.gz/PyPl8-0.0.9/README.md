# PyPl8

Image analysis package for segmenting images of microbial communities and extracting quantitative features automatically. 

## Background
This package makes use of the cv2 and sci-kit image libraries. 

It was developed in the Dudley lab at Pacific Northwest Research Institute and is currently most useful for analyzing images of rectangularly arrayed
patches/colonies on omnitrays photographed against a dark background.

## Organization

* The function in the barcode methods can be used to rename images based on a barcode visible in the image if an excel spreadsheet 
relating barcode numbers to relevant plate information is provided.

* The functions in the preprocessing methods are used to crop each image to relevant areas of interest

* ProcessImages.py contains the main functions for processing a single image or a batch of images

* Now includes parallel batch processing

* There are several example images included in the package which can be used for demos

