class Data:
    def __init__(self, rawdata):
        self.rawdata = rawdata
        self.countries_ids = self._generate_index()

    def _generate_index(self):
        country_ids = {};
        for i in range(0, len(self.data)):
            if self.data[i][0] == '':
                country_ids[self.data[i][1]] = i
            else:
                country_ids[self.data[i][0]] = i
        return country_ids
    
    def _get_total_days(self, country_name):
        return len(self.data[self.countries_ids[country_name]][4:])

    def get_death_data(self, country_name):
        total_days = self._get_total_days(country_name)
        death_data_days = {}
        for i in range(0, total_days):
            death_data_days[i] = {
                "Data": self.data[0][i+4],
                "Deaths": self.data[self.countries_ids[country_name]][i+4]
            }
        return death_data_days

    def get_rawdata(self):
        return self.rawdata
    
    def get_all_availables_countries(self):
        return self.countries_ids
