import unittest
import shutil
import MGP_SDK.cli_commands.cli_commands
from click.testing import CliRunner
import os
import ast
import datetime


class Auth_cli_functions(unittest.TestCase):

    def setUp(self):
        self.commands = MGP_SDK.cli_commands.cli_commands
        self.runner = CliRunner()

    def test_home_dir(self):
        print("test_home_dir: starting")
        result = self.runner.invoke(self.commands.home_dir)
        assert result.exit_code == 0
        print("test_home_dir: finished")

    def test_create_token(self):
        print("test_create_token: starting")
        result = self.runner.invoke(self.commands.create_token, args=['--name', 'CLI_testing_suite', '--description', 'Testing Suite'], input='y\n')
        print(result.output)
        assert "Token created" in result.output
        assert result.exit_code == 0
        print("test_create_token: done")

    def test_d_get_tokens(self):
        print("test_get_tokens: starting")
        result = self.runner.invoke(self.commands.get_tokens)
        print(result.output)
        new_token = [i for i in ast.literal_eval(result.output) if i['name'] == "CLI_testing_suite"]
        assert len(new_token) == 1
        assert result.exit_code == 0
        print("test_get_tokens: done")


    def test_delete_tokens(self):
        print("test_delete_tokens: starting")
        tokens = self.runner.invoke(self.commands.get_tokens)
        all_tokens = ast.literal_eval(tokens.output)
        delete = [i for i in all_tokens if i['name'] == "CLI_testing_suite"]
        delete_id = [i['id'] for i in delete]
        result = self.runner.invoke(self.commands.delete_tokens, args=['--token_id', delete_id[0]], input='y\n')
        print(result.output)
        assert "Token successfully deleted" in result.output
        assert result.exit_code == 0
        print("test_delete_tokens: done")


class Streaming_cli_functions(unittest.TestCase):

    def setUp(self):
        self.commands = MGP_SDK.cli_commands.cli_commands
        self.runner = CliRunner()
        self.bbox = "39.746196,-104.954672,39.747858,-104.951625"
        self.full_res_bbox = "39.743791,-104.959645,39.754449,-104.940934"
        self.feature = 'a9b9cbda-fb1f-64a4-eb2c-f954265dfa3e'
        self.pwd = os.getcwd()


    def test_search(self):
        print("test_search: starting")
        result = self.runner.invoke(self.commands.search, args=['--bbox', self.bbox, '--default'])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_search: done")


    def test_download_image(self):
        print("test_download_image: starting")
        result = self.runner.invoke(self.commands.download, args=['--bbox', self.bbox, '--zoom_level', 17,
                                                                  '--img_format', 'jpeg', '--outputpath',
                                                                  os.path.join(self.pwd, "CLI_download.jpeg"),
                                                                  '--default'])
        print(result.output)
        self.assertIn('Download complete', result.output)
        assert result.exit_code == 0
        print("test_download_image: done")


    def test_get_tile_list(self):
        print("test_get_tile_list: starting")
        result = self.runner.invoke(self.commands.get_tile_list, args=['--bbox', self.bbox, '--zoom', 17, '--yes'])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_get_tile_list: done")


    def test_download_tiles(self):
        print("test_download_tiles: starting")
        result = self.runner.invoke(self.commands.download_tiles, args=[
            '--bbox', self.bbox, '--zoom', 17, '--outputpath', os.path.join(self.pwd, 'cli_test.jpeg'), '--yes'
        ])
        print(result.output)
        self.assertIn('Download complete', result.output)
        assert result.exit_code == 0
        print("test_download_tiles: done")


    def test_download_by_pixel_count(self):
        print("test_download_by_pixel_count: starting")
        result = self.runner.invoke(self.commands.download_by_pixel_count, args=[
            '--bbox', self.bbox, '--height', 512, '--width', 512, '--outputpath', os.path.join(
                self.pwd, 'cli_test.jpeg'), '--yes'
        ])
        print(result.output)
        self.assertIn('Downloaded file', result.output)
        self.assertTrue(os.path.isfile(os.path.join(self.pwd, "cli_test.jpeg")))
        assert result.exit_code == 0
        print("test_download_by_pixel_count: done")


    def test_full_res_image(self):
        print("test_full_res_image: starting")
        result = self.runner.invoke(self.commands.full_res_image, args=[
            '--featureid', self.feature, '--bbox', self.full_res_bbox, '--outputdirectory', self.pwd, '--mosaic', '--yes'
        ])
        print(result.output)
        self.assertIn("Finished full image download process, output directory is:", result.output)
        self.assertTrue(os.path.isfile(os.path.join(self.pwd, 'Maxar_Image', "Grid_cell_coordinates.txt")))
        assert result.exit_code == 0
        print("test_full_res_image: done")


    def test_calculate_bbox(self):
        print("test_calculate_bbox: starting")
        result = self.runner.invoke(self.commands.calculate_bbox_sqkm, args=['--bbox', self.bbox], input='n\n')
        print(result.output)
        self.assertIn("Square kilometers of bbox is:", result.output)
        assert result.exit_code == 0
        print("test_calculate_bbox: done")

    def tearDown(self):
        if os.path.isdir(os.path.join(self.pwd, 'Maxar_Image')):
            shutil.rmtree(os.path.join(self.pwd, 'Maxar_Image'))
        for file in os.listdir(os.getcwd()):
            if ".py" not in file:
                os.remove(os.path.join(os.getcwd(), file))


