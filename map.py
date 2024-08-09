import matplotlib.pyplot as plt
import geopandas
import numpy as np
from matplotlib.cm import ScalarMappable

world = geopandas.read_file('./world_map/ne_110m_admin_0_countries.shp')
ax = world.plot(color='#e2e2e2', edgecolor='black', lw=0.2)

# Importa todos os países de results.txt
countries = []
mad = []
with open('results/mad.txt', 'r') as file:
    for line in file:
        countries.append(line.split(',')[0])
        mad.append(float(line.split(',')[1].strip()))

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

# Cria um objeto ScalarMappable para a barra de cores
sm = ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min_mad, vmax=max_mad))
sm.set_array([])  # Você pode passar os valores de 'mad' aqui se quiser

# Ajusta o layout para dar espaço à barra de cores na parte inferior
ax.set_xticks([])  # Remove os ticks do eixo X
ax.set_yticks([])  # Remove os ticks do eixo Y
ax.set_xticklabels([])  # Remove as etiquetas do eixo X
ax.set_yticklabels([])  # Remove as etiquetas do eixo Y
ax.xaxis.set_visible(False)  # Esconde o eixo X
ax.yaxis.set_visible(False)  # Esconde o eixo Y

plt.gcf().subplots_adjust(bottom=0.2)

# Adiciona a barra de cores na parte inferior do gráfico
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.1, pad=0.1)
cbar.set_label('Valor de MAD')
print(quantity)

# Definir os limites para as Américas
# Definir os limites para a América do Sul
plt.show()
