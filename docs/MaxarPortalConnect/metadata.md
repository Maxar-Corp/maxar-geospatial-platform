# Metadata Viewer
The metadata viewer tab allows users to see the metadata of all the images that intersect
the current viewport.

1. In the Maxar Portal Connect plugin, go to the Metadata Viewer tab.
2. If the list of layers does not match the layers in your QGIS **Layers** tab, select **Load Layers**
to refresh the list.
3. From the Layer drop-down, select the layer you want to view metadata for.
4. Select Get Metadata. Image metadata displays for imagery in the layer you selected that intersects
your viewport.
    * By default, the metadata table shows
        * featureId
        * source
        * acquisitionDate
    * If your layer has additional CQL filters applied to it, those parameters will also show in the table.
    * The default stacking profile stacks images by acquistionDate. So, the imagery on top of the layer
you are viewing will also be on top of the table in the metadataViewer.
#### Example table of the metadata viewer
![Figure 3](/images/metadataViewer.PNG)