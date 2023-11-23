from peewee import *
from datetime import datetime

db = SqliteDatabase("Obras_urbanas.db", pragmas={"journal_mode": "wal"})

class BaseModel(Model):
    class Meta:
        database = db

class TipoEntorno(BaseModel):
    id_entorno = AutoField(unique=True)
    nombre = CharField()
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'tipo_entorno'

class Etapas(BaseModel):
    nombre = CharField(unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'Etapas'

class TipoObra(BaseModel):
    nombre = CharField(unique=True)

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'tipo_obra'

class TipoContratacion(BaseModel):
    nombre = CharField(unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'Tipo_contratacion'

class Empresa(BaseModel):
    nombre = CharField(unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'Empresa'


class ObrasPublicas(BaseModel):
    entorno = ForeignKeyField(TipoEntorno, backref='tipo_entorno', null = True)
    nombre = CharField(null = True)
    etapa = ForeignKeyField(Etapas, backref='Etapas', null = True)
    tipo = ForeignKeyField(TipoObra, backref='tipo_obra', null = True)
    area_responsable = CharField(null = True)
    descripcion = CharField(null = True)
    monto_contrato = CharField(null = True)
    comuna = CharField(null = True)
    barrio = CharField(null = True)
    direccion = CharField(null = True)
    latitud = CharField(null = True)
    longitud = CharField(null = True)
    fecha_inicio = DateField(null = True)
    fecha_fin_inicial = DateField(null = True)
    plazo_meses = CharField(null = True)
    porcentaje_valance = CharField(null = True)
    imagen_1 = CharField(null = True)
    imagen_2 = CharField(null = True)
    imagen_3 = CharField(null = True)
    imagen_4 = CharField(null = True)
    licitacion_oferta_empresa = CharField(null = True)
    licitacion_anio = CharField(null = True)
    contratacion_tipo = CharField
    nro_contratacion = ForeignKeyField(TipoContratacion, backref='tipo_contratacion', null = True)
    cuit_contratista = CharField(null = True)
    beneficiario = CharField(null = True)
    mano_obra = CharField(null = True)
    compromiso = CharField(null = True)
    empresa = CharField(null = True)
    expediente_numero = CharField(null = True)
    destacada = CharField(null = True)
    ba_elije = CharField(null = True)
    pliego_descarga = CharField(null = True)
    estudio_ambiental_descarga = CharField(null = True)
    #valor agreagado
    fuente_financiamiento = CharField(null = True)
    porcentaje_avance = CharField(null = True)
    financiamiento = CharField(null = True)

    def __str__(self):
        pass
    class Meta:
        db_table = 'Obras_publicas'


class Obra():

    def __init__(self, etapas, tipo_obra, area_del_responsable, barrio, nro_contratacion):
        
        self.etapas= etapas
        self.tipo_obra = tipo_obra
        self.area_responsable = area_del_responsable
        self.barrio = barrio
        self.nro_contratacion = nro_contratacion
        #self.empresa = empresa
        #self.nro_expediente = nro_expediente
        #self.destacada = destacada 
        #self.mano_obra = mano_obra
        #self.porcentaje_avance = porcentaje_avance

    def nuevo_proyecto(self):
        try:
            id_etapa = Etapas.select(Etapas.id).where(Etapas.nombre == self.etapas).get()
            id_tipo = TipoObra.select(TipoObra.id).where(TipoObra.nombre== self.tipo_obra).get()
            ObrasPublicas.create(etapa_id = id_etapa, tipo_id = id_tipo, area_responsable = self.area_responsable, barrio = self.barrio)

        except DoesNotExist as e:
            print("El valor no existe en la BD")
            Etapas.create(nombre="Proyecto")
            print('Valor ya creado')
            id_etapa = Etapas.select(Etapas.id).where(Etapas.nombre == self.etapas).get()
            id_tipo = TipoObra.select(TipoObra.id).where(TipoObra.nombre== self.tipo_obra).get()
            ObrasPublicas.create(etapa_id = id_etapa, tipo_id = id_tipo, area_responsable = self.area_responsable, barrio = self.barrio)

    def iniciar_contratacion(self):
        try:
            id_nro_contratacion = TipoContratacion.select(TipoContratacion.id).where(TipoContratacion.nombre == self.nro_contratacion).get()
            ObrasPublicas.create(nro_contratacion_id = id_nro_contratacion)

        except DoesNotExist as e:
            print("El valor no existe en la BD")
            TipoContratacion.create(nombre=self.nro_contratacion)
            print('Valor ya creado')
            id_nro_contratacion = TipoContratacion.select(TipoContratacion.id).where(TipoContratacion.nombre == self.nro_contratacion).get()
            ObrasPublicas.create(nro_contratacion_id = id_nro_contratacion)

    def adjudicar_obra(self):
        pass

    def iniciar_obra(self):
        pass

    def actualizar_porcentaje_avance(self):
        pass

    def incrementar_plazo(self):
        pass
    def incrementar_mano_obra(self):
       pass

    def finalizar_obra(self):
        #Para indicar la finalización de una obra, se debe invocar al método finalizar_obra() y
        #actualizar el valor del atributo etapa a “Finalizada” y del atributo porcentaje_avance a “100”.
        pass

            

    def rescindir_obra(self):
     #Para indicar la rescisión de una obra, se debe invocar al método rescindir_obra() y
     #actualizar el valor del atributo etapa a “Rescindida”.
        pass


