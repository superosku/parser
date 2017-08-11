from parser.doctor import Doctor, Location

import pytest


class TestParseFromJson:
    @pytest.fixture
    def data(self):
        return {
            'doctor': {
                'first_name': 'Dean',
                'last_name': 'Israel',
                'npi': '85103080143784778415'
            },
            'practices': [
                {
                    'street': '271 Annabelle Fort',
                    'street_2': 'Apt. 404',
                    'zip': '53549',
                    'city': 'Port Demetris',
                    'state': 'LA',
                    'lat': '-79.8757664338564',
                    'lon': '84.31253504872467'
                }
            ]
        }

    @pytest.fixture
    def doctor(self, data):
        return Doctor.from_json(data)

    def test_parses_doctor_from_json(self, doctor):
        assert doctor.first_name == 'Dean'
        assert doctor.last_name == 'Israel'
        assert doctor.npi == '85103080143784778415'

    def test_parses_locations_from_json(self, doctor):
        assert len(doctor.locations) == 1
        location = doctor.locations[0]
        assert location.street == '271 Annabelle Fort'
        assert location.street_2 == 'Apt. 404'
        assert location.zip == '53549'
        assert location.city == 'Port Demetris'
        assert location.state == 'LA'


class TestParseFromCSV:
    def test_without_location_data(self):
        doctor = Doctor.from_CSV(
            'Justyn,Abbie,78362387662864903554'
        )
        assert doctor.first_name == 'Justyn'
        assert doctor.last_name == 'Abbie'
        assert doctor.npi == '78362387662864903554'

    def test_without_npi(self):
        doctor = Doctor.from_CSV(
            'Justyn,Abbie,""'
        )
        assert doctor.first_name == 'Justyn'
        assert doctor.last_name == 'Abbie'
        assert doctor.npi == ''

    def test_with_location_data(self):
        doctor = Doctor.from_CSV(
            'Granville,Benton,17871640342222098849,95496 dare rue,suite 203,'
            'octaviastad,il,45294-0751'
        )
        assert doctor.first_name == 'Granville'
        assert doctor.last_name == 'Benton'
        assert doctor.npi == '17871640342222098849'
        assert len(doctor.locations) == 1
        location = doctor.locations[0]
        assert location.street == '95496 dare rue'
        assert location.street_2 == 'suite 203'
        assert location.zip == '45294-0751'
        assert location.city == 'octaviastad'
        assert location.state == 'il'

    def test_with_invalid_data(self):
        with pytest.raises(ValueError):
            Doctor.from_CSV(
                'Granville,Benton,17871640342222098849,95496 dare rue,suite 2'
            )


class MatchTestCase:
    @pytest.fixture
    def doctor_a(self):
        return Doctor(
            first_name='Justny',
            last_name='Abbie',
            npi='abc123',
            locations=[
                Location('Dae rue', 'suite 1', '123', 'Helsinki', 'CA')
            ]
        )

    @pytest.fixture
    def doctor_b(self):
        return Doctor(
            first_name='Justny',
            last_name='Abbie',
            npi='abc123',
            locations=[
                Location('Dae rue', 'suite 1', '123', 'Helsinki', 'CA')
            ]
        )


class TestMatchNpi(MatchTestCase):
    def test_should_match_same_npis(self, doctor_a, doctor_b):
        assert doctor_a.match_npi(doctor_b)

    def test_should_match_npis_with_different_cases(self, doctor_a, doctor_b):
        doctor_a.npi = 'ABC123'
        assert doctor_a.match_npi(doctor_b)

    def test_should_not_match_different_npis(self, doctor_a, doctor_b):
        doctor_a.npi = '123456'
        assert not doctor_a.match_npi(doctor_b)

    def test_should_not_match_empty(self, doctor_a, doctor_b):
        doctor_a.npi = ''
        doctor_b.npi = ''
        assert not doctor_a.match_npi(doctor_b)


