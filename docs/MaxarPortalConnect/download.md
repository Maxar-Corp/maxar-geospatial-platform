# Download
1. In the Maxar Portal Connect plugin, go to the **Download** tab.
2. Select your download folder, image format, and filename using the options in the 
**Download Options** section. NOTE: JPEG is not supported for full resolution downloads.
3. Ensure your QGIS session Coordinate Reference System (CRS) is set to EPSG:3857 or EPSG:4326. Your
image will be downloaded in the CRS QGIS is set to.
4. Once the above steps have been completed, there are two methods of downloading an image: snapshot or full resolution.

## Download a snapshot
A snapshot is a screen resolution image downloaded to the current extent of your QGIS viewport.
To use this feature, you first need to use the streaming tab to create a WMS or WMTS imagery layer.
Then, you will select one of these layers to download the imagery you see in QGIS.
Snapshots can be PNG, JPEG, or geotiff and are always 1024x1024 pixels. The minimum scale for a
snapshot download is  1:75000.

1. In the **Snapshot Download** section, from the **Layer** drop-down, select a layer.
    * Only Maxar Imagery Layers Populate in the dropdown.
    * If you don't see the layer you want to use, click **Load Layers** to reload the
available layers in the dropdown. You may need to do this if you have turned the plugin on
and off.
2. Ensure you are zoomed in closer than 1:75000.
3. Select **Download Snapshot**. The extent of the viewport downloads at screen resolution.

## Download a full resolution image
A full resolution download requires users to select a single featureId for download and 
zoom in to scales greater than 1:10000. Full resolution images can be downloaded in PNG or
georeferenced tiff image formats. The tool will download several small 1024x1024 tiles 
at full resolution and then stitch them together to create an image which captures your entire
viewport.

1. In the **Full Resolution Download** section, enter the Feature ID you wish to download.
    * To find a Feature ID, use the Metadata Viewer tab.
    * Your current viewport must be within the bounds of the Feature ID you are downloading.
2. Ensure you are zoomed in closer than 1:10000.
3. Select **Download Full Resolution Feature Clipped to Extent**.

#### Example view of the download tab
![Figure 2](/images/download.PNG)