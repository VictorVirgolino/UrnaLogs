# UrnaLogs
## O UrnaLogs é uma ferramenta desenvolvida em Python que oferece uma solução completa para extrair, estruturar e visualizar os dados contidos nos logs das urnas eletrônicas disponibilizados pelo TSE. 

### Tabela de conteúdos
### ===================
<!--ts-->
* [Sobre](#Sobre)
* [Tabela de Conteudo](#tabela-de-conteudo)
* [Pre Requisitos](#pre-requisitos)
* [Instalação](#instalacao)
* [Como usar](#como-usar)
    * [Módulo de Web Scraping](#web-scraping)
    * [Módulo de ETL](#etl)
    * [Módulo de Persistência](#persistencia)
    * [Módulo de Dashboard](#dashboard)
* [Exemplos](#exemplos)
<!--te-->


### Pré-requisitos
Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

* [Git](https://git-scm.com)
* [Python](https://www.python.org/downloads/)
* [Chrome](https://www.google.com/intl/pt-BR/chrome/)
* [VSCode](https://code.visualstudio.com/)
* [Banco de Dados Compativel com Peewee ORM (SQLite, MySQL, Postgres)](https://docs.peewee-orm.com/en/latest/peewee/database.html#:~:text=Peewee%20comes%20with%20support%20for,%2C%20database%2Dspecific%20configuration%20options.&text=Peewee%20provides%20advanced%20support%20for,via%20database%2Dspecific%20extension%20modules.)
* [Docker](https://docs.docker.com/desktop/install/windows-install/)

Para facilitar, o projeto já vem com um arquivo docker-compose.yml com a configuração da instalação e configuração de uma imagem de um banco Postgres utilizando a ferramenta Docker, o link  possui um passo a passo da ferramenta para plataformas windows.
### Instalação
```bash
# Clone este repositório
git clone https://github.com/VictorVirgolino/UrnaLogs

# Acesse a pasta do projeto no terminal/cmd
cd Urnalogs

#instalar as bibliotecas necessárias com o PIP
pip install -r requirements.txt
```

O arquivo db.py possui a configuração do ORM, é neste arquivo que se pode configurar qual o banco de dados a ser utilizado, por padrão é utilizado uma imagem Docker do Postgres.
Após configurado o banco de dados, deve-se rodar o arquivo db.py para criação das tabelas e conexão com o ORM.
```bash
#Após instalar o banco de dados, criar as tabelas, é necessário descomentar a linha para criação das tabelas apenas a primeira vez.
python db.py
```

é necessário baixar o driver chrome compatível com a sua versão do navegador, segua o passo a passo a seguir:

Passo 1 - Onde encontrar a versão do seu navegador Chrome

![Passo 1](/imagens/passo%20a%20passo/1-onde%20encontrar%20a%20vers%C3%A3o.png "Passo 1 - Onde encontrar a versão")

Passo 2 - Versão do Chrome

![Passo 2](/imagens/passo%20a%20passo/2-versao.png "Passo 2 - versão do chrome")
Passo 3 - Acessar o site o driver chrome abaixo

[Driver chrome](https://chromedriver.chromium.org/downloads)

![Passo 3](/imagens/passo%20a%20passo/3-baixar%20o%20driver%20do%20chromium%20compativel.png "Passo 3 - site do driver chrome")

Passo 4 - Baixar versão windows do chrome driver

![Passo 4](/imagens/passo%20a%20passo/4-versao%20de%20windows.png "Passo 4 - baixar o driver chrome compátivel")

Passo 5 - Usar o terminal/cmd e encontrar o caminho da pasta onde está instalado o Python basta usar o comando abaixo:
```bash
 #Encontrar a pasta onde está instalado o python no seu sistema
 where python
```

![Passo 5](/imagens/passo%20a%20passo/5-onde%20est%C3%A1%20o%20python.png "Passo 5 - onde está o Python")

Passo 6 - Extrair do zip o arquivo chromedriver.exe e copiar para a pasta do python

![Passo 6](/imagens/passo%20a%20passo/6-copiar%20o%20chrome%20driver.png "Passo 6 - copiar o driver para a pasta do python")

Sempre que seu navegador for atualizado é necessário baixar a versão compátivel e substituir o chromedriver.exe na pasta do python.


#### Como saber a versão do Chrome


### Como usar
O UrnaLogs é divido em 4 módulos que podem ser usados separadamente ou em conjunto para extrair, estruturar e visualizar os dados das urnas eletrônicas.
#### Módulo de Web Scraping
O módulo de Web Scraping é responsável por extrair os arquivos comprimidos contendo os logs das urnas de uma eleição e os salvando de hieraquica na pasta no computador.
Para usa-lo, precisa primeiramente selecionar qual eleição se está interresado, selecionar dados da urna da eleição, e copiar a url para substituir o valor da variável turno do script log.py.
![Setar eleicao](/imagens/passo%20a%20passo/setar%20eleicao.png "Setar a eleição")
Por default a url corresponde ao primeiro turno das eleições 2022.
Além disso é possivel selecionar qual é o estado, municipio, zona e seção que o módulo  deve começar.

O numeros corresponde a posição do estado, municipio, zona e seção da sua lista de dropdown. No caso de zona e seção se adiciona +1(começa do 2).

É importante criar uma pasta "Workstation" dentro da pasta do Urnalogs
```bash
#criar a pasta workstation
mkdir Workstation
```

Tendo setado a eleição, os parametros de entrada e criado a pasta Workstation basta roda o script log.py
```bash
#rodar o módulo de web scraping
python log.py
```

O resultado será os arquivos comprimidos sendo salvos na pasta workstation na hieraquia estado, municipio, zona, seção:

![diagrama arquivos](/imagens/passo%20a%20passo/diagrama%20de%20arquivos.png "diagrama de arquivos")


#### Módulo de ETL
Em seguida o módulo de ETL ira ler e inserir os logs no módulo de presistência.
Para isso primeiramente é preciso criar um pasta "Dados" na pasta UrnaLogs e criar duas pasta um,a dentro da outra com o ano e o turno referente a eleição selecionada.
```bash
#criar a pasta Dados
mkdir Dados
#entra na pasta Dados
cd Dados
#criar uma pasta com o ano da eleição
mkdir 2022
#entra na pasta do ano
cd 2022
#criar uma pasta referente ao turno
mkdir 1
```
Em seguida se copia as pastas no workstation para dentro da pasta do turno.

Tendo feito isso, basta rodar o script read_file.py
```bash
#rodar o módulo de web scraping
python read_file.py
```

#### Módulo de Persistência
O módulo de persistência corresponde ao banco de dados selecionado para reter as informações dos logs das urnas.
É possivel ter acesso aos dados diretamente no banco de dados através do uso de um SGBD.
No caso da opção padrão do uso do banco Postgres, recomendo o uso da ferramenta DBeaver pois ele oferece uma forma fácil e compelta de navegar pelos dados e fazer consultas.

[DBeaver](https://dbeaver.io/)

#### Módulo de Dashboard
O módulo de dashboard permite uma alternativa fácile interativa de explorar os dados contidos no módulo de persistência,
o notebook python dashboard_secao permite gerar gráficos histogramas,dispersão e de calor corelacionando as informações das seções.

Para utilizar pasta abrir o notebook "dashboard_secao.ipynb" utilizando o vscode ou seu editor de preferência.
Ele utiliza o ORM Peewee para realizar as consultas e plotar os graficos.


### Exemplos
Segue alguns exemplos de graficos que podem ser gerados com o uso da ferramenta:

Histograma Erros na Votação

![grafico 1](/imagens/grafico/erros%20na%20vota%C3%A7%C3%A3o.png "histograma erros na votação")

Dispersão Tempo de Votação X Erros na Votação

![grafico 2](/imagens/grafico//tempo%20na%20urna%20x%20erros%20na%20vota%C3%A7%C3%A3o2.png "dispersao tempo de votação X erros na votação")

Calor Votos por Hora

![grafico 3](/imagens/grafico/calor%20votos.png "calor votos por hora")