class TestMatchName(MatchTestCase):
    def test_should_match_same_names(self, doctor_a, doctor_b):
        assert doctor_a.match_name(doctor_b)

    def test_should_match_same_names_with_different_cases(
        self, doctor_a, doctor_b
    ):
        doctor_a.first_name = 'justNY'
        doctor_a.last_name = 'aBBie'
        assert doctor_a.match_name(doctor_b)

    def test_should_not_match_different_names(
        self, doctor_a, doctor_b
    ):
        doctor_a.first_name = 'Ben'
        doctor_a.last_name = 'Israel'
        assert not doctor_a.match_name(doctor_b)


class TestMatchLocation(MatchTestCase):
    def test_should_match_same_locations(self, doctor_a, doctor_b):
        assert doctor_a.match_location(doctor_b)

    def test_should_match_locations_with_different_casing(
        self, doctor_a, doctor_b
    ):
        doctor_a.locations = [
            Location('dae rue', 'SUITE 1', '123', 'HELsinki', 'ca')
        ]
        assert doctor_a.match_location(doctor_b)

    def test_should_match_regardless_of_multiple_non_matchin_locations(
            self, doctor_a, doctor_b
    ):
        doctor_a.locations = [
            Location('Dae rue', 'xxxx', '123', 'Helsinki', 'CA'),
            Location('Dae rue', 'suite 1', '123', 'Helsinki', 'CA'),
            Location('Dae rue', 'yyyy', '123', 'Helsinki', 'CA'),
        ]
        doctor_b.locations = [
            Location('Dae rue', 'zzzz', '123', 'Helsinki', 'CA'),
            Location('Dae rue', 'suite 1', '123', 'Helsinki', 'CA'),
            Location('Dae rue', 'aaaa', '123', 'Helsinki', 'CA'),
        ]
        assert doctor_a.match_location(doctor_b)

    def test_should_not_match_when_either_of_doctors_has_no_locations(
            self, doctor_a, doctor_b
    ):
        doctor_a.locations = []
        assert not doctor_a.match_location(doctor_b)
        assert not doctor_b.match_location(doctor_a)

    def test_should_not_match_when_neither_of_doctors_has_locations(
        self, doctor_a, doctor_b
    ):
        doctor_a.locations = []
        doctor_b.locations = []
        assert not doctor_a.match_location(doctor_b)
        assert not doctor_b.match_location(doctor_a)


class TestMatchDoctor:
    def test_should_match_doctors_with_same_npi(self):
        doctor_a = Doctor(
            first_name='a', last_name='b', npi='123'
        )
        doctor_b = Doctor(
            first_name='c', last_name='d', npi='123'
        )
        assert doctor_a.match_doctor(doctor_b)

    def test_should_not_match_doctors_with_just_same_names(self):
        doctor_a = Doctor(
            first_name='Pekka', last_name='Puupaa', npi=''
        )
        doctor_b = Doctor(
            first_name='Pekka', last_name='Puupaa', npi=''
        )
        assert not doctor_a.match_doctor(doctor_b)

    def test_should_match_doctors_with_same_name_and_location(self):
        doctor_a = Doctor(
            first_name='Pekka', last_name='Puupaa', npi='', locations=[
                Location('Dae rue', 'suite 1', '123', 'Helsinki', 'CA')
            ]
        )
        doctor_b = Doctor(
            first_name='Pekka', last_name='Puupaa', npi='', locations=[
                Location('Dae rue', 'suite 1', '123', 'Helsinki', 'CA')
            ]
        )
        assert doctor_a.match_doctor(doctor_b)

    def test_should_not_match_doctors_with_different_npis(self):
        doctor_a = Doctor(
            first_name='Pekka', last_name='Puupaa', npi='123', locations=[
                Location('Dae rue', 'suite 1', '123', 'Helsinki', 'CA')
            ]
        )
        doctor_b = Doctor(
            first_name='Pekka', last_name='Puupaa', npi='321', locations=[
                Location('Dae rue', 'suite 1', '123', 'Helsinki', 'CA')
            ]
        )
        assert not doctor_a.match_doctor(doctor_b)
