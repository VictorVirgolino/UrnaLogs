
from peewee import SqliteDatabase, Model, TextField, ForeignKeyField, DateTimeField, IntegerField, ManyToManyField
from datetime import datetime
# from playhouse.migrate import migrate, SchemaMigrator
from playhouse.postgres_ext import PostgresqlExtDatabase
import psycopg2

# conn = psycopg2.connect(
#    database="postgres", user='admin', password='eleicoes_db', host='127.0.0.1', port= '5434'
# )
# conn.autocommit = True

# #Creating a cursor object using the cursor() method
# cursor = conn.cursor()

# #Preparing query to create a database
# sql = '''CREATE database eleicoes''';

# #Creating a database
# cursor.execute(sql)
# print("Database created successfully........")

# #Closing the connection
# conn.close()


db = PostgresqlExtDatabase(database='eleicoes', user="admin", password="eleicoes_db", host="localhost", port=5434)

# db = SqliteDatabase('teste.db')

class BaseModel(Model):
    class Meta:
        database = db

class Eleicao(BaseModel):
    ano = TextField()
    turno = IntegerField()

class Estado(BaseModel):
    nome = TextField()
    sigla = TextField()
    eleicao = ForeignKeyField(Eleicao, backref='estados')

class Municipio(BaseModel):
    nome = TextField()
    estado = ForeignKeyField(Estado, backref='municipios', )

class Zona(BaseModel):
    nome = TextField()
    estado = ForeignKeyField(Estado, backref='zonas')

class MunicipioZona(BaseModel):
    municipio = ForeignKeyField(Municipio)
    zona = ForeignKeyField(Zona)

class Secao(BaseModel):
    nome = TextField()
    zona = ForeignKeyField(Zona, backref='secoes')
    municipio = ForeignKeyField(Municipio, backref='secoes')

class Log(BaseModel):

    datetime = DateTimeField()
    tipo = TextField()
    urna = TextField()
    modo = TextField()
    descricao = TextField()
    hash = TextField()
    secao = ForeignKeyField(Secao, backref='logs')


# db.drop_tables([Eleicao, Estado, Municipio, Zona, Secao, Log, MunicipioZona])

# db.create_tables([Eleicao, Estado, Municipio, Zona, Secao, Log, MunicipioZona])