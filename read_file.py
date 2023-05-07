from db import Eleicao, Estado, Municipio, Zona, Secao, Log, MunicipioZona
import os
import pathlib
import shutil
import py7zr
import datetime


rootdir = os.path.join(pathlib.Path(__file__).parent.resolve(), 'Dados')

columns = ['datetime', 'tipo', 'urna', 'modo', 'descricao', 'hash', 'secao']


for ano in  os.listdir(rootdir):
    path_ano = os.path.join(rootdir, ano)

    
    
    #Para cada turno ele cadastrar uma eleição
    for turno in os.listdir(path_ano):
        path_turno = os.path.join(path_ano, turno) 

        print(
        f"   Eleicão: ", ano, " Turno: ", turno,"\n",
        )


        try:
            eleicao_id = Eleicao.select(Eleicao.id).where(Eleicao.ano == ano, Eleicao.turno == turno).get()
        except:
            eleicao_id = False

        if(not eleicao_id):
            eleicao_id = Eleicao.create(
                ano= ano,
                turno = turno
            )
        
        #Para cada turno ele cadastra os Estados
        for estado in os.listdir(path_turno):
            path_estado = os.path.join(path_turno, estado)
            
            nome_estado, sigla = estado.split(' – ')

            try:
                estado_id = Estado.select(Estado.id).where(Estado.nome == nome_estado, Estado.sigla == sigla, Estado.eleicao == eleicao_id).get()
            except:
                estado_id = False

            if(not estado_id):
                estado_id = Estado.create(
                    nome = nome_estado,
                    sigla = sigla,
                    eleicao = eleicao_id
                )

            

            print(  
                f"    Estado: ", nome_estado, "\n",  
            )

            #Para cada Municipio nos estados
            for municipio in os.listdir(path_estado):
                path_municipio = os.path.join(path_estado, municipio)

                try:
                    municipio_id = Municipio.select(Municipio.id).where(Municipio.nome == municipio, Municipio.estado == estado_id).get()
                except:
                    municipio_id = False

                if(not municipio_id):
                    municipio_id = Municipio.create(
                        nome = municipio,
                        estado = estado_id
                    )

                print(
                    
                    f"     Municipio: ", municipio, "\n",
                    
                )

                #Para cada Zona ele cria a Zona e relaciona as Zonas aos Municipios
                for zona in os.listdir(path_municipio):
                    path_zona = os.path.join(path_municipio, zona)

                    nome_zona = zona.replace("Zona ", '')


                    #checa se a zona já existe antes de cadastrar
                    try:
                        zona_id = Zona.select(Zona.id).where(Zona.nome == nome_zona, Zona.estado == estado_id).get()
                    except:
                        zona_id = False

                    if(not zona_id):
                        zona_id = Zona.create(
                            nome = nome_zona,
                            estado = estado_id
                        )

                    print(
                        
                        f"      Zona: ", zona, "\n",
                        
                    )

                    #relacionar zona ao municipio
                    municipioZona = MunicipioZona.create(
                        municipio = municipio_id,
                        zona = zona_id
                    )

                    #Cadastra cada secão 
                    for secao in os.listdir(path_zona):
                        path_secao = os.path.join(path_zona, secao)

                        nome_secao = secao.replace("Seção ", '')

                        try:
                            secao_id = Secao.select(Secao.id).where(Secao.nome == nome_secao, Secao.zona == zona_id, Secao.municipio == municipio_id).get()
                        except:
                            secao_id = False
                            
                        if(not secao_id):
                            secao_id = Secao.create(
                                nome = nome_secao,
                                zona = zona_id,
                                municipio = municipio_id
                            )

                        

                        print(
                            
                            f"       Secao: ", secao, "\n",
                            
                        )

                        #Extrair o Zip de secao
                        for file in os.listdir(path_secao):
                            if(file.endswith('.zip')):
                                path_zip = os.path.join(path_secao, file)

                                shutil.unpack_archive(path_zip, path_secao)

                                # Descriptografa o Arquivo .logjez
                                for file in os.listdir(path_secao):
                                    if(file.endswith('.logjez')):
                                        path_logjez = os.path.join(path_secao, file)

                                        logjez = py7zr.SevenZipFile(path_logjez, mode='r')
                                        logjez.extractall(path_secao)
                                        logjez.close()

                                        # Ler os Logs do arquivo .dat
                                        for file in os.listdir(path_secao):
                                            if(file.endswith('.dat')):
                                                path_dat = os.path.join(path_secao, file)

                                                with open(path_dat, mode='r') as file:
                                                    for line in file:
                                                        line = line.replace('\n', '')
                                                        dados_log = dict(zip(columns, line.split("\t")))
                                                        dados_log['secao'] = secao_id

                                        

                                                        datahora = datetime.datetime.strptime(dados_log['datetime'], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")


                                                        try:
                                                            log_id = Log.select(Log.id).where(Log.datetime == datahora, Log.tipo == dados_log['tipo'], Log.urna == dados_log['urna'], Log.modo == dados_log['modo'], Log.descricao == dados_log['descricao'], Log.hash == dados_log['hash'], Log.secao == dados_log['secao']).get()
                                                        except:
                                                            log_id = False
                                                            
                                                        if(not log_id):
                                                            log_id = Log.create(
                                                                datetime = datahora,
                                                                tipo = dados_log['tipo'],
                                                                urna = dados_log['urna'],
                                                                modo = dados_log['modo'],
                                                                descricao = dados_log['descricao'],
                                                                hash = dados_log['hash'],
                                                                secao = dados_log['secao'],
                                                            )

                                                         


                                                





            




        



    