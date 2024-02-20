import data_manager
class Country(data_manager.Data):
    def __init__(self, rawdata, country_name):
        super().__init__(rawdata)
        self.country_name = country_name
        self.death_data = self.get_death_data(country_name)
        self.get_days_only = self._get_days_data_only()
        self.get_death_only = self._get_death_data_only()

    def _get_days_data_only(self):
        days = []
        for i in range(0, len(self.death_data)):
            days.append(self.death_data[i]["Data"])
        return days
    
    def _get_death_data_only(self):
        death = []
        for i in range(0, len(self.death_data)):
            death.append(self.death_data[i]["Deaths"])
        return death