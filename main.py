import Tela

# Scraping de animes do site "Anime House".

if __name__ == '__main__':

    Tela.inicio()

'''
Alguns animes para testar todo o funcionamento do scraping são:
    Overlord - Possui 2 parágrafos separados dentro da div e ambos fazem parte da sinopse

    Jujutsu Kaisen - Possui dois nomes em seu título, assim irá demonstrar bem o uso da máscara pra string
    e também não possui TMDb, o que irá demonstrar bem o uso da função "evita_problema()"
'''