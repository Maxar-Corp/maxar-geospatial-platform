import unittest
import os
import shutil
import datetime
from MGP_SDK.interface import Interface
import MGP_SDK.process as process


class TestOgcMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()
        self.bbox = "39.84387,-105.05608,39.95133,-104.94827"
        self.featureid = '7144979f-3472-da9b-b2fd-b6b90170c47c'
        self.basemap_filter = "product_name='VIVID_STANDARD_30'"
        self.pwd = os.getcwd()
        self.catalog_id = '10500100325D6D00'

    def test_process(self):
        with self.assertRaises(Exception):
            process._validate_bbox("4830020.1118,-11688476.1480,4831124.2831,-11687253.1555")
        with self.assertRaises(Exception):
            process._validate_bbox('Not a numeric BBox')
        with self.assertRaises(Exception):
            process._validate_bbox(bbox="39.7580,-104.9962,39.7530,-104.9912")  # miny position larger value than max y
        with self.assertRaises(Exception):
            process._validate_bbox("39.7530,-104.9912,39.7580,-104.9962")  # min x position larger than maxx
        with self.assertRaises(Exception):
            process._validate_bbox("-91,-104.9962,39.7580,-104.9912")  # y value outside of range -90:90
        with self.assertRaises(Exception):
            process._validate_bbox("39.7530,-181,39.7580,-104.9912")  # x value outside of range -180:180
        with self.assertRaises(Exception):
            process._validate_bbox('-1,1,1,1,1')  # to long of bbox
        with self.assertRaises(Exception):
            process._check_image_format(img_format='Old timey picture')
        with self.assertRaises(Exception):
            process._check_typeName(typename='I am not your type')
        self.assertEqual(type(process.area_sqkm(self.bbox)), float)  # commented out for story MDS-809 to complete

    def test_streaming_download_image(self):
        result = self.interface.streaming.download_image(bbox=self.bbox, height=400, width=400, img_format='jpeg',
                                                         display=False)
        self.assertIn('Downloaded file', result)
        # exception tests
        with self.assertRaises(Exception):
            self.interface.streaming.download_image(bbox='badbbox')
        with self.assertRaises(Exception):
            self.interface.streaming.download_image(height=8001, width=8001)
        with self.assertRaises(Exception):
            self.interface.streaming.download_image(zoom_level=78)
        with self.assertRaises(Exception):
            self.interface.streaming.download_image(gridoffsets='testoffsets')
        with self.assertRaises(Exception):
            self.interface.streaming.download_image(identifier=self.featureid)

    def test_basemap_download_image(self):
        result = self.interface.basemap_service.download_image(bbox=self.bbox, height=400, width=400, img_format='jpeg',
                                                         display=False)
        self.assertIn('Downloaded file', result)
        # exception tests
        with self.assertRaises(Exception):
            self.interface.basemap_service.download_image(bbox='badbbox')
        with self.assertRaises(Exception):
            self.interface.basemap_service.download_image(height=8001, width=8001)
        with self.assertRaises(Exception):
            self.interface.basemap_service.download_image(zoom_level=78)
        with self.assertRaises(Exception):
            self.interface.basemap_service.download_image(gridoffsets='testoffsets')
        with self.assertRaises(Exception):
            self.interface.basemap_service.download_image(identifier=self.featureid)

    def test_streaming_search(self):
        self.assertEqual(type(self.interface.streaming.search(filter="featureId='{}'".format(self.featureid))), list)
        self.assertEqual(type(self.interface.streaming.search(bbox=self.bbox)), list)
        self.assertEqual(type(self.interface.streaming.search(bbox=self.bbox,
                                                              filter="featureId='{}'".format(self.featureid))), list)
        self.assertEqual(type(self.interface.streaming.search(bbox=self.bbox,
                                                              filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")),
                         list)
        shapefile_search = self.interface.streaming.search(bbox=self.bbox,
                                                           filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)",
                                                           shapefile=True)
        csv_search = self.interface.streaming.search(bbox="39.84387,-105.05608,39.95133,-104.94827",
                                                     filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)",
                                                     csv=True)
        self.assertEqual(type(shapefile_search), str)
        self.assertEqual(type(csv_search), str)
        self.assertTrue(os.path.isfile(shapefile_search))

        with self.assertRaises(Exception):
            self.interface.streaming.search(bbox=self.bbox,
                                            typename='BadTYPENAME')  # bad typename exception  in process.py
        with self.assertRaises(Exception):
            self.interface.streaming.search(bbox=None, filter=None)  # pass in no bbox and no filter in wfs.py
        with self.assertRaises(Exception):
            self.interface.streaming.search(bbox='45, 46, 47, 48, 49',
                                            filter=None)  # trip exception for EPSG 4326 in wfs.py
        with self.assertRaises(Exception):
            self.interface.streaming.search(bbox='181, 46, 47, 48, 49',
                                            filter=None)  # raise exception for bad x coordinates
        with self.assertRaises(Exception):
            self.interface.streaming.search(bbox='45, 91, 47, 48, 49',
                                            filter=None)  # raise exception for bad y coordinates
        with self.assertRaises(Exception):
            self.interface.streaming.search(bbox='cheesburger', filter=None)

    def test_basemap_search(self):
        self.assertEqual(type(self.interface.basemap_service.search(filter=self.basemap_filter, bbox=self.bbox)),
                         list)
        self.assertEqual(type(self.interface.basemap_service.search(bbox=self.bbox)), list)
        shapefile_search = self.interface.basemap_service.search(bbox=self.bbox, filter=self.basemap_filter,
                                                                 shapefile=True)
        csv_search = self.interface.basemap_service.search(bbox="39.84387,-105.05608,39.95133,-104.94827",
                                                           filter=self.basemap_filter, csv=True)
        self.assertEqual(type(shapefile_search), str)
        self.assertEqual(type(csv_search), str)
        self.assertTrue(os.path.isfile(shapefile_search))

        with self.assertRaises(Exception):
            self.interface.basemap_service.search(bbox=self.bbox,
                                            typename='BadTYPENAME')  # bad typename exception  in process.py
        with self.assertRaises(Exception):
            self.interface.basemap_service.search(bbox=None, filter=None)  # pass in no bbox and no filter in wfs.py
        with self.assertRaises(Exception):
            self.interface.basemap_service.search(bbox='45, 46, 47, 48, 49',
                                            filter=None)  # trip exception for EPSG 4326 in wfs.py
        with self.assertRaises(Exception):
            self.interface.basemap_service.search(bbox='181, 46, 47, 48, 49',
                                            filter=None)  # raise exception for bad x coordinates
        with self.assertRaises(Exception):
            self.interface.basemap_service.search(bbox='45, 91, 47, 48, 49',
                                            filter=None)  # raise exception for bad y coordinates
        with self.assertRaises(Exception):
            self.interface.basemap_service.search(bbox='cheesburger', filter=None)

    def test_streaming_full_image(self):
        download = self.interface.streaming.get_full_res_image(featureid=self.featureid, outputdirectory=self.pwd)
        self.assertEqual(type(download), str)
        self.assertIn("Finished full image download process, output directory is:", download)
        self.assertTrue(os.path.isfile(os.path.join(self.pwd, 'Maxar_Image', "Grid_cell_coordinates.txt")))

    def test_streaming_full_image_bbox(self):
        download = self.interface.streaming.get_full_res_image(featureid=self.featureid, bbox=self.bbox,
                                                               outputdirectory=self.pwd)
        self.assertEqual(type(download), str)
        self.assertIn("Finished full image download process, output directory is:", download)
        self.assertTrue(os.path.isfile(os.path.join(self.pwd, 'Maxar_Image', "Grid_cell_coordinates.txt")))

    def test_streaming_full_image_bbox_mosaic(self):
        # Need a check to see when the file doesn't fully download and retry
        download = self.interface.streaming.get_full_res_image(featureid=self.featureid, bbox=self.bbox, mosaic=True,
                                                               outputdirectory=self.pwd)
        self.assertEqual(type(download), str)
        self.assertIn("Finished full image download process, output directory is:", download)
        self.assertTrue(os.path.isfile(os.path.join(self.pwd, 'merged_image.jpeg')))

    # TODO waiting on browse functionality from Xpress
    # def test_streaming_browse(self):
    #     image = self.interface.streaming.download_browse_image(self.featureid)
    #     self.assertIn("Downloaded file", image)
    #     self.assertTrue(os.path.isfile(os.path.join(self.pwd, 'Download.jpeg')))
    #     with self.assertRaises(Exception):
    #         self.interface.streaming.download_browse_image(input_id='Im a bad ID arent I?')
    #     with self.assertRaises(Exception):
    #         self.interface.streaming.download_browse_image(input_id=self.featureid, img_format='BadFMT')

    def test_streaming_wmts(self):
        tiles = self.interface.streaming.get_tile_list_with_zoom(bbox=self.bbox, zoom_level=13)
        self.assertEqual(type(tiles), list)
        tile_download = self.interface.streaming.download_tiles(bbox=self.bbox, zoom_level=13)
        self.assertIn("Download complete", tile_download)
        with self.assertRaises(Exception):
            self.interface.streaming.get_tile_list_with_zoom(bbox='Not a BBOX', zoom_level=13)
        with self.assertRaises(Exception):
            # bad zoom level for get tiles
            self.interface.streaming.get_tile_list_with_zoom(bbox=self.bbox,
                                                             zoom_level=8000)
        # this exception doesn't work currently
        with self.assertRaises(Exception):
            # bad image format
            self.interface.streaming.download_tiles(bbox=self.bbox, zoom_level=13, img_format='screenshot')
        with self.assertRaises(Exception):
            # bad zoom level for download
            self.interface.streaming.download_tiles(bbox=self.bbox, zoom_level=8000)

    def test_basemap_wmts(self):
        tiles = self.interface.basemap_service.get_tile_list_with_zoom(bbox=self.bbox, zoom_level=13)
        self.assertEqual(type(tiles), list)
        tile_download = self.interface.basemap_service.download_tiles(bbox=self.bbox, zoom_level=13)
        self.assertIn("Download complete", tile_download)
        with self.assertRaises(Exception):
            self.interface.basemap_service.get_tile_list_with_zoom(bbox='Not a BBOX', zoom_level=13)
        with self.assertRaises(Exception):
            # bad zoom level for get tiles
            self.interface.basemap_service.get_tile_list_with_zoom(bbox=self.bbox, zoom_level=8000)
        # bad image format
        with self.assertRaises(Exception):
            self.interface.streaming.download_tiles(bbox=self.bbox, zoom_level=13, img_format='screenshot')
        with self.assertRaises(Exception):
            # bad zoom level for download
            self.interface.streaming.download_tiles(bbox=self.bbox, zoom_level=8000)

    def tearDown(self):
        for file in os.listdir(os.getcwd()):
            if 'Download' in file or 'merged_image' in file:
                os.remove(os.path.join(os.getcwd(), file))
        if os.path.isdir(os.path.join(self.pwd, 'Maxar_Image')):
            shutil.rmtree(os.path.join(self.pwd, 'Maxar_Image'))


class TestAccountServiceMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()
        self.test_client_id = 'f924d13f-81f1-4e72-aa8b-93979c3d8112'

    def test_account_usage(self):
        self.assertTrue(type(self.interface.account_service.usage.get_account_usage()), dict)
        with self.assertRaises(ValueError):
            self.interface.account_service.usage.get_account_usage(pageSize=0)
        with self.assertRaises(Exception):
            self.interface.account_service.usage.get_account_usage(sortBy='not_a_real_sort')
        self.assertTrue(type(self.interface.account_service.usage.get_activation_usage()), dict)
        with self.assertRaises(ValueError):
            self.interface.account_service.usage.get_activation_usage(pageSize=0)
        with self.assertRaises(Exception):
            self.interface.account_service.usage.get_activation_usage(sortBy='not_a_real_sort')
        self.assertTrue(type(self.interface.account_service.usage.get_user_usage()), dict)
        with self.assertRaises(ValueError):
            self.interface.account_service.usage.get_user_usage(pageSize=0)
        with self.assertRaises(Exception):
            self.interface.account_service.usage.get_user_usage(sortBy='not_a_real_sort')


class TestAuthMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()

    def test_bad_auth(self):
        user_name = 'ThisIsABadUsername'
        password = 'ThisIsABadPassword'

        # Test incorrect username/password
        with self.assertRaises(Exception):
            self.interface.auth(user_name, password)

        # Test incorrect format of file
        if os.path.isfile(os.path.join(os.path.expanduser('~'), '.MGP-config')):
            file_name = os.path.join(os.path.expanduser('~'), '.MGP-config')
            os.rename(file_name, file_name.split('.')[0] + '.MGP-config-old')

        with open(os.path.join(os.path.expanduser('~'), '.MGP-config'), 'w+') as f:
            f.write('user_name={}\n'.format(user_name))
            f.write('user_password={}\n'.format(password))
        with self.assertRaises(Exception):
            self.interface.auth()
        os.remove(os.path.join(os.path.expanduser('~'), '.MGP-config'))

        if os.path.isfile(os.path.join(os.path.expanduser('~'), '.MGP-config-old')):
            file_name = os.path.join(os.path.expanduser('~'), '.MGP-config-old')
            os.rename(file_name, file_name.split('.')[0] + '.MGP-config')


class TestDiscoveryServiceMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface().discovery_service
        self.bbox = '-105,40,-104,41'
        self.datetime = '2015-01-01T00:00:00Z/2016-01-01T00:00:00Z'
        self.sub_catalog_id = 'dg-archive'
        self.collections = 'wv01'
        self.where = 'eo:cloud_cover < 20'
        self.orderby = 'id'
        self.audit_date = '2023-03-12T00:00:00Z/2023-03-15T12:31:12Z'
        self.stac_id = '160623e2-69dd-4aba-9354-a6d685d28190-inv'
        self.id_list = '0d1e2b78-aeb0-493e-b046-561265c6735b-inv, 385c2a01-d880-4662-9bef-adde996cf810-inv'
        self.intersects = {"type": "Polygon", "coordinates":
            [[[-105, 39], [-103, 39], [-103, 41], [-104, 41], [-104, 40], [-105, 40], [-105, 39]]]}

    def test_stac_search(self):
        stac_search_with_filtering = self.interface.stac_search(bbox=self.bbox, datetime=self.datetime,
                                                                collections=self.collections, where=self.where,
                                                                orderby=self.orderby)
        search_stac_by_id = self.interface.stac_search(ids=self.stac_id)
        search_stac_by_ids = self.interface.stac_search(ids=self.id_list)
        search_stac_in_sub_catalog = self.interface.stac_search(sub_catalog_id=self.sub_catalog_id, bbox=self.bbox,
                                                                where=self.where)
        search_sub_catalog_collections = self.interface.stac_search(sub_catalog_id=self.sub_catalog_id,
                                                                    collections=self.collections, bbox=self.bbox,
                                                                    where=self.where)
        search_stac_by_audit_fields1 = self.interface.search_by_audit_fields(collection_id=self.collections,
                                                                             audit_insert_date=self.audit_date,
                                                                             limit=10)
        search_stac_by_audit_fields2 = self.interface.search_by_audit_fields(collection_id=self.collections,
                                                                             audit_update_date=self.audit_date,
                                                                             limit=10)
        get_single_stac = self.interface.stac_search(ids=self.stac_id)
        self.assertTrue(type(get_single_stac), 'list')
        self.assertTrue(type(stac_search_with_filtering), 'dict')
        self.assertTrue(type(stac_search_with_filtering), 'dict')
        self.assertTrue(type(search_stac_by_id), 'dict')
        self.assertTrue(type(search_stac_by_ids), 'dict')
        self.assertTrue(type(search_stac_in_sub_catalog), 'dict')
        self.assertTrue(type(search_sub_catalog_collections), 'dict')
        # self.assertTrue(type(search_stac_by_audit_fields1), 'list')
        # self.assertTrue(type(search_stac_by_audit_fields2), 'list')

        # bbox and intersects exception
        with self.assertRaises(Exception):
            self.interface.stac_search(bbox=self.bbox, intersects=self.intersects)
        # bad datetime
        with self.assertRaises(Exception):
            self.interface.stac_search(datetime='12345')
        # both audit fields
        with self.assertRaises(Exception):
            self.interface.search_by_audit_fields(audit_insert_date=self.audit_date, audit_update_date=self.audit_date)

    def test_catalog_checks(self):
        self.assertTrue(type(self.interface.get_root_catalog()), 'dict')
        self.assertTrue(type(self.interface.get_top_level_sub_catalog()), 'dict')
        self.assertTrue(type(self.interface.get_sub_catalog(sub_catalog_id=self.sub_catalog_id)), 'dict')
        self.assertTrue(type(self.interface.get_all_sub_catalog_collections(sub_catalog_id=self.sub_catalog_id)), 'dict')
        self.assertTrue(type(self.interface.get_sub_catalog_collection_definition(sub_catalog_id=self.sub_catalog_id,
                                                                                  sub_catalog_collection_id='wv04'),
                             ), 'dict')
        self.assertTrue(type(self.interface.get_specifications()), 'dict')
        self.assertTrue(type(self.interface.healthcheck()), 'dict')
        self.assertTrue(type(self.interface.get_status()), 'dict')



class TestMonitorServiceMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()

    def test_monitor(self):
        time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(minutes=15, days=1)
        end_time = time.isoformat()
        now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(days=1)
        now_time = now.isoformat()
        monitor = self.interface.monitoring_service. \
            new_monitor(source="discovery/catalog", start_datetime=now_time, end_datetime=end_time,
                        description="Marianas test monitor for sdk", aoi_geojson={"type": "Polygon", "coordinates": [
                            [
                                [-106.8, 35.1], [-106.4, 35.1], [-106.4, 35.4], [-106.8, 35.4], [-106.8, 35.1]
                            ]
                        ]
                                    },
                        match_criteria={"platform": {"in": ["worldview-03", "worldview-02"]},
                                        "eo:cloud_cover": {"lt": 75},
                                        "aoi:coverage_sqkm": {"gte": 1}},
                        monitor_notifications=[{"type": "email", "target": "myemail@mymail.com"}])
        monitor_id = monitor['data']['id']
        self.assertTrue(type(monitor_id), dict)
        self.assertTrue(type(self.interface.monitoring_service.get_monitor(monitor_id)), dict)
        if self.interface.monitoring_service.get_monitor(monitor_id)['data']['enabled']:
            self.assertTrue(type(self.interface.monitoring_service.toggle_monitor_status(monitor_id, 'disable')),
                            dict)
        # Enabling feature commented out, no way to enable a monitor with this type of test. Enabling can only be done
        # on disabled monitors that have an end_datetime in the future. Monitors cannot be created in the past and
        # cannot be set as enabled with a start_datetime in the future
        # else:
        #     self.assertTrue(type(self.interface.monitoring_service.toggle_monitor_status(monitor_id, 'enable')),
        #                     dict)
        self.assertTrue(type(self.interface.monitoring_service.get_monitor_list()), dict)
        self.assertTrue(type(self.interface.monitoring_service.get_monitor_events(monitor_id)), dict)

    # def test_tasking(self):
    #     tasking = self.interface.tasking_service.new_tasking("2023-06-18T00:00:00+00:00",
    #                                                          "2023-09-18T00:00:00+00:00",
    #                                                          {"type": "Polygon", "coordinates": [
    #                                                              [
    #                                                                  [-106.8, 35.1], [-106.4, 35.1], [-106.4, 35.4],
    #                                                                  [-106.8, 35.4], [-106.8, 35.1]
    #                                                              ]
    #                                                          ]
    #                                                           },
    #                                                          "50cm_Color",
    #                                                          max_cloud_cover=.5,
    #                                                          max_collect_gsd=1,
    #                                                          max_off_nadir_angle=50,
    #                                                          max_sun_elevation_angle=50)
    #     self.assertTrue(type(tasking), dict)
    #     self.assertTrue(type(self.interface.tasking_service.get_tasking_request(tasking['id'])), dict)
    #     self.assertTrue(type(self.interface.tasking_service.tasking_list()), dict)
    #     self.assertTrue(type(self.interface.tasking_service.cancel_tasking(tasking['id'], 'sdk test')), dict)


class TestOrderingServiceMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()
        self.test_user_id = 'f:63a7af62-7902-4925-9382-3d920450a524:24'
        self.test_order_id = ''

    # Need proper schema for pipeline specific settings
    def test_order(self):
        namespace = 'imagery'
        pipeline = 'map-ready'
        output_config = {"output_config": {"amazon_s3": {"bucket": "ard-ordering-test", "prefix": "marianas-script"}}}
        settings = {
            "settings": {
                "inventory_ids": ["03cf5011-7fd0-49ab-8bcf-36d7e2a1075f-inv"],
                "customer_description": "Marianas_smoke_test"
            }
        }
        notifications = [{"type": "email", "target": "DL-GCS-Marianas-Team@maxar.com", "level": "FINAL_ONLY"}]
        metadata = {"metadata": {"project_id": "marianas_script_order_test"}}
        order = self.interface.order_service.place_order(namespace, pipeline, output_config=output_config,
                                                         settings=settings, notifications=notifications,
                                                         metadata=metadata, validate=False)
        self.assertTrue(type(order), dict)
        orders = self.interface.order_service.get_user_orders(self.test_user_id)
        self.assertTrue(type(orders), dict)
        order_id = [i['id'] for i in orders['data']['orders'] if i['pipeline_id'] == 'imagery/map-ready'][0]
        self.assertTrue(order_id)
        order_details = self.interface.order_service.get_order_details(order_id)
        self.assertTrue(type(order_details), dict)
        self.assertTrue(order_details['data'])
        pipeline_details = self.interface.order_service.get_pipeline_details('imagery', 'map-ready')
        self.assertTrue(type(pipeline_details), dict)
        self.assertTrue(pipeline_details['data'])

        self.assertTrue(type(self.interface.order_service.get_usage_estimate(namespace, pipeline, settings=settings,
                                                                             output_config=output_config,
                                                                             metadata=metadata)), dict)
        self.assertTrue(type(self.interface.order_service.get_order_events(order_id)), dict)
        self.assertTrue(type(self.interface.order_service.cancel_order(order_id)), dict)
        # pipeline_no_cancel = 'analysis-ready'
        # settings_no_cancel = {
        #     "settings": {
        #         "acquisitions": [{"id": "03cf5011-7fd0-49ab-8bcf-36d7e2a1075f-inv"}],
        #         "bbox": [47.8,29.25,47.81,29.27],
        #         "ard_settings": {"bundle_adjust": False, "healthy_vegetation_mask": False, "water_mask": False}
        #     }
        # }
        # order_no_cancel = self.interface.order_service.place_order(namespace, pipeline_no_cancel,
        #                                                            output_config=output_config,
        #                                                            settings=settings_no_cancel,
        #                                                            notifications=notifications, metadata=metadata,
        #                                                            validate=False)
        # self.assertTrue(type(order_no_cancel), dict)
        # orders_no_cancel = self.interface.order_service.get_my_orders(self.test_user_id)
        # order_id_no_cancel = [i['id'] for i in orders_no_cancel['data']['orders']][0]
        # self.assertTrue(order_id_no_cancel)
        # with self.assertRaises(Exception):
        #     self.interface.order_service.cancel_order(order_id_no_cancel)


class TestTaskingServiceMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()

    def test_tasking(self):
        template = [{
                "pipeline": "imagery/analysis-ready",
                "template": {
                    "settings": {
                        "acquisitions": [{
                            "id": "$.id"
                        }],
                        "intersects": "$._aoi_geojson",
                        "ard_settings": {
                            "bundle_adjust": True, "healthy_vegetation_mask": False, "water_mask": False
                        }
                    },
                    "output_config": {
                        "amazon_s3": {
                            "bucket": "ard-ordering-test",
                            "prefix": "marianas-script"
                        }
                    },
                    "notifications": [{
                        "type": "email",
                        "target": "DL-GCS-Marianas-Team@maxar.com",
                        "level": "INITIAL_FINAL"
                    }],
                    "metadata": {
                        "project_id": "marianas_SDK_tasking_test"
                    }
                }
            }]
        tasking = self.interface.tasking_service.new_tasking(start_datetime="2023-06-18T00:00:00+00:00",
                                                             end_datetime="2023-09-18T00:00:00+00:00",
                                                             aoi_geojson={"type": "Polygon", "coordinates": [
                                                                 [
                                                                     [-105.024490, 39.675484],
                                                                     [-104.867935, 39.675484],
                                                                     [-104.867935, 39.784268],
                                                                     [-105.024490, 39.784268],
                                                                     [-105.024490, 39.675484]
                                                                 ]
                                                             ]
                                                              },
                                                             recipe="50cm_Color",
                                                             order_templates=template)
        tasking_id = tasking['data']['id']
        self.assertTrue(type(tasking_id), dict)
        self.assertTrue(type(self.interface.tasking_service.get_tasking_request(tasking_id)), dict)
        self.assertTrue(type(self.interface.tasking_service.tasking_list()), dict)
        self.assertTrue(type(self.interface.tasking_service.cancel_tasking(tasking_id, 'sdk test')), dict)


class TestThreeDMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()
        self.bbox = "39.84387,-105.05608,39.95133,-104.94827"

    # n3D not live yet
    # def test_3d(self):
    #     self.assertEqual(type(self.interface.three_d.get_capabilites()), dict)
    #
    #     self.assertEqual(type(self.interface.three_d.get_coverage(self.bbox)), dict)
    #
    #     layer_name = ""
    #     self.assertEqual(type(self.interface.three_d.get_layer_tileset_3d(layer_name)), dict)


class TestTokenServiceMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()
        self.test_name = 'Marianas_test'

    def test_token(self):
        self.assertEqual(type(self.interface.token.get_user_tokens()), list)

        description = 'this is a test of the token service'
        token = self.interface.token.create_token_record(name=self.test_name, description=description)
        self.assertEqual(type(token), dict)

        delete_token = self.interface.token.delete_tokens(token['id'])
        self.assertIn('204', delete_token)


class TestUsageServiceMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()

    def test_usage(self):
        self.assertIn('Usage is allowed', self.interface.usage_service.check_usage_is_allowed())

        # Activation usage endpoint not up yet
        # self.assertTrue(type(self.interface.usage_service.get_usage_by_activation(activation)), dict)
        # Usage overview currently returns 500
        # self.assertTrue(type(self.interface.usage_service.get_usage_overview()), dict)

class TestAnalyticsServiceMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()
        self.scriptId = 'ac1fd96964ebf2acaeb5fbb7358f44cd6a664da1c898dca36c8c741761557958'
        self.bbox = "39.84387,-105.05608,39.95133,-104.94827"
        self.bbox_3857 = "4851060.1776836105,-11712956.404248431,4870628.056924616,-11693388.525007427"
        self.layer = "layer_pcm_eo_2010"
    # def test_get_image_metadata_raster(self):
    #     self.assertEqual(type(self.interface.analytics.get_image_metadata_raster(function='pansharp',script_id=str(self.scriptId),)),dict)
    # def test_get_byte_range_raster(self):
    #     self.assertEqual(type(self.interface.analytics.get_byte_range_raster(function='pansharp',script_id=str(self.scriptId))),dict)
    def test_search_vector_layer(self):
        result = self.interface.analytics.search_vector_layer(layers=self.layer,bbox=self.bbox_3857, srsname="EPSG:3857")
        self.assertEqual(type(result),list)
    def test_get_vector_analytics_layer(self):
        result = self.interface.analytics.download_vector_analytics(layers=self.layer, bbox=self.bbox_3857, srsname="EPSG:3857", height=512, width=512)
        self.assertIn('Downloaded file', result)
    def tearDown(self):
        for file in os.listdir(os.getcwd()):
            if 'Download' in file:
                os.remove(os.path.join(os.getcwd(), file))

class TestAuthFunctions(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()

    def test_token_service_token(self):
        get_token = self.interface.auth.token_service_token()
        self.assertEqual(type(get_token), dict)
        id_of_token = get_token["id"]
        import requests
        url = f"{self.interface.auth.api_base_url}/token-service/api/{self.interface.auth.api_version}/token/id/{id_of_token}"
        headers = {"Authorization": f"Bearer {self.interface.auth.access}"}
        delete = requests.request("DELETE", url, headers=headers)

        self.assertTrue(type(self.interface.usage_service.get_usage_overview()), dict)

# class TestAnalyticsServiceMethods(unittest.TestCase):
#     def setUp(self):
#         self.interface = Interface()
#         self.scriptId = 'ac1fd96964ebf2acaeb5fbb7358f44cd6a664da1c898dca36c8c741761557958'
#         self.bbox = "39.84387,-105.05608,39.95133,-104.94827"
#         self.bbox_3857 = "4851060.1776836105,-11712956.404248431,4870628.056924616,-11693388.525007427"
#         self.layer = "layer_pcm_eo_2010"
#     def test_get_image_metadata_raster(self):
#         self.assertEqual(type(self.interface.analytics.get_image_metadata_raster(function='pansharp',script_id=str(self.scriptId),)),dict)
#     def test_get_byte_range_raster(self):
#         self.assertEqual(type(self.interface.analytics.get_byte_range_raster(function='pansharp',script_id=str(self.scriptId))),dict)
#     def test_search_vector_layer(self):
#         result = self.interface.analytics.search_vector_layer(layers=self.layer,bbox=self.bbox_3857, srsname="EPSG:3857")
#         self.assertEqual(type(result),list)
#     def test_get_vector_analytics_layer(self):
#         result = self.interface.analytics.download_vector_analytics(layers=self.layer, bbox=self.bbox_3857, srsname="EPSG:3857", height=512, width=512)
#         self.assertIn('Downloaded file', result)
#     def tearDown(self):
#         for file in os.listdir(os.getcwd()):
#             if 'Download' in file:
#                 os.remove(os.path.join(os.getcwd(), file))
class TestProcessMethods(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()


if __name__ == '__main__':
    unittest.main()
