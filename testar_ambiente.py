from pathlib import Path

from ambiente import carregar_ambiente_txt


def main() -> None:
    ambiente = carregar_ambiente_txt(Path("estados/entice.txt"))
    for linha in ambiente["matriz"]:
        print("".join(linha))


if __name__ == "__main__":
    main()
