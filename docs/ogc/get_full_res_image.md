# Download Full Resolution Image

## Args:


#### featureid (str) (required):

  The `featureid` is the online id of the desired image feature
  
   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce')
	 
#### thread_number (int):

  The number of threads used in the download process. More threads will generally go faster but use more system resources (defaults to 100 threads).

   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', thread_number=200)
	 
#### bbox (str):

  A `bbox` (bounding box) is a rectangular feature that will encompass a desired Area Of Interest (AOI).
  The format is miny,minx,maxy,maxx (minimum y coordinate, minimum x coordinate, maximum y coordinate, maximum y coordinate) for projection EPSG:4326 (defaults to EPSG:4326).
  
   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', bbox="39.7530, -104.9962, 39.7580, -104.9912")
	 
#### mosaic (bool):

  Flag to create mosaic image from downloaded files (defaults to False)
  
   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', mosaic=True)
	 
#### srsname (str):

  The `srsname` is the desired projection for the downloaded image (defaults to EPSG:4326)
	
   **Example:**
	
	 interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', srsname='EPSG:3857')
	 
	 
## Kwargs:	 
	 

#### outputdirectory (str):

  The `outputdirectory` is the desired location for the image to be downloaded. `outputdirectory` defaults to root directory (ex: `r'C:\Users\<user>'`).

   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', outputdirectory=r'C:\Users\<user>\full_res_directory')

#### img_format (str):

  The `img_format` is the desired format of the returned object. Available options include **jpeg**, **png**, or **geotiff**

   **Example:**
   
     interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', img_format='jpeg')
	 
#### filename (str):

  If `mosaic` is set to True, the filename of the mosaiced image, defaults to `merged_image`. Recommended to be used with `outputdirectory` as noted above.
  
    **Example:**
	
	  interface.get_full_res_image(featureid='932f7992a4d86a9ca412c024c22792ce', outputdirectory=r'C:\Users\<user>\full_res_directory', filename='My_Mosaic')
	  