from collections import namedtuple

Location = namedtuple(
    'Location',
    ['street', 'street_2', 'zip', 'city', 'state']
)


class Doctor:
    def __init__(self, first_name, last_name, npi, locations=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.npi = npi
        self.locations = locations

    @classmethod
    def from_json(cls, json_data):
        locations = []
        for location_json in json_data['practices']:
            locations.append(Location(
                location_json['street'],
                location_json['street_2'],
                location_json['zip'],
                location_json['city'],
                location_json['state'],
            ))
        return cls(
            json_data['doctor']['first_name'],
            json_data['doctor']['last_name'],
            json_data['doctor']['npi'],
            locations
        )

    @classmethod
    def from_CSV(cls, csv_line):
        line_data = [
            item.strip('"') for item in csv_line.strip().split(',')
        ]
        if len(line_data) == 3:
            return cls(
                line_data[0],
                line_data[1],
                line_data[2]
            )
        elif len(line_data) == 8:
            return cls(
                line_data[0],
                line_data[1],
                line_data[2],
                [
                    Location(
                        line_data[3],
                        line_data[4],
                        line_data[7],
                        line_data[5],
                        line_data[6],
                    )
                ]
            )
        else:
            raise ValueError('Illegal csv line')

    def match_npi(self, other_doctor):
        if not self.npi or not other_doctor.npi:
            return False
        return self.npi.lower() == other_doctor.npi.lower()

    def match_name(self, other_doctor):
        return (
            self.first_name.lower() == other_doctor.first_name.lower() and
            self.last_name.lower() == other_doctor.last_name.lower()
        )

    def match_location(self, other_doctor):
        for own_location in self.locations:
            for other_location in other_doctor.locations:
                if (
                    own_location.street.lower() ==
                    other_location.street.lower() and
                    own_location.street_2.lower() ==
                    other_location.street_2.lower() and
                    own_location.zip.lower() == other_location.zip.lower() and
                    own_location.city.lower() ==
                    other_location.city.lower() and
                    own_location.state.lower() == other_location.state.lower()
                ):
                    return True
        return False

    def match_doctor(self, other_doctor):
        if self.npi and other_doctor.npi:
            return self.match_npi(other_doctor)
        else:
            return (
                self.match_name(other_doctor) and
                self.match_location(other_doctor)
            )
