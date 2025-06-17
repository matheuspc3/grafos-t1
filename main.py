from grafo import Grafo

def main():
    grafo = Grafo(representacao="lista")  
    grafo.carregar_arquivo("entrada.txt")
    grafo.salvar_info_grafo("info_saida.txt")
    grafo.bfs(origem=1, caminho_saida="bfs_saida.txt")
    grafo.dfs(origem=1, caminho_saida="dfs_saida.txt")
    grafo.componentes_conexos(caminho_saida="componentes_saida.txt")

if __name__ == "__main__":
    main()
