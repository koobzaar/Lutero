import matplotlib.pyplot as plt
import geopandas
import numpy as np
from matplotlib.cm import ScalarMappable
import os
import subprocess

world = geopandas.read_file('./world_map/ne_110m_admin_0_countries.shp')
ax = world.plot(color='#e2e2e2', edgecolor='black', lw=0.2)

countries = []
mad = []


countries = []
mad = []

# O script de mapa só pode ser gerado se houver valores de mad presentes em mad.txt
# Caso não haja nenhum valor de mad gerado previamente, o script por padrão gera um mapa global
def check_and_generate_mad():
    file_path = 'results/mad.txt'
    
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print("Arquivo 'results/mad.txt' não encontrado ou está vazio. Gerando valores de MAD...")
        
        subprocess.run(['python', 'main.py', '--all'], check=True)
        
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            raise FileNotFoundError("Falha ao gerar o arquivo 'results/mad.txt'. Verifique o script main.py.")
    
    with open(file_path, 'r') as file:
        for line in file:
            countries.append(line.split(',')[0])
            mad.append(float(line.split(',')[1].strip()))

check_and_generate_mad()

# Normalizar os valores de 'mad'
mad = np.array(mad)  # Já convertido para float durante a leitura
min_mad = mad.min()
max_mad = mad.max()
normalized_mad = (mad - min_mad) / (max_mad - min_mad)

# Obter o mapa de cores 'viridis'
cmap = plt.get_cmap('viridis')
quantity = 0
for i, country in enumerate(countries):
    if country in world['ADMIN'].values:
        quantity+=1
        color = cmap(normalized_mad[i])
        world[world['ADMIN'] == country].plot(ax=ax, color=color)
    else:
        print(f"País não encontrado: {country}")


sm = ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_mad, vmax=max_mad))
sm.set_array([]) 

# Ajusta o layout para dar espaço à barra de cores na parte inferior
ax.set_xticks([])  # Remove os ticks do eixo X
ax.set_yticks([])  # Remove os ticks do eixo Y
ax.set_xticklabels([])  # Remove as etiquetas do eixo X
ax.set_yticklabels([])  # Remove as etiquetas do eixo Y
ax.xaxis.set_visible(False)  # Esconde o eixo X
ax.yaxis.set_visible(False)  # Esconde o eixo Y

plt.gcf().subplots_adjust(bottom=0.2)

cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.1, pad=0.1)
cbar.set_label('Valor de MAD')
print(quantity)

plt.show()
