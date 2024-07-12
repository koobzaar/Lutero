import csv
import glob

class Converter:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self._load_data()
        
    def _load_data(self):
        data = []
        # Implementação ridícula. Deveria ser aberto linha por linha, e não carregar tudo de uma vez
        for file_path in glob.glob(self.data_path + '/*.csv'):
            # Solução ridícula. Mas ocupa menos espaço na memória que verificar via amostra
            if 'brasil_ministerio_saude' in file_path:
                delimiter = ';'
            else:
                delimiter = ','
            with open(file_path, 'r', encoding='utf-8') as file:
                data.extend(list(csv.reader(file, delimiter=delimiter)))
        return data

    def get_data_converted(self):
        return self.data