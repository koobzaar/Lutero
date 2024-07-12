from tqdm import tqdm
from abc import ABC, abstractmethod

class IData(ABC):
    @abstractmethod
    def get_data(self):
        pass

class ICountryData(IData):
    @abstractmethod
    def get_all_available_countries(self):
        pass

class IDeathData(IData):
    @abstractmethod
    def get_detailed_death_data(self, country_name):
        pass


class Data(IDeathData, ICountryData):
    """
    Represents a data manager for death data and country data.

    Args:
        data (list): The data containing death and country information.

    Attributes:
        data (list): The data containing death and country information.
        countries_ids (dict): A dictionary mapping country names to their respective indices in the data.

    """

    def __init__(self, data):
        self.data = data
        self.countries_ids = self._generate_index()

    def _generate_index(self):
        """
        Generates an index mapping country names to their respective indices in the data.

        Returns:
            dict: A dictionary mapping country names to their respective indices.

        """
        country_ids = {}
        for i in tqdm(range(1, len(self.data)), desc='Generating index'):
            if self.data[i][0] == '':
                country_ids[self.data[i][1]] = i
            else:
                country_ids[self.data[i][0]] = i
        return country_ids
    
    def _get_total_days(self, country_name):
        """
        Returns the total number of days for a given country.

        Args:
            country_name (str): The name of the country.

        Returns:
            int: The total number of days.

        """
        return len(self.data[self.countries_ids[country_name]][4:])

    def _get_death_variation(self, country_name, current_day):
        """
        Returns the difference in deaths between the current day and the previous day.

        Args:
            country_name (str): The name of the country.
            current_day (int): The current day.

        Returns:
            int: The difference in deaths.
        """
        if current_day == 0:
            return int(self.data[self.countries_ids[country_name]][current_day+4])
        else:
            return int(self.data[self.countries_ids[country_name]][current_day+4]) - int(self.data[self.countries_ids[country_name]][current_day+3])

    def get_detailed_death_data(self, country_name):
        """
        Returns the death data for a given country.

        Args:
            country_name (str): The name of the country.

        Returns:
            dict: A dictionary containing the death data for each day, with keys 'Date' and 'Deaths'.

        """
        total_days = self._get_total_days(country_name)
        death_data_days = {}
        for i in tqdm(range(0, total_days), desc='Getting detailed death data'):
            death_data_days[i] = {
                "Date": self.data[0][i+4],
                "Deaths": int(self.data[self.countries_ids[country_name]][i+4]),
                "Variation": self._get_death_variation(country_name, i)
            }
        return death_data_days
    def get_death_data(self, country_name):
        """
        Returns the death data for a given country.

        Args:
            country_name (str): The name of the country.

        Returns:
            list: A list containing the death data for each day.

        """
        total_days = self._get_total_days(country_name)
        death_data_days = []
        for i in tqdm(range(0, total_days), desc=f'Processando dados de mortes de: {country_name}'):
            death_data_days.append(int(float(self.data[self.countries_ids[country_name]][i+4])))
        return death_data_days
    
    def get_death_variation(self, country_name):
        """
        Returns the death variation for a given country.
    
        Args:
            country_name (str): The name of the country.
    
        Returns:
            list: A list containing the death variation for each day.
    
        """
        death_data = self.get_death_data(country_name)
        death_variation = [j-i for i, j in zip(death_data[:-1], death_data[1:])]
        return death_variation

    def get_death_variation_for_CVI(self, raw_data):
        # return only the 6 column of each line
        death_variation = []
        for i in range(1, len(raw_data)):
            if(raw_data[i][5] == '' or int(raw_data[i][5]) < 0):
                continue
            death_variation.append(int(raw_data[i][5]))
        return death_variation

    def get_death_variation_for_BMS(self, raw_data):
        # return only the 6 column of each line
        death_variation = []
        for i in range(1, len(raw_data)):
            if(raw_data[i][0]!='Brasil' or raw_data[i][13] == '' or int(raw_data[i][13]) < 0):
                continue
            death_variation.append(int(raw_data[i][13]))
        print(death_variation)
        print(len(death_variation))
        return death_variation

    def get_death_variation_for_USA(self, raw_data):
        # return only the 6 column of each line
        death_variation = []
        for i in range(1, len(raw_data)):
            if(raw_data[i][2] == '' or not raw_data[i][2].isdigit() or int(raw_data[i][2]) < 0):
                continue
            death_variation.append(int(raw_data[i][2]))
        print(death_variation)
        print(len(death_variation))
        return death_variation


    def get_data(self):
        return self.data

    def get_all_available_countries(self):
        """
        Returns all available countries and their respective indices.

        Returns:
            dict: A dictionary mapping country names to their respective indices.

        """
        return self.countries_ids
    
