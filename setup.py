import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent.resolve()

README = (HERE / "README.md").read_text()

setup(
  name = 'MGP_SDK',
  version = '1.1.0',
  license='MIT',
  description = 'SDK for interacting with Maxar Geospatial Platform',
  long_description=README,
  long_description_content_type="text/markdown",
  author = 'MDS Marianas Team',
  author_email = 'DL-GCS-Marianas@maxar.com',
  project_urls = {
        'Documentation': 'https://maxar-geospatial-platform.readthedocs.io/en/latest/',
        'Source': 'https://github.com/Maxar-Corp/maxar-geospatial-platform'
        },
  keywords = ['OGC', 'WMS', 'WFS', 'WMTS', 'WCS', 'MAXAR', 'IMAGERY', 'GIS'],
  python_requires= '>=3.7',
  install_requires=[
          'pyproj',
          'shapely',
          'requests',
          'ipython',
          'pillow',
          'click',
          'beautifulsoup4',
          'lxml'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  entry_points='''
    [console_scripts]
    search=MGP_SDK.streaming.cli_commands:search
    config=MGP_SDK.streaming.cli_commands:config_file
    password=MGP_SDK.streaming.cli_commands:reset_password
    download=MGP_SDK.streaming.cli_commands:download
    area=MGP_SDK.streaming.cli_commands:calculate_bbox_sqkm
    token=MGP_SDK.token_service.cli_commands:create_token
    get_token=MGP_SDK.token_service.cli_commands:get_tokens
    delete_token=MGP_SDK.token_service.cli_commands:delete_tokens
    '''
)
