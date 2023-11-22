from peewee import *
from datetime import datetime

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


class ObrasPublicas(BaseModel):
    id_identificacion_obra = AutoField(unique=True)
    tipo_entorno = ForeignKeyField(TipoEntorno, backref='tipo_entorno', null = True)
    nombre = CharField(null = True)
    etapa = CharField(null = True)
    tipo = CharField(null = True)
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
    contratacion_tipo = CharField(null = True)
    nro_contratacion = CharField(null = True)
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

class Etapas(BaseModel):
    etapa = CharField(unique=True)

    def __str__(self):
        return self.etapa
    
    class Meta:
        db_table = 'Etapas'


class TipoContratacion(BaseModel):
    nro_contratacion = CharField(unique=True)

    def __str__(self):
        return self.nro_contratacion
    
    class Meta:
        db_table = 'Tipo_contratacion'
    

class Empresa(BaseModel):
    nro_expediente = CharField(unique=True)

    def __str__(self):
        return self.nro_expediente
    
    class Meta:
        db_table = 'Empresa'

class Obra():

    def __init__(self, etapas, tipo_obra,area_del_responsable, barrio, empresa, nro_expediente, destacada, mano_obra, porcentaje_avance):
        
        self.etapas= etapas
        self.tipo_obra = tipo_obra
        self.area_responsable = area_del_responsable
        self.barrio = barrio
        #self.nro_contratacion = nro_contratacion
        self.empresa = empresa
        self.nro_expediente = nro_expediente
        self.destacada = destacada 
        self.mano_obra = mano_obra
        self.porcentaje_avance = porcentaje_avance

    def nuevo_proyecto(self):
        try:
            ObrasPublicas.create(etapa = self.etapas, tipo=self.tipo_obra,area_responsable= self.area_responsable, barrio=self.barrio)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)

    def iniciar_contratacion(self):
        try:
            ObrasPublicas.create(nro_contratacion = self.nro_contratacion)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)

    def adjudicar_obra(self):
        try:
            ObrasPublicas.create(empresa = self.empresa, expediente_numero = self.nro_expediente)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)
        

    def iniciar_obra(self):
        self.fecha_inicio = datetime.now()
        try:
            ObrasPublicas.create(destacada = self.destacada, mano_obra = self.mano_obra, fecha_inicio = self.fecha_inicio)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)

    def actualizar_porcentaje_avance(self):
        try:
            ObrasPublicas.create(porcentaje_avance = self.porcentaje_avance)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)   

    def incrementar_plazo(self):
        try:
            ObrasPublicas.create(plazo_meses = self.plazo_meses)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)

    def incrementar_mano_obra(self):
        try:
            ObrasPublicas.create(mano_obra = self.mano_obra)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)

    def finalizar_obra(self):
        #Para indicar la finalización de una obra, se debe invocar al método finalizar_obra() y
        #actualizar el valor del atributo etapa a “Finalizada” y del atributo porcentaje_avance a “100”.
        self.etapas = ObrasPublicas.get(ObrasPublicas.etapa == 'Finalizacion')
        if self.etapas == "Finalizacion":
            self.porcentaje_avance == "100"
        try:
            ObrasPublicas.create(etapa = self.etapas, porcentaje_avance = self.porcentaje_avance)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)

            

    def rescindir_obra(self):
     #Para indicar la rescisión de una obra, se debe invocar al método rescindir_obra() y
     #actualizar el valor del atributo etapa a “Rescindida”.
        self.etapa_rescindida = Etapas(etapa = 'Rescindida')
        try:
            ObrasPublicas.create(etapa = self.etapa_rescindida)
        except IntegrityError as e:
            print("Error al insertar en la tabla.", e)