class Admin_cli_functions(unittest.TestCase):

    def setUp(self):
        self.commands = MGP_SDK.cli_commands.cli_commands
        self.runner = CliRunner()


    def test_get_accounts(self):
        print("test_get_accounts: starting")
        result = self.runner.invoke(self.commands.get_accounts)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_get_accounts: done")


    def test_account_roles(self):
        print("test_account_roles: starting")
        result = self.runner.invoke(self.commands.account_roles)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_account_roles: done")


    def test_account_comments(self):
        print("test_account_comments: starting")
        result = self.runner.invoke(self.commands.account_comments, args=['--account_id', 2])
        assert result.exit_code == 0
        print("test_account_comments: done")


    def test_get_activations(self):
        print("test_get_activations: starting")
        result = self.runner.invoke(self.commands.get_activations)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_get_activations: done")


    def test_activations_for_account(self):
        print("test_activations_for_account: starting")
        result = self.runner.invoke(self.commands.activations_for_account, args=['--account_id', 2])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_activations_for_account: done")


    def test_activation_credit_limit(self):
        print("test_activation_credit_limit: starting")
        result = self.runner.invoke(self.commands.activation_credit_limit, args=['--activation_number', "ACT-6142411"])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_activation_credit_limit: done")


    def test_activation_types(self):
        print("test_activation_types: starting")
        result = self.runner.invoke(self.commands.activation_types)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_activation_types: done")


    def test_get_products(self):
        print("test_get_products: starting")
        result = self.runner.invoke(self.commands.get_products)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_get_products: done")


    def test_product_filter(self):
        print("test_product_filter: starting")
        result = self.runner.invoke(self.commands.product_filter, args=['--usage_type', 'Streaming'])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_product_filter: done")


    def test_get_rate_table(self):
        print("test_get_rate_table: starting")
        result = self.runner.invoke(self.commands.get_rate_table, args=['--table_id', 115])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_get_rate_table: done")


    def test_get_activation_for_table(self):
        print("test_get_activation_for_table: starting")
        result = self.runner.invoke(self.commands.get_activation_for_table, args=['--table_id', 115])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_get_activation_for_table: done")


    def test_get_credit_types(self):
        print("test_get_credit_types: starting")
        result = self.runner.invoke(self.commands.get_credit_types)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_get_credit_types: done")


    def test_get_rate_amounts(self):
        print("test_get_rate_amounts: starting")
        result = self.runner.invoke(self.commands.get_rate_amounts, args=['--table_id', 115])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_get_rate_amounts: done")


    def test_get_table_and_activations(self):
        print("test_get_table_and_activations: starting")
        result = self.runner.invoke(self.commands.get_table_and_activations)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_get_table_and_activations: done")


    def test_get_roles(self):
        print("test_get_roles: starting")
        result = self.runner.invoke(self.commands.get_roles)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_get_roles: done")


    def test_user_types(self):
        print("test_user_types: starting")
        result = self.runner.invoke(self.commands.user_types)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_user_types: done")


    def test_get_users(self):
        print("test_get_users: starting")
        result = self.runner.invoke(self.commands.get_users)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_get_users: done")


    def test_create_user(self):
        print("test_create_user: starting")
        result = self.runner.invoke(self.commands.create_user, args=[
            '--user_type', 'BASE_USER', '--account_id', 893, '--activation_id', 914, '--email',
            'marianas_cli_test_user@maxar.com', '--first_name', 'marianas', '--last_name', 'cli_test', '--country',
            'United States of America'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        self.assertIn("marianas_cli_test_user@maxar.com", result.output)
        assert result.exit_code == 0
        print("test_create_user: done")


    def test_update_user(self):
        print("test_update_user: starting")
        users = self.runner.invoke(self.commands.get_users, args=['--page_size', 2000])
        all_users = ast.literal_eval(users.output)
        test_user = [i['userId'] for i in all_users['users'] if i['username'] == "marianas_cli_test_user@maxar.com"]
        result = self.runner.invoke(self.commands.update_user, args=['--user_id', test_user[0], '--first_name', 'marianasupdate', '--yes'])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        self.assertIn("marianasupdate", result.output)
        assert result.exit_code == 0
        print("test_update_user: done")


    def test_update_user_roles(self):
        print("test_update_user_roles: starting")
        users = self.runner.invoke(self.commands.get_users, args=['--page_size', 2000])
        all_users = ast.literal_eval(users.output)
        test_user = [i['userId'] for i in all_users['users'] if i['username'] == "marianas_cli_test_user@maxar.com"]
        result_add = self.runner.invoke(self.commands.update_user_roles, args=['--user_id', test_user[0], '--roles', "DAILY_TAKE"])
        print(result_add.output)
        self.assertEqual(type(ast.literal_eval(result_add.output)), list)
        assert result_add.exit_code == 0
        result_delete = self.runner.invoke(self.commands.update_user_roles, args=['--user_id', test_user[0], '--roles', "DAILY_TAKE", '--delete'])
        print(result_delete.output)
        self.assertIn("Response [200]", result_delete.output)
        assert result_delete.exit_code == 0
        print("test_update_user_roles: done")


    def test_get_user_roles(self):
        print("test_get_user_roles: starting")
        users = self.runner.invoke(self.commands.get_users, args=['--page_size', 2000])
        all_users = ast.literal_eval(users.output)
        test_user = [i['userId'] for i in all_users['users'] if i['username'] == "marianas_cli_test_user@maxar.com"]
        result = self.runner.invoke(self.commands.get_user_roles, args=['--user_id', test_user[0]])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_get_user_roles: done")


    def test_get_user_available_roles(self):
        print("test_get_user_available_roles: starting")
        users = self.runner.invoke(self.commands.get_users, args=['--page_size', 2000])
        all_users = ast.literal_eval(users.output)
        test_user = [i['userId'] for i in all_users['users'] if i['username'] == "marianas_cli_test_user@maxar.com"]
        result = self.runner.invoke(self.commands.get_user_available_roles, args=['--user_id', test_user[0]])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_get_user_available_roles: done")


    def test_z_delete_user(self):
        print("test_delete_user: starting")
        users = self.runner.invoke(self.commands.get_users, args=['--page_size', 2000])
        all_users = ast.literal_eval(users.output)
        test_user = [i['userId'] for i in all_users['users'] if i['username'] == "marianas_cli_test_user@maxar.com"]
        result = self.runner.invoke(self.commands.delete_user, args=['--user_id', test_user[0], '--yes'])
        print(result.output)
        self.assertIn("User {} successfully deleted".format(test_user[0]), result.output)
        assert result.exit_code == 0
        print("test_delete_user: done")


class Usage_cli_functions(unittest.TestCase):

    def setUp(self):
        self.commands = MGP_SDK.cli_commands.cli_commands
        self.runner = CliRunner()


    def test_account_usage(self):
        print("test_account_usage: starting")
        result = self.runner.invoke(self.commands.account_usage, args=['--page_size', 5])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_account_usage: done")


    def test_activation_usage(self):
        print("test_activation_usage: starting")
        result = self.runner.invoke(self.commands.activation_usage, args=['--page_size', 5])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_activation_usage: done")


    def test_user_usage(self):
        print("test_user_usage: starting")
        result = self.runner.invoke(self.commands.user_usage, args=['--page_size', 5])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_user_usage: done")


    def test_usage_is_allowed(self):
        print("test_usage_is_allowed: starting")
        result = self.runner.invoke(self.commands.usage_is_allowed)
        print(result.output)
        self.assertIn("Usage is allowed", result.output)
        assert result.exit_code == 0
        print("test_usage_is_allowed: done")


    def test_usage_overview(self):
        print("test_usage_overview: starting")
        result = self.runner.invoke(self.commands.usage_overview)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_usage_overview: done")


class Discovery_cli_functions(unittest.TestCase):

    def setUp(self):
        self.commands = MGP_SDK.cli_commands.cli_commands
        self.runner = CliRunner()

    def test_stac_search(self):
        print("test_stac_search: starting")
        result = self.runner.invoke(self.commands.stac_search, args=[
            '--collections', 'wv02', '--bbox', "-104.954672,39.746196,-104.951625,39.747858", '--where',
            'eo:cloud_cover<20', '--orderby', 'id', '--limit', 5, '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_stac_search: done")


    def test_search_audit_fields(self):
        print("test_search_audit_fields: starting")
        result = self.runner.invoke(self.commands.search_audit_fields, args=[
            '--collection_id', 'wv01', '--audit_insert_date', '2023-03-12T00:00:00Z/2023-03-18T12:31:12Z'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), list)
        assert result.exit_code == 0
        print("test_search_audit_fields: done")


    def test_root_catalog(self):
        print("test_root_catalog: starting")
        result = self.runner.invoke(self.commands.root_catalog)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_root_catalog: done")


    def test_collection_definition(self):
        print("test_collection_definition: starting")
        result = self.runner.invoke(self.commands.collection_definition, args=['--collection_id', 'wv01'])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_collection_definition: done")


    def test_all_collections(self):
        print("test_all_collections: starting")
        result = self.runner.invoke(self.commands.all_collections, args=['--limit', 5])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_all_collections: done")


    def test_get_stac_item(self):
        print("test_get_stac_item: starting")
        item = self.runner.invoke(self.commands.stac_search, args=[
            '--collections', 'wv02', '--bbox', "-104.954672,39.746196,-104.951625,39.747858", '--where',
            'eo:cloud_cover<20', '--orderby', 'id', '--limit', 5, '--yes'
        ])
        item_id = [i['id'] for i in ast.literal_eval(item.output)['features']]
        result = self.runner.invoke(self.commands.get_stac_item, args=[
            '--collection_id', 'wv02', '--item_id', item_id[0]
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_get_stac_item: done")


    def test_top_level_sub_catalog(self):
        print("test_top_level_sub_catalog: starting")
        result = self.runner.invoke(self.commands.top_level_sub_catalog, args=['--limit', 5])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_top_level_sub_catalog: done")


    def test_sub_catalog_definition(self):
        print("test_sub_catalog_definition: starting")
        result = self.runner.invoke(self.commands.sub_catalog_definition, args=['--sub_catalog_id', 'dg-archive'])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_sub_catalog_definition: done")


    def test_all_sub_catalog_definitions(self):
        print("test_all_sub_catalog_definitions: starting")
        result = self.runner.invoke(self.commands.all_sub_catalog_definitions, args=[
            '--sub_catalog_id', 'dg-archive', '--limit', 5
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_all_sub_catalog_definitions: done")


    def test_sub_catalog_collection_definition(self):
        print("test_sub_catalog_collection_definition: starting")
        result = self.runner.invoke(self.commands.sub_catalog_collection_definition, args=[
            '--sub_catalog_id', 'dg-archive', '--sub_catalog_collection_id', 'wv04'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_sub_catalog_collection_definition: done")


class Ordering_cli_functions(unittest.TestCase):

    def setUp(self):
        self.commands = MGP_SDK.cli_commands.cli_commands
        self.runner = CliRunner()


    def test_all_pipelines(self):
        print("test_all_pipelines: starting")
        result = self.runner.invoke(self.commands.all_pipelines)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_all_pipelines: done")


    def test_get_pipeline(self):
        print("test_get_pipeline: starting")
        result = self.runner.invoke(self.commands.get_pipeline, args=['--namespace', 'imagery', '--name', 'map-ready'])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_get_pipeline: done")


    def test_a_order_validate(self):
        # This function requires a settings dictionary, a GEOjson, an output config dictionary, and a notifications
        # dicitonary in the .MGP-config file in order to run. Certain dictionaries cannot be passed in via command line
        print("test_order_validate: starting")
        result = self.runner.invoke(self.commands.order, args=[
            '--namespace', 'imagery', '--name', 'map-ready', '--metadata', 'cli-testing', '--validate', '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        self.assertIn("validation successful", result.output)
        assert result.exit_code == 0
        print("test_order_validate: done")


    def test_b_order_estimate(self):
        # This function requires a settings dictionary, a GEOjson, an output config dictionary, and a notifications
        # dicitonary in the .MGP-config file in order to run. Certain dictionaries cannot be passed in via command line
        print("test_order_estimate: starting")
        result = self.runner.invoke(self.commands.order, args=[
            '--namespace', 'imagery', '--name', 'map-ready', '--metadata', 'cli-testing', '--estimate', '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        self.assertIn("usage_estimate", result.output)
        assert result.exit_code == 0
        print("test_order_estimate: done")


    def test_c_order_place(self):
        # This function requires a settings dictionary, a GEOjson, an output config dictionary, and a notifications
        # dicitonary in the .MGP-config file in order to run. Certain dictionaries cannot be passed in via command line
        print("test_order_place: starting")
        result1 = self.runner.invoke(self.commands.order, args=[
            '--namespace', 'imagery', '--name', 'map-ready', '--metadata', 'cli-testing', '--yes'
        ])
        print(result1.output)
        self.assertEqual(type(ast.literal_eval(result1.output)), dict)
        order_id = ast.literal_eval(result1.output)['data']['id']
        assert result1.exit_code == 0
        print("test_order_place: done")
        # Test order details
        print("test_order_details: starting")
        result2 = self.runner.invoke(self.commands.order_details, args=['--order_id', order_id])
        print(result2.output)
        self.assertEqual(type(ast.literal_eval(result2.output)), dict)
        assert result2.exit_code == 0
        print("test_order_details: done")
        # Test order events
        print("test_order_events: starting")
        result3 = self.runner.invoke(self.commands.order_events, args=['--order_id', order_id, '--limit', 5])
        print(result3.output)
        self.assertEqual(type(ast.literal_eval(result3.output)), dict)
        assert result3.exit_code == 0
        print("test_order_events: done")
        # Test cancel order
        print("test_cancel_order: starting")
        result4 = self.runner.invoke(self.commands.cancel_order, args=['--order_id', order_id])
        print(result4.output)
        self.assertEqual(type(ast.literal_eval(result4.output)), dict)
        assert result4.exit_code == 0
        print("test_cancel_order: done")


    def test_list_users_orders(self):
        print("test_list_users_orders: starting")
        result = self.runner.invoke(self.commands.list_users_orders)
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_list_users_orders: done")


class Tasking_cli_functions(unittest.TestCase):

    def setUp(self):
        self.commands = MGP_SDK.cli_commands.cli_commands
        self.runner = CliRunner()
        self.pipeline = "imagery/map-ready"
        self.start_set_time = datetime.datetime.now() + datetime.timedelta(days=1)
        self.start_time = self.start_set_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.end_set_time = datetime.datetime.now() + datetime.timedelta(days=2)
        self.end_time = self.end_set_time.strftime("%Y-%m-%dT%H:%M:%SZ")


    def test_a_validate_tasking(self):
        print("test_validate_tasking: starting")
        result = self.runner.invoke(self.commands.submit_tasking, args=[
            '--pipeline', self.pipeline, '--recipe', '50cm_Color', '--start_datetime', self.start_time,
            '--end_datetime', self.end_time, '--metadata', "cli_testing_suite", '--validate', '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_validate_tasking: done")


    def test_b_submit_tasking(self):
        print("test_submit_tasking: starting")
        result = self.runner.invoke(self.commands.submit_tasking, args=[
            '--pipeline', self.pipeline, '--recipe', '50cm_Color', '--start_datetime', self.start_time,
            '--end_datetime', self.end_time, '--metadata', "cli_testing_suite", '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        tasking_id = ast.literal_eval(result.output)['data']['id']
        assert result.exit_code == 0
        print("test_submit_tasking: done")
        # Test get_tasking_request
        print("test_get_tasking_request: starting")
        result2 = self.runner.invoke(self.commands.get_tasking_request, args=['--tasking_id', tasking_id])
        print(result2.output)
        self.assertEqual(type(ast.literal_eval(result2.output)), dict)
        assert result2.exit_code == 0
        print("test_get_tasking_request: done")
        # Test cancel_tasking
        print("test_cancel_tasking: starting")
        result3 = self.runner.invoke(self.commands.cancel_tasking, args=[
            '--tasking_id', tasking_id, '--reason', "CLI Testing Suite"
        ])
        print(result3.output)
        self.assertEqual(type(ast.literal_eval(result3.output)), dict)
        assert result3.exit_code == 0
        print("test_cancel_tasking: done")


class Monitor_cli_functions(unittest.TestCase):

    def setUp(self):
        self.commands = MGP_SDK.cli_commands.cli_commands
        self.runner = CliRunner()
        self.pipeline = "imagery/map-ready"
        self.start_set_time = datetime.datetime.now() + datetime.timedelta(days=1)
        self.start_time = self.start_set_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.end_set_time = datetime.datetime.now() + datetime.timedelta(days=2)
        self.end_time = self.end_set_time.strftime("%Y-%m-%dT%H:%M:%SZ")


    def test_a_validate_monitor(self):
        print("test_validate_monitor: starting")
        result = self.runner.invoke(self.commands.create_monitor, args=[
            '--start_datetime', self.start_time, '--end_datetime', self.end_time, '--description', "CLI Testing Suite",
            '--validate', '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_validate_monitor: done")


    def test_b_validate_monitor_order(self):
        print("test_validate_monitor_order: starting")
        result = self.runner.invoke(self.commands.create_monitor, args=[
            '--start_datetime', self.start_time, '--end_datetime', self.end_time, '--description', "CLI Testing Suite",
            '--pipeline', self.pipeline, '--order_templates', '--validate', '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        assert result.exit_code == 0
        print("test_validate_monitor_order: done")


    def test_c_create_monitor_no_order(self):
        print("test_create_monitor_no_order: starting")
        result = self.runner.invoke(self.commands.create_monitor, args=[
            '--start_datetime', self.start_time, '--end_datetime', self.end_time, '--description', "CLI Testing Suite",
            '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        monitor_id = ast.literal_eval(result.output)['data']['id']
        assert result.exit_code == 0
        print("test_create_monitor_no_order: done")
        # Test get_monitor
        print("test_get_monitor: starting")
        result2 = self.runner.invoke(self.commands.get_monitor, args=['--monitor_id', monitor_id])
        print(result2.output)
        self.assertEqual(type(ast.literal_eval(result2.output)), dict)
        assert result2.exit_code == 0
        print("test_get_monitor: done")
        # Test monitor_events
        print("test_monitor_events: starting")
        result3 = self.runner.invoke(self.commands.monitor_events, args=['--monitor_id', monitor_id])
        print(result3.output)
        self.assertEqual(type(ast.literal_eval(result3.output)), dict)
        assert result3.exit_code == 0
        print("test_monitor_events: done")
        # Test toggle_monitor
        print("test_toggle_monitor: starting")
        result4 = self.runner.invoke(self.commands.toggle_monitor, args=['--monitor_id', monitor_id, '--disable'])
        print(result4.output)
        self.assertIn("Status change accepted", result4.output)
        assert result4.exit_code == 0
        print("test_toggle_monitor: done")


    def test_d_create_monitor_order(self):
        print("test_create_monitor_order: starting")
        result = self.runner.invoke(self.commands.create_monitor, args=[
            '--start_datetime', self.start_time, '--end_datetime', self.end_time, '--description', "CLI Testing Suite",
            '--order_templates', '--pipeline', self.pipeline, '--yes'
        ])
        print(result.output)
        self.assertEqual(type(ast.literal_eval(result.output)), dict)
        monitor_id = ast.literal_eval(result.output)['data']['id']
        assert result.exit_code == 0
        print("test_create_monitor_order: done")
        # Test get_monitor
        print("test_get_monitor: starting")
        result2 = self.runner.invoke(self.commands.get_monitor, args=['--monitor_id', monitor_id])
        print(result2.output)
        self.assertEqual(type(ast.literal_eval(result2.output)), dict)
        assert result2.exit_code == 0
        print("test_get_monitor: done")
        # Test monitor_events
        print("test_monitor_events: starting")
        result3 = self.runner.invoke(self.commands.monitor_events, args=['--monitor_id', monitor_id])
        print(result3.output)
        self.assertEqual(type(ast.literal_eval(result3.output)), dict)
        assert result3.exit_code == 0
        print("test_monitor_events: done")
        # Test toggle_monitor
        print("test_toggle_monitor: starting")
        result4 = self.runner.invoke(self.commands.toggle_monitor, args=['--monitor_id', monitor_id, '--disable'])
        print(result4.output)
        self.assertIn("Status change accepted", result4.output)
        assert result4.exit_code == 0
        print("test_toggle_monitor: done")



if __name__ == '__main__':
    unittest.main()
