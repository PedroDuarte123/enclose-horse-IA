from pathlib import Path
from dataclasses import dataclass
from collections import deque

class No:
    def __init__(self, i, j, rotulo):
        self.i = i
        self.j = j
        self.rotulo = rotulo


@dataclass(frozen=True)
class Ambiente:
	largura: int
	altura: int
	matriz: list[list[str]]
	posicao_cavalo: tuple[int, int] | None

	@classmethod
	def from_txt(cls, caminho_arquivo: str | Path) -> "Ambiente":
		caminho = Path(caminho_arquivo)
		linhas = caminho.read_text(encoding="utf-8").splitlines()

		if not linhas:
			raise ValueError("Arquivo vazio.")

		try:
			largura, altura = map(int, linhas[0].split())
		except ValueError as exc:
			raise ValueError(
				"Primeira linha invalida. Use o formato: 'H V' com dois inteiros."
			) from exc

		if len(linhas) < 1 + altura:
			raise ValueError(
				f"Quantidade de linhas do tabuleiro insuficiente: esperado {altura}, "
				f"recebido {max(0, len(linhas) - 1)}."
			)

		linhas_tabuleiro = linhas[1 : 1 + altura]

		matriz: list[list[str]] = []
		posicao_cavalo: tuple[int, int] | None = None
		for i, linha in enumerate(linhas_tabuleiro):
			if len(linha) != largura:
				raise ValueError(
					f"Linha {i + 2} com tamanho invalido: esperado {largura}, "
					f"recebido {len(linha)}."
				)

			row = list(linha)
			matriz.append(row)

			if "C" in row:
				j = row.index("C")
				posicao_cavalo = (i, j)

		return cls(
			largura=largura,
			altura=altura,
			matriz=matriz,
			posicao_cavalo=posicao_cavalo,
		)

	def __getitem__(self, chave: str):
		"""Compatibilidade com o retorno antigo (dict)."""
		if chave == "largura":
			return self.largura
		if chave == "altura":
			return self.altura
		if chave == "matriz":
			return self.matriz
		if chave == "posicao_cavalo":
			return self.posicao_cavalo
		raise KeyError(chave)

	def printar_matriz(self):
		for linha in self.matriz:
			print("".join(linha))

	def estado_inicial(self):
		"""Retorna o estado inicial do tabuleiro, que é a posição do cavalo."""
		return self.posicao_cavalo

	def e_estado_final(self, no) -> bool:
		"""Verifica se o nó está numa borda pisável.

		Mantém a mesma regra do código anterior: considera objetivo apenas
		células rotuladas por ' ', 'A', 'J' ou 'M' nas bordas.
		"""
		i = no.i
		j = no.j
		rotulo = getattr(no, "rotulo", self.matriz[i][j])
		if rotulo == " " or rotulo == "A" or rotulo == "J" or rotulo == "M":
			if i == 0 or i == self.altura - 1 or j == 0 or j == self.largura - 1:
				return True
		return False
	
	def funcao_transicao(self, no):
		i, j = no.i, no.j
		estados = []
		obstaculos = {"%", "+"}
		if i + 1 < self.altura and self.matriz[i + 1][j] not in obstaculos: # baixo
			estados.append(No(i + 1, j, self.matriz[i + 1][j]))
		if i - 1 >= 0 and self.matriz[i - 1][j] not in obstaculos: # cima
			estados.append(No(i - 1, j, self.matriz[i - 1][j]))
		if j + 1 < self.largura and self.matriz[i][j + 1] not in obstaculos: # direita
			estados.append(No(i, j + 1, self.matriz[i][j + 1]))
		if j - 1 >= 0 and self.matriz[i][j - 1] not in obstaculos: # esquerda
			estados.append(No(i, j - 1, self.matriz[i][j - 1]))

		return estados
	
	def calcular_pontuacao(self):
		if self.posicao_cavalo is None:
			raise ValueError("Não encontrei 'C' no tabuleiro.")

		obstaculos = {"%", "+"}
		fila = deque([self.posicao_cavalo])
		visitados = {self.posicao_cavalo}

		pontuacao = 0

		while fila:
			i, j = fila.popleft()
			celula = self.matriz[i][j]

			# +1 por cada célula alcançável (inclui J/M/A e a posição do cavalo)
			pontuacao += 1
			if celula == "J":
				pontuacao += 3
			elif celula == "M":
				pontuacao += 10
			elif celula == "A":
				pontuacao -= 5

			for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
				ni, nj = i + di, j + dj
				if 0 <= ni < self.altura and 0 <= nj < self.largura:
					if (ni, nj) not in visitados and self.matriz[ni][nj] not in obstaculos:
						visitados.add((ni, nj))
						fila.append((ni, nj))

		return pontuacao



def carregar_ambiente_txt(caminho_arquivo):
	"""Le um arquivo de estado e retorna um `Ambiente`.

	Formato esperado:
	- Primeira linha: "H V"
	- Proximas V linhas: cada uma com H caracteres do tabuleiro

	Obs.: `Ambiente` mantém compatibilidade com o retorno antigo via
	`ambiente["matriz"]`, `ambiente["altura"]`, etc.
	"""
	return Ambiente.from_txt(caminho_arquivo)


def printar_matriz(matriz):
	for linha in matriz:
		print("".join(linha))

def estado_inicial(matriz):
	"""Retorna o estado inicial do tabuleiro, que é a posição do cavalo."""
	for i, linha in enumerate(matriz):
		for j, celula in enumerate(linha):
			if celula == "C":
				return (i, j)
			

def e_estado_final(no, ambiente: Ambiente):
	"""Wrapper para usar `Ambiente.e_estado_final` sem passar altura/largura."""
	return ambiente.e_estado_final(no)








