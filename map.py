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
mad = np.array(list(map(lambda x: x * 100, mad))) # Multiplicar por 100 para facilitar a visualização
min_mad = mad.min()
max_mad = mad.max()
normalized_mad = (mad - min_mad) / (max_mad - min_mad)

# Obter o mapa de cores 'viridis'
cmap = plt.get_cmap('magma')
quantity = 0
for i, country in enumerate(countries):
    if country in world['ADMIN'].values:
        quantity += 1
        color = cmap(normalized_mad[i])
        country_shape = world[world['ADMIN'] == country]
        country_shape.plot(ax=ax, color=color)
        
        # Adicionar rótulo com o valor de MAD
        representative_point = country_shape.geometry.representative_point()
               # Adiciona a sombra
        # Texto principal
        central_america_countries = [
    'Belize', 'Costa Rica', 'El Salvador', 'Guatemala', 'Honduras', 'Nicaragua', 'Panama'
]   
        if country not in central_america_countries:
          plt.text(representative_point.x.values[0], representative_point.y.values[0], f'{mad[i]:.1f}', 
                 fontsize=12, color='white', ha='center', va='center', fontweight='bold')

            
    else:
        print(f"País não encontrado: {country}")

sm = ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_mad, vmax=max_mad))

# Ajusta o layout para dar espaço à barra de cores na parte inferior
# plt.gcf().subplots_adjust(bottom=0.01)
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.05, pad=0.05)
cbar.set_label('\nDistribuição de MAD')

#make americas the center of map
ax.set_xlim(-170, -40)
ax.set_ylim(-60, 80)
plt.show()