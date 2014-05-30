from corehq.apps.commtrack.helpers import make_supply_point
from corehq.apps.commtrack.tests.util import CommTrackTest, make_loc, DAYS_IN_MONTH
from corehq.apps.locations.models import Location
from corehq.apps.locations.bulk import import_location
from mock import patch
from corehq.apps.consumption.shortcuts import get_default_consumption
from corehq.apps.commtrack.models import Product


class LocationImportTest(CommTrackTest):
    def names_of_locs(self):
        return [loc.name for loc in Location.by_domain(self.domain.name)]

    def test_import_new_top_level_location(self):
        data = {
            'name': 'importedloc'
        }

        import_location(self.domain.name, 'state', data)

        self.assertTrue(data['name'] in self.names_of_locs())

    def test_import_with_existing_parent_by_id(self):
        # state can't have outlet as child
        parent = make_loc('sillyparents', type='state')

        data = {
            'name': 'importedloc',
            'parent_id': parent._id
        }

        result = import_location(self.domain.name, 'district', data)

        if result['id'] is None:
            self.fail('import failed with error: %s' % result['message'])

        self.assertTrue(data['name'] in self.names_of_locs())
        new_loc = Location.get(result['id'])
        self.assertEqual(new_loc.parent_id, parent._id)

    def test_id_of_invalid_parent_type(self):
        # state can't have outlet as child
        parent = make_loc('sillyparents', type='state')
        data = {
            'name': 'oops',
            'outlet_type': 'SHG',
            'parent_id': parent._id
        }

        original_count = len(list(Location.by_domain(self.domain.name)))

        result = import_location(self.domain.name, 'outlet', data)

        self.assertEqual(result['id'], None)
        self.assertEqual(len(list(Location.by_domain(self.domain.name))), original_count)
        self.assertTrue('Invalid parent type' in result['message'])

    def test_invalid_parent_id(self):
        data = {
            'name': 'oops',
            'outlet_type': 'SHG',
            'parent_id': 'banana'
        }

        result = import_location(self.domain.name, 'outlet', data)

        self.assertTrue('Parent with id banana does not exist' in result['message'])

    def test_invalid_parent_domain(self):
        parent = make_loc('someparent', domain='notright', type='village')

        data = {
            'name': 'bad parent',
            'outlet_type': 'SHG',
            'site_code': 'wat',
            'parent_id': parent._id,
        }

        original_count = len(list(Location.by_domain(self.domain.name)))
        result = import_location(self.domain.name, 'outlet', data)
        self.assertEqual(result['id'], None)
        self.assertEqual(len(list(Location.by_domain(self.domain.name))), original_count)
        self.assertTrue('references a location in another project' in result['message'])

    def test_change_parent(self):
        parent = make_loc('original parent', type='village')
        existing = make_loc('existingloc', type='outlet', parent=parent)

        new_parent = make_loc('new parent', type='village')
        self.assertNotEqual(parent._id, new_parent._id)
        data = {
            'id': existing._id,
            'name': existing.name,
            'site_code': 'wat',
            'outlet_type': 'SHG',
            'parent_id': new_parent._id,
        }

        result = import_location(self.domain.name, 'outlet', data)
        new_loc = Location.get(result['id'])
        self.assertEqual(existing._id, new_loc._id)
        self.assertEqual(new_loc.parent_id, new_parent._id)

    def test_change_to_invalid_parent(self):
        parent = make_loc('original parent', type='village')
        existing = make_loc('existingloc', type='outlet', parent=parent)

        new_parent = make_loc('new parent', type='state')
        data = {
            'id': existing._id,
            'name': existing.name,
            'site_code': 'wat',
            'outlet_type': 'SHG',
            'parent_id': new_parent._id,
        }

        result = import_location(self.domain.name, 'outlet', data)
        self.assertEqual(None, result['id'])
        self.assertTrue('Invalid parent type' in result['message'])
        new_loc = Location.get(existing._id)
        self.assertEqual(existing._id, new_loc._id)
        self.assertEqual(new_loc.parent_id, parent._id)

    def test_updating_existing_location_properties(self):
        parent = make_loc('sillyparents', type='village')
        existing = make_loc('existingloc', type='outlet', parent=parent)

        data = {
            'id': existing._id,
            'name': existing.name,
            'site_code': 'wat',
            'outlet_type': 'SHG'
        }

        self.assertNotEqual(existing.site_code, data['site_code'])

        loc_id = import_location(self.domain.name, 'outlet', data).get('id', None)
        new_loc = Location.get(loc_id)

        self.assertEqual(existing._id, loc_id)
        self.assertEqual(new_loc.site_code, data['site_code'])

    def test_given_id_matches_type(self):
        existing = make_loc('existingloc', type='state')

        data = {
            'id': existing._id,
            'name': 'new_name',
        }

        result = import_location(self.domain.name, 'outlet', data)

        self.assertEqual(result['id'], None)
        self.assertTrue('Existing location type error' in result['message'])

    def test_shouldnt_save_if_no_changes(self):
        parent = make_loc('sillyparents', type='village')
        existing = make_loc('existingloc', type='outlet', parent=parent)
        existing.site_code = 'wat'
        existing.outlet_type = 'SHG'
        existing.save()

        data = {
            'id': existing._id,
            'name': existing.name,
            'site_code': 'wat',
            'outlet_type': 'SHG',
        }

        with patch('corehq.apps.locations.forms.LocationForm.save') as save:
            result = import_location(self.domain.name, 'outlet', data)
            self.assertEqual(save.call_count, 0)
            self.assertEqual(result['id'], existing._id)

    def test_should_still_save_if_name_changes(self):
        # name isn't a dynamic property so should test these still
        # get updated alone
        parent = make_loc('sillyparents', type='village')
        existing = make_loc('existingloc', type='outlet', parent=parent)
        existing.site_code = 'wat'
        existing.outlet_type = 'SHG'
        existing.save()

        data = {
            'id': existing._id,
            'name': 'newname',
            'site_code': 'wat',
            'outlet_type': 'SHG',
        }

        with patch('corehq.apps.locations.forms.LocationForm.save') as save:
            result = import_location(self.domain.name, 'outlet', data)
            self.assertEqual(save.call_count, 1)
            # id isn't accurate because of the mock, but want to make
            # sure we didn't actually return with None
            self.assertTrue(result['id'] is not None)

    def test_should_import_consumption(self):
        existing = make_loc('existingloc', type='state')
        sp = make_supply_point(self.loc.domain, existing)

        data = {
            'id': existing._id,
            'name': 'existingloc',
            'default_pp': 77
        }

        import_location(self.domain.name, 'state', data)

        self.assertEqual(
            get_default_consumption(
                self.domain.name,
                Product.get_by_code(self.domain.name, 'pp')._id,
                'state',
                sp._id,
            ),
            77 / DAYS_IN_MONTH
        )

    def test_import_coordinates(self):
        data = {
            'name': 'importedloc',
            'latitude': 55,
            'longitude': -55,
        }

        loc_id = import_location(self.domain.name, 'state', data)['id']

        loc = Location.get(loc_id)

        self.assertEqual(data['latitude'], loc.latitude)
        self.assertEqual(data['longitude'], loc.longitude)
