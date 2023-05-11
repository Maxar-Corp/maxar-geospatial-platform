# Streaming

1. In the Maxar Portal Connect plugin, go to the **streaming** tab
2. Choose between png or jpeg image formats and EPSG:4326 or EPSG:3857 coordinate reference systems.
3. (Optional) Add a CQL Filter using the CQL Filter Builder or leave CQL Filter blank.
4. (Optional) Add an additional argument. Most users will want to leave this field blank.
5. Click Add WMS Imagery or WMTS Imagery to add an OGC connection to your Table of Contents. This is similar to manually adding a WMS/WMTS layer
in QGIS.
6. If you are using a WMS connection, ensure you are zoomed in below 1:150000 and are over a landmass.

## CQL Filters:

CQL Filter:
  A CQL Filter is a Common Query Language string that allows you to filter imagery based on the metadata of the imagery.
  Documentation on how to format a CQL Filter is found [here](https://securewatchdocs.maxar.com/en-us/Miscellaneous/DevGuides/Common_Query_Language/Query.htm?Highlight=cql%20filter) for SecureWatch and [here](https://gcs-docs.s3.amazonaws.com/EVWHS/Miscellaneous/DevGuides/Common_Query_Language/Query.htm?Highlight=cql%20filter) for GEGD.

   **Examples:**

     groundSampleDistance<=0.4
     source=WV03_VNIR
     featureId=15915f-e16331-f44297-c7d4e0-f2148a4a
     (acquisitionDate>='2022-06-01')AND(cloudCover<0.40)
     (source=WV01)OR(source=WV02)AND(cloudCover<0.40)

1. If no imagery will populate, ensure your CQL filter is not too restrictive and you are zoomed in
closer than 1:150000 over a landmass.

### CQL Filter Builder
![Figure 2](/images/cql.PNG)

The CQL Filter Builder helps users construct syntactically correct CQL Filters. To use it: <br>

1. **Parameter** Select a commonly used filter parameter. For a full list of available parameters, see [CQL Filter Parameters](/ogc/get_filter_parameters)
2. **Operator** Select an available operator.
3. **Value** Enter a value that you want to filter by. <br> <br>
Each Parameter has its own set of possible values. The CQL Filter Builder restricts you from selecting invalid values. For example: <br>
    * **cloudCover** values should be floating point values between 0.0 and 1.0
    * **featureIds** and **legacyIds** must be strings containing letters and numbers.
    * **acquisitionDate** uses the date value from the date widget below the value field and formats it correctly.
4. Select **Build**. The **CQL Filter** field populates with the filter you made. If you see an error message, the filter was invalid.
5. (Optional) To add an additional clause to your filter, click **Add And Clause** or **Add Or Clause**. The **CQL Filter** field will add a clause and format it correctly.
6. (Optional) You may need to adjust the parentheses added by the CQL Filter to achieve your desired results. 
    **For example, the following two queries have different meanings.**

         (source=’WV01’)OR(source=’WV02’)AND(cloudCover<0.40)
         (source=’WV01’)OR((source=’WV02’)AND(cloudCover<0.40))

## Additional Argument 
The additional argument field is for anything you want to add to your WMS/WMTS connection.
Only use this field if you know what you are adding is a valid key value pair for WMS or WMTS connections.

   **Example:**
   
     featureProfile=Vivid_2020
