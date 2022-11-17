from bs4 import BeautifulSoup
import requests
from time import sleep
import os

clear = lambda: os.system('cls')
animeTitulos = []
url_site = 'https://animeshouse.net/anime/'

def inicio():
  aviso()
  titulo_desejado()
  pedir_outra_obra()
  buscar_informações()

  print('Finalizada toda a lista.')


# Aviso para não dar problemas no scraping.
def aviso():
  clear()
  print('Caso dê algum erro na busca da obra, segue-se os motivos possíveis:')
  print('#1 - A obra não está disponível no site!')
  print('#2 - O nome da obra foi digitado incorretamente, verifique a ortografia!')
  print('#3 - Algumas obras possuem pontuações em seus títulos, digite somente as letras!')
  print('#4 - O nome da obra está incompleto e foi associada à um filme ou OVA da franquia!')
  input('\nPressione qualquer tecla para continuar.')


# Função para o usuário informar a obra que quer.
def titulo_desejado():
  clear()
  titulo = input('Sobre que obra deseja saber? ')
  animeTitulos.append(titulo)


# Função para a opção de adicionar outra obra na lista.
def pedir_outra_obra():
  clear()
  resposta = input('Deseja saber sobre outra(s) obra(s)? [Y/N] ')
  
  if resposta.upper() != 'Y' and resposta.upper() != 'N':
    print("\nFavor responder apenas com 'Y' ou 'N'! ")
    input('Pressione qualquer tecla para continuar. ')
    pedir_outra_obra()

  elif resposta.upper() == 'Y':
    clear()
    titulo_desejado()
    pedir_outra_obra()


# Mostra o conteúdo do array que guarda as obras informadas.
def lista_das_obras():
  for i in animeTitulos:
    print(i)


# Formatação do nome da obra para ser inserida na url corretamente.
def formatar_nome(obra):
  nome_formatado = obra.lower().strip().replace(' ', '-')
  return nome_formatado


# Busca e extração de informações no site.
def buscar_informações():
  clear()   
  for obra in animeTitulos:

    url_obra = '{}/{}'.format(url_site, formatar_nome(obra))
    soup = BeautifulSoup(requests.get(url_obra).text, 'html5lib')

    titulo = extrai_titulo(soup)
    titulo_original = extrai_titulo_original(soup)
    sinopse = extrai_sinopse(soup)
    data_estreia = extrai_data_estreia(soup)
    qtd_temporadas = extrai_qtd_temporadas(soup)
    qtd_episodios = extrai_qtd_episodios(soup)

    print('Obra: {}'.format(titulo))
    criar_arquivo(titulo, titulo_original, sinopse, data_estreia, qtd_temporadas, qtd_episodios)

    sleep(20)


# Algumas obras inda não possuem TMDb, diminuindo assim uma classe no html.
# Essa função serve para não dar erro na iteração nesse caso.
def evita_problema(soup):
  div_das_informações = soup.find_all('div', {'class' : 'custom_fields'})
  if len(div_das_informações) == 4:
    return 1
  return 0


# Extração do título da obra.
def extrai_titulo(soup):
  for h1 in soup('h1'):
    if not h1.get('class'):
      return h1.text


# Extração do título original da obra (seja ele em inglês, japonês, etc).
def extrai_titulo_original(soup):
  div_das_informações = soup('div', {'class' : 'custom_fields'})[0]
  span_das_informações = div_das_informações('span', {'class' : 'valor'})[0]
  titulo_original = span_das_informações.text

  return titulo_original


# Extração da Data de lançamento.
def extrai_data_estreia(soup):
  div_das_informações = soup('div', {'class' : 'custom_fields'})[2 - evita_problema(soup)]
  span_das_informações = div_das_informações('span', {'class' : 'valor'})[0]
  data_estreia = span_das_informações.text

  return data_estreia


# Extração da quantidade de temporadas.
def extrai_qtd_temporadas(soup):
  div_das_informações = soup('div', {'class' : 'custom_fields'})[3 - evita_problema(soup)]
  span_das_informações = div_das_informações('span', {'class' : 'valor'})[0]
  qtd_temporadas = span_das_informações.text

  return qtd_temporadas


# Extração da quantidade de episódios.
def extrai_qtd_episodios(soup):
  div_das_informações = soup('div', {'class' : 'custom_fields'})[4 - evita_problema(soup)]
  span_das_informações = div_das_informações('span', {'class' : 'valor'})[0]
  qtd_episodios = span_das_informações.text

  return qtd_episodios


# Extração da sinopse da obra.
def extrai_sinopse(soup):
  sinopse = []
  div_da_sinopse = soup('div', {'class' : 'wp-content'})[0]
  sinopse_com_tag = div_da_sinopse.find_all('p')
  for p in sinopse_com_tag:
    sinopse.append(p.text)

  return sinopse


# Criação do arquivo da obra com suas informações.
''' Por conta da maioria das obras terem os títulos originais escritos com kanjis ("letras" japonesas),
    é necessário utilizar "enconding='utf-8'" para que não dê erro na hora guardar no bloco de notas. '''

def criar_arquivo(titulo, titulo_original, sinopse, data_estreia, qtd_temporadas, qtd_episodios):
  with open('Informações {}.txt'.format(titulo), 'w', encoding='utf-8') as file:
    file.write('{}\n'.format(titulo))
    file.write('\nTitulo Original: {}\n'.format(titulo_original))
    file.write('\nData de estreia: {}\n'.format(data_estreia))
    file.write('\nTemporadas: {}\n'.format(qtd_temporadas))
    file.write('\nEpisódios: {}\n'.format(qtd_episodios))
    file.write('\n')
    
    file.write('Sinopse da obra:\n')
    for p in sinopse:
      file.write('\t{}\n'.format(p))