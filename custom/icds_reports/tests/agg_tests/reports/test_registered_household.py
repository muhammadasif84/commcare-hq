from django.test.utils import override_settings

from custom.icds_reports.const import ChartColors, MapColors
from custom.icds_reports.reports.registered_household import get_registered_household_data_map, \
    get_registered_household_data_chart, get_registered_household_sector_data
from django.test import TestCase


@override_settings(SERVER_ENVIRONMENT='icds')
class TestRegisteredHousehold(TestCase):

    def test_map_data(self):
        self.assertDictEqual(
            get_registered_household_data_map(
                'icds-cas',
                config={
                    'month': (2017, 5, 1),
                    'aggregation_level': 1
                },
                loc_level='state'
            ),
            {
                "rightLegend": {
                    "info": "Total number of households registered: 2,799",
                    "average": 399.85714285714283,
                    "average_format": "number"
                },
                "fills": {
                    "Household": MapColors.BLUE,
                    "defaultFill": MapColors.GREY
                },
                "data": {
                    'st4': {'household': 0, 'original_name': ['st4'], 'fillKey': 'Household'}, 
                    'st5': {'household': 0, 'original_name': ['st5'], 'fillKey': 'Household'}, 
                    'st6': {'household': 0, 'original_name': ['st6'], 'fillKey': 'Household'}, 
                    'st7': {'household': 1, 'original_name': ['st7'], 'fillKey': 'Household'},
                    'st1': {'household': 1322, 'original_name': ['st1'], 'fillKey': 'Household'},
                    'st2': {'household': 1476, 'original_name': ['st2'], 'fillKey': 'Household'},
                    'st3': {'household': 0, 'original_name': ['st3'], 'fillKey': 'Household'}
                },
                "slug": "registered_household",
                "label": ""
            }
        )

    def test_map_name_is_different_data(self):
        self.maxDiff = None
        self.assertDictEqual(
            get_registered_household_data_map(
                'icds-cas',
                config={
                    'month': (2017, 5, 1),
                    'state_id': 'st1',
                    'district_id': 'd1',
                    'aggregation_level': 3
                },
                loc_level='block',
            ),
            {
                "rightLegend": {
                    "info": "Total number of households registered: 1,322",
                    "average": 661.0,
                    "average_format": "number"
                },
                "fills": {
                    "Household": MapColors.BLUE,
                    "defaultFill": MapColors.GREY
                },
                "data": {
                    'block_map': {
                        'household': 1322,
                        'original_name': ['b1', 'b2'],
                        'fillKey': 'Household'
                    }
                },
                "slug": "registered_household",
                "label": ""
            }
        )

    def test_chart_data(self):
        self.assertDictEqual(
            get_registered_household_data_chart(
                'icds-cas',
                config={
                    'month': (2017, 5, 1),
                    'aggregation_level': 1
                },
                loc_level='state'
            ),
            {
                "location_type": "State",
                "bottom_five": [
                    {'loc_name': 'st7', 'value': 1.0},
                    {'loc_name': 'st3', 'value': 0.0},
                    {'loc_name': 'st4', 'value': 0.0},
                    {'loc_name': 'st5', 'value': 0.0},
                    {'loc_name': 'st6', 'value': 0.0}
                    ,
                ],
                "top_five": [
                    {'loc_name': 'st2', 'value': 1476.0},
                    {'loc_name': 'st1', 'value': 1322.0},
                    {'loc_name': 'st7', 'value': 1.0},
                    {'loc_name': 'st3', 'value': 0.0},
                    {'loc_name': 'st4', 'value': 0.0},
                ],
                "chart_data": [
                    {
                        "color": ChartColors.BLUE,
                        "classed": "dashed",
                        "strokeWidth": 2,
                        "values": [
                            {
                                "y": 0.0,
                                "x": 1485907200000,
                                "all": 0
                            },
                            {
                                "y": 0.0,
                                "x": 1488326400000,
                                "all": 0
                            },
                            {
                                "y": 2792.0,
                                "x": 1491004800000,
                                "all": 0
                            },
                            {
                                "y": 2799.0,
                                "x": 1493596800000,
                                "all": 0
                            }
                        ],
                        "key": "Registered Households"
                    }
                ],
                "all_locations": [
                    {'loc_name': 'st2', 'value': 1476.0},
                    {'loc_name': 'st1', 'value': 1322.0},
                    {'loc_name': 'st7', 'value': 1.0},
                    {'loc_name': 'st3', 'value': 0.0},
                    {'loc_name': 'st4', 'value': 0.0},
                    {'loc_name': 'st5', 'value': 0.0},
                    {'loc_name': 'st6', 'value': 0.0},

                ]
            }
        )

    def test_sector_data(self):
        self.assertDictEqual(
            get_registered_household_sector_data(
                'icds-cas',
                config={
                    'month': (2017, 5, 1),
                    'state_id': 'st1',
                    'district_id': 'd1',
                    'block_id': 'b1',
                    'aggregation_level': 4
                },
                location_id='b1',
                loc_level='supervisor'
            ),
            {
                "info": "Total number of households registered",
                "tooltips_data": {
                    "s2": {
                        "household": 402
                    },
                    "s1": {
                        "household": 198
                    }
                },
                "chart_data": [
                    {
                        "color": MapColors.BLUE,
                        "classed": "dashed",
                        "strokeWidth": 2,
                        "values": [
                            [
                                "s1",
                                198
                            ],
                            [
                                "s2",
                                402
                            ]
                        ],
                        "key": ""
                    }
                ],
                "format": "number"
            }
        )
