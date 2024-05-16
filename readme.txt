1 - Para a execução do código primeiro deverão ser instalados os módulos numpy, pandas, matplotlib, datetime e scipy.
2 - O código foi comentado de forma a demonstrar onde foi cumprida cada uma das condições impostas na tarefa.
3 - O arquivo csv/data de entrada deve ser altetrado na linha 81 do código.
4 - O Arquivo csv/data deverá conter a classe como a última coluna do arquivo, pois esta será ignorada na execução do algoritmo.
5 - Os dados são carregados e normalizados para os cálculos.
6 - A função calculate_distance_matrix é utilizada para calcular a matriz de distâncias para o algoritmo.
7 - a função single_link tanto calcula as distâncias e executa o single link, quanto também faz a montagem da linkage_matrix, sendo esta utilizada futuramente para plotagem do dendograma.
8 - A biblioteca scipi foi utilizada unicamente para plotagem do dendograma, o algoritmo foi implementado manualmente.
9 - Ao fim do código serão gerados três arquivos:
	9.1 - o primeiro deles no formato PDF, sendo este o dendogram_matrix seguido pelo momento onde ele foi gerado, este contém a matriz de distâncias e o dendograma gerado pelo single_link
	9.2 - o segundo deles no formato txt, sendo este o matrix seguido pelo momento onde ele foi gerado, este contém a matriz de distâncias em formato de texto, utilizada para conferência.
	9.3 - o terceiro deles também no formato txt, sendo este o hierarchy seguido pelo momento onde ele foi gerado, este contém a hierarquia, a cada nível mostrando quais foram os índices dos itens que foram agrupados e em qual nível ocorreu tal agrupamento.
