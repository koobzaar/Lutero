import csv
class Converter:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self._load_data()
        
    def _load_data(self):
        with open(self.data_path, 'r') as file:
            data = list(csv.reader(file))
        return data

    def get_data_coverted(self):
        return self.data
    
   

   


        
        
