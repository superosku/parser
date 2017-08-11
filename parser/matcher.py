import json
from parser.doctor import Doctor


class Matcher():
    def __init__(self):
        self.json_doctors = []
        self.csv_doctors = []

        self.matches = []
        self.without_match = []

    def set_json_doctor_data(self, file_object):
        self.json_doctors = []
        with file_object as file:
            for line in file.readlines():
                self.json_doctors.append(Doctor.from_json(json.loads(line)))

    def set_CSV_doctor_data(self, file_object):
        self.csv_doctors = []
        with file_object as file:
            file.readline()  # Skip csv:s first line
            for line in file.readlines():
                self.csv_doctors.append(Doctor.from_CSV(line))

    def _get_matchin_json_doctor(self, csv_doctor):
        for doctor in self.json_doctors:
            if doctor.match_doctor(csv_doctor):
                return doctor

    def match_datas(self):
        for csv_doctor in self.csv_doctors:
            matching_json_doctor = self._get_matchin_json_doctor(csv_doctor)
            if matching_json_doctor:
                self.matches.append(
                    (csv_doctor, matching_json_doctor)
                )
            else:
                self.without_match.append(csv_doctor)

    def print_results(self):
        print('Doctors in our database:', len(self.json_doctors))
        print('Doctors in CSV file:', len(self.csv_doctors))
        print('Matches found:', len(self.matches))
        print('CSV doctors without match:', len(self.without_match))
        print('Match %:', 100 * len(self.matches) / len(self.csv_doctors))
