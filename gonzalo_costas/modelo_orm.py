from peewee import *

db = SqliteDatabase("Obras_urbanas.db", pragmas={"journal_mode": "wal"})

class BaseModel(Model):
    class Meta:
        database = db

class TipoEntorno(BaseModel):
    id_obra = AutoField(unique=True)
    nombre = CharField()
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'tipo_entorno'


class IndentificacionObra(BaseModel):
    id_identificacion_obra = AutoField(unique=True)
    tipo_entorno = ForeignKeyField(TipoEntorno, backref='tipo_entorno')
    nombre = CharField()
    etapa = CharField()
    area_responsable = CharField()
    descripcion = CharField()
    monto_contrato = CharField()
    def __str__(self):
        pass
    class Meta:
        db_table = 'Identificacion_obra'

class UbicacionObra(BaseModel):
    comuna = CharField()
    barrio = CharField()
    direccion = CharField()
    latitud = CharField()
    longitud = CharField()

class TiemposObra(BaseModel):
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = CharField()
    porcentaje_valance = CharField()
    imagen_1 = CharField()
    imagen_2 = CharField()
    imagen_3 = CharField()
    imagen_4 = CharField()

class LicitacionesObra(BaseModel):
    licitacion_oferta_empresa = CharField()
    licitacion_anio = CharField()

class ContratistasObra(BaseModel):
    contratacion_tipo = CharField()
    nro_contratacion = CharField()
    cuit_contratista = CharField()
    beneficiario = CharField()
    mano_obra = CharField()
    compromiso = CharField()

class expedientesObra(BaseModel):

    expediente_numero = CharField()
    destacada = CharField()
    ba_elije = CharField()
    pliego_descarga = CharField()
   
class Doc_ambiental(BaseModel):
    estudio_ambiental_descarga = CharField()

class Financiamiento(BaseModel):
    financiamiento = CharField()
        

db.create_tables([TipoEntorno,IndentificacionObra,UbicacionObra, TiemposObra, LicitacionesObra, ContratistasObra, expedientesObra, Doc_ambiental, Financiamiento])


    


