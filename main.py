from parser.matcher import Matcher

if __name__ == '__main__':
    matcher = Matcher()
    matcher.set_json_doctor_data(open('source_data.json'))
    matcher.set_CSV_doctor_data(open('match_file.csv'))
    matcher.match_datas()
    matcher.print_results()
