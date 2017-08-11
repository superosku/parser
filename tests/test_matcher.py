import io
from parser.doctor import Doctor
from parser.matcher import Matcher

import pytest


class TestSetJsonDoctorData:
    def test_should_initialize_json_doctors(self):
        matcher = Matcher()
        matcher.set_json_doctor_data(io.StringIO(
            '{"doctor":{"first_name":"Dean","last_name":"Israel","npi":'
            '"85103080143784778415"},"practices":[]}'
        ))
        assert len(matcher.json_doctors) == 1
        assert matcher.json_doctors[0].first_name == 'Dean'
        assert matcher.json_doctors[0].last_name == 'Israel'
        assert matcher.json_doctors[0].npi == '85103080143784778415'


class TestSetCSVDoctorData:
    def test_should_skip_first_line(self):
        matcher = Matcher()
        matcher.set_CSV_doctor_data(io.StringIO(
            'bogus\n'
        ))
        assert len(matcher.csv_doctors) == 0

    def test_should_parse_csv_line(self):
        matcher = Matcher()
        matcher.set_CSV_doctor_data(io.StringIO(
            'bogus\n'
            'Justyn,Abbie,78362387662864903554\n'
        ))
        assert len(matcher.csv_doctors) == 1
        doctor = matcher.csv_doctors[0]
        assert doctor.first_name == 'Justyn'
        assert doctor.last_name == 'Abbie'
        assert doctor.npi == '78362387662864903554'


class TestMatchDatas:
    @pytest.fixture
    def json_doctors(self):
        return [
            Doctor(first_name='a', last_name='b', npi='111'),
            Doctor(first_name='a', last_name='b', npi='222')
        ]

    @pytest.fixture
    def csv_doctors(self):
        return [
            Doctor(first_name='a', last_name='b', npi='222'),
            Doctor(first_name='a', last_name='b', npi='333')
        ]

    @pytest.fixture
    def matcher(self, json_doctors, csv_doctors):
        matcher = Matcher()
        matcher.json_doctors = json_doctors
        matcher.csv_doctors = csv_doctors
        return matcher

    def test_matches_doctors_correctly(
        self, matcher, json_doctors, csv_doctors
    ):
        matcher.match_datas()
        assert len(matcher.matches) == 1
        assert len(matcher.without_match) == 1

        assert matcher.matches == [
            (csv_doctors[0], json_doctors[1])
        ]

        assert matcher.without_match == [csv_doctors[1]]
