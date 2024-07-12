import csv
import glob

class Converter:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self._load_data()
        
    def _load_data(self):
        data = []
        for file_path in glob.glob(self.data_path + '/*.csv'):
            with open(file_path, 'r', encoding='utf-8') as file:
                # Lê uma pequena amostra do arquivo para determinar o delimitador
                sample = file.read(1024)
                file.seek(0)  # Retorna ao início do arquivo após a leitura da amostra
                # Usa o Sniffer para detectar o delimitador
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample)
                csv_reader = csv.reader(file, dialect)
                # Pula o cabeçalho para arquivos subsequentes
                next(csv_reader, None)
                for row in csv_reader:
                    data.append(row)
        return data

    def get_data_coverted(self):
        return self.data
    
   

   


        
        
