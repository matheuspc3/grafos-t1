from collections import defaultdict, deque


class Grafo:
    def __init__(self, representacao="lista"):
        self.num_vertices = 0
        self.num_arestas = 0
        self.representacao = representacao  # 'lista' ou 'matriz'
        self.lista_adjacencia = defaultdict(list)
        self.matriz_adjacencia = []
        self.tem_peso = False

    def carregar_arquivo(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()

        self.num_vertices = int(linhas[0].strip())
        self.num_arestas = 0

        # Inicializar matriz se for o caso
        if self.representacao == "matriz":
            self.matriz_adjacencia = [[0] * self.num_vertices for _ in range(self.num_vertices)]

        for linha in linhas[1:]:
            partes = linha.strip().split()
            if len(partes) < 2:
                continue
            u = int(partes[0]) - 1
            v = int(partes[1]) - 1
            peso = float(partes[2]) if len(partes) == 3 else 1.0
            if len(partes) == 3:
                self.tem_peso = True

            if self.representacao == "lista":
                self.lista_adjacencia[u].append((v, peso))
                self.lista_adjacencia[v].append((u, peso))  # Grafo não direcionado
            elif self.representacao == "matriz":
                self.matriz_adjacencia[u][v] = peso
                self.matriz_adjacencia[v][u] = peso  # Grafo não direcionado

            self.num_arestas += 1

    def salvar_info_grafo(self, caminho_saida):
        graus = self.calcular_graus()
        grau_medio = sum(graus.values()) / self.num_vertices

        with open(caminho_saida, 'w') as f:
            f.write(f"# n = {self.num_vertices}\n")
            f.write(f"# m = {self.num_arestas}\n")
            f.write(f"# d_medio = {grau_medio:.2f}\n")

            distribuicao = defaultdict(int)
            for grau in graus.values():
                distribuicao[grau] += 1

            for grau, freq in sorted(distribuicao.items()):
                f.write(f"{grau} {freq/self.num_vertices:.2f}\n")

    def calcular_graus(self):
        graus = defaultdict(int)
        if self.representacao == "lista":
            for v in range(self.num_vertices):
                graus[v] = len(self.lista_adjacencia[v])
        elif self.representacao == "matriz":
            for v in range(self.num_vertices):
                graus[v] = sum(1 for peso in self.matriz_adjacencia[v] if peso != 0)
        return graus

    def bfs(self, origem, caminho_saida):
        origem -= 1  # Converter para índice
        visitado = [False] * self.num_vertices
        pai = [-1] * self.num_vertices
        nivel = [-1] * self.num_vertices

        fila = deque([origem])
        visitado[origem] = True
        nivel[origem] = 0

        while fila:
            atual = fila.popleft()
            vizinhos = self.obter_vizinhos(atual)
            for vizinho, _ in vizinhos:
                if not visitado[vizinho]:
                    visitado[vizinho] = True
                    pai[vizinho] = atual
                    nivel[vizinho] = nivel[atual] + 1
                    fila.append(vizinho)

        with open(caminho_saida, 'w') as f:
            for v in range(self.num_vertices):
                f.write(f"{v+1} {pai[v]+1 if pai[v]!=-1 else '-'} {nivel[v]}\n")

    def dfs(self, origem, caminho_saida):
        origem -= 1  # Converter para índice
        visitado = [False] * self.num_vertices
        pai = [-1] * self.num_vertices
        nivel = [-1] * self.num_vertices

        def dfs_rec(atual, niv):
            visitado[atual] = True
            nivel[atual] = niv
            for vizinho, _ in self.obter_vizinhos(atual):
                if not visitado[vizinho]:
                    pai[vizinho] = atual
                    dfs_rec(vizinho, niv + 1)

        dfs_rec(origem, 0)

        with open(caminho_saida, 'w') as f:
            for v in range(self.num_vertices):
                f.write(f"{v+1} {pai[v]+1 if pai[v]!=-1 else '-'} {nivel[v]}\n")

    def obter_vizinhos(self, v):
        if self.representacao == "lista":
            return self.lista_adjacencia[v]
        elif self.representacao == "matriz":
            return [(i, self.matriz_adjacencia[v][i]) for i in range(self.num_vertices) if self.matriz_adjacencia[v][i] != 0]

    def componentes_conexos(self, caminho_saida):
        visitado = [False] * self.num_vertices
        componentes = []

        def dfs_comp(v, componente):
            visitado[v] = True
            componente.append(v)
            for vizinho, _ in self.obter_vizinhos(v):
                if not visitado[vizinho]:
                    dfs_comp(vizinho, componente)

        for v in range(self.num_vertices):
            if not visitado[v]:
                componente = []
                dfs_comp(v, componente)
                componentes.append(componente)

        componentes.sort(key=len, reverse=True)

        with open(caminho_saida, 'w') as f:
            f.write(f"Número de componentes: {len(componentes)}\n")
            for i, comp in enumerate(componentes, 1):
                f.write(f"Componente {i}: tamanho={len(comp)}, vértices={[v+1 for v in comp]}\n")
