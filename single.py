import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from scipy.cluster.hierarchy import dendrogram


def euclidean_distance(point1, point2):#i.	Medida de proximidade: distância Euclidiana
    return np.sqrt(np.sum((point2 - point1) ** 2))

def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    data = df.iloc[:, :-1].values  #A última coluna foi removida pois era a classe    
    normalized_data = (data - data.mean(axis=0)) / data.std(axis=0) # Normalização dos dados
    return normalized_data

# Função para calcular a matriz de distâncias entre todos os pontos do conjunto de dados
def calculate_distance_matrix(data):
    n = len(data)
    distances = np.zeros((n, n))  #Primeiro crio a matriz com zeros
    
    for i in range(n): 
        for j in range(i+1, n):
            distances[i, j] = euclidean_distance(data[i], data[j])#i.	Medida de proximidade: distância Euclidiana
            distances[j, i] = distances[i, j]  # Matriz simétrica
    
    return distances

# Função para executar o algoritmo de clusterização Single Link
def single_link(data):
    n = len(data)
    clusters = [[i] for i in range(n)]  # Inicializa cada ponto como um cluster separado
    distances = calculate_distance_matrix(data)  # Calcula a matriz de distâncias
    iterations = 0
    hierarchy = []
    linkage_matrix = []
    cluster_label = n  # Novo índice de cluster a ser utilizado

    
    cluster_map = {i: i for i in range(n)}#Dicionário para mapear índices de pontos para os novos índices de clusters

    while len(clusters) > 1: #ii.	Condição de parada: um único grupo seja obtido
        min_distance = np.inf
        merge_indices = None
        
        # Calcula os clusters com a menor distância
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                for idx1 in clusters[i]:
                    for idx2 in clusters[j]:
                        if distances[idx1, idx2] < min_distance:
                            min_distance = distances[idx1, idx2]
                            merge_indices = (i, j)
        
        # Une os clusters com a menor distância
        cluster1, cluster2 = clusters[merge_indices[0]], clusters[merge_indices[1]]
        new_cluster = cluster1 + cluster2
        clusters.append(new_cluster)

        # Adiciona a fusão à matriz de ligação usando novos índices de clusters
        cluster1_id = cluster_map[cluster1[0]]
        cluster2_id = cluster_map[cluster2[0]]
        linkage_matrix.append([cluster1_id, cluster2_id, min_distance, len(new_cluster)])
        
        # Atualiza o mapeamento de clusters com um novo índice
        for idx in new_cluster:
            cluster_map[idx] = cluster_label
        cluster_label += 1
        
        # Remove os clusters antigos
        del clusters[max(merge_indices)]
        del clusters[min(merge_indices)]

        # Salva os clusters pra apresentar futuramente no arquivo
        hierarchy.append([set(c) for c in clusters])
        iterations += 1

    return clusters, distances, iterations, hierarchy, linkage_matrix

file_path = "iris.data"  #c.	O seu programa deve receber como entrada um arquivo.csv 
X = preprocess_data(file_path)


# Executar o algoritmo
clusters, distances, iterations, hierarchy, linkage_matrix = single_link(X)

#Arquivos gerados pela execução
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
result_matrix_file = f"matrix_{current_time}.txt"
result_pdf_file = f"dendrogram_matrix_{current_time}.pdf"
result_hierarchy_file = f"hierarchy_{current_time}.txt"

#Salva em um PDF resultados para verificar o resultado da execução
with PdfPages(result_pdf_file) as pdf:
    # Plotar uma matriz de distância
    plt.figure(figsize=(8, 6))
    plt.imshow(distances, cmap='viridis', origin='lower', interpolation='nearest')
    plt.colorbar(label='Distância Euclidiana')
    plt.title('Matriz de Distâncias')
    plt.xlabel('Índice do Elemento')
    plt.ylabel('Índice do Elemento')
    pdf.savefig()
    plt.close()

    # Plotar um dendograma para verificar o agrupamentto
    plt.figure(figsize=(10, 5))
    dendrogram(np.array(linkage_matrix))
    plt.title(f'Dendrograma Hierárquico - Iterações: {iterations}')
    plt.xlabel('Índice do Elemento')
    plt.ylabel('Distância')
    pdf.savefig()
    plt.close()


#Salvo a matriz de distâncias para conferência
np.savetxt(result_matrix_file, distances, fmt='%.4f', delimiter='\t')


with open(result_hierarchy_file, 'w') as f: #deverá produzir como saída um arquivo indicando em cada nível da hierarquia qual par de elementos, representados pela sua posição no arquivo
    for level, groups in enumerate(hierarchy):
        f.write(f"Nivel {level}:\n")
        for group in groups:
            f.write("{" + ", ".join(map(str, group)) + "}\n")
        f.write("\n")

print(f"Execução completa em {iterations} iterações.")
