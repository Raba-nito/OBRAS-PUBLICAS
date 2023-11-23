import pandas as pd
from modelo_orm import *
from abc import ABC


class GestionarObra(ABC):
    df = None
    df_limpio = None

    @classmethod
    def extraer_datos(cls):
        """CSV de Obras Publicas"""
    
        archivo_csv = "gonzalo_costas/observatorio-de-obras-urbanas.csv"

        try:
            cls.df = pd.read_csv(archivo_csv, sep=",", encoding='utf8')
            return True
        except FileNotFoundError as e:
            print("Error al conectar con el dataset.", e)
            return False

    @classmethod
    def limpiar_datos(cls):
        cls.extraer_datos()
        cls.df.dropna(subset=['entorno', 'nombre','etapa', 'tipo','contratacion_tipo','licitacion_oferta_empresa', 'estudio_ambiental_descarga'],axis = 0, inplace = True)
        data_unique_entorno= list(cls.df['entorno'].unique())
        data_unique_etapas= list(cls.df['etapa'].unique())
        data_unique_tipo= list(cls.df['tipo'].unique())
        data_unique_nro_contratacion= list(cls.df['nro_contratacion'].unique())


        cls.df_limpio_entorno = data_unique_entorno
        cls.df_limpio_etapas = data_unique_etapas
        cls.df_limpio_tipo = data_unique_tipo
        cls.df_limpio_nro_contratacion = data_unique_nro_contratacion

    @classmethod
    def conectar_db(cls):
        try:
            print('base de datos conectada')
            cls.db = db.connect()
        except OperationalError as e:
            print("Error al conectar con la BD.", e)
            exit()
        
    @classmethod
    def mapear_orm(cls):
        db.create_tables([TipoEntorno,ObrasPublicas, Etapas,TipoObra ,TipoContratacion, Empresa])

    @classmethod
    def cargar_datos(cls):
        
        for elem in cls.df_limpio_entorno:
            print("Elemento:", elem)
            try:
                TipoEntorno.create(nombre=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla tipo entorno", e)

        for elem in cls.df_limpio_etapas:
            print("Elemento:", elem)
            try:
                Etapas.create(nombre=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla tipo etapas", e)

        for elem in cls.df_limpio_tipo:
            print("Elemento:", elem)
            try:
                TipoObra.create(nombre=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla tipo entorno", e)

        for elem in cls.df_limpio_nro_contratacion:
            print("Elemento:", elem)
            try:
                TipoContratacion.create(nombre=elem)
                #Empresa.create(nombre=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla tipo entorno", e)
        print("Se han persistido los tipos de transporte en la BD.")

        print("Recorremos las filas del archivo csv e insertamos los valores en la tabla 'ObrasPublicas' de la BD")
        
        for elem in cls.df.values:
            tipo_entorn= TipoEntorno.get(TipoEntorno.nombre == elem[1])
            tipo_etapas = Etapas.get(Etapas.nombre == elem[3])
            tipo_obra = TipoObra.get(TipoObra.nombre == elem[4])
            tipo_nro_contratacion = TipoContratacion.get(TipoContratacion.nombre==elem[24])
            try:
                ObrasPublicas.create(tipo_entorno=tipo_entorn,etapa=tipo_etapas,
                                    tipo = tipo_obra, contratacion_tipo = elem[23],
                                    nombre=elem[2],area_responsable = elem[5],
                                    descripcion=elem[6], monto_contrato=elem[7],
                                    comuna =elem[8], barrio =elem[9], direccion = elem[10],
                                    latitud = elem[11],longitud = elem[12],
                                    fecha_inicio = elem[13], fecha_fin_inicial = elem[14], plazo_meses = elem[15],
                                    porcentaje_valance = elem[16],
                                    imagen_1 = elem[17], imagen_2 = elem[18], imagen_3 = elem[19],imagen_4 = elem[20],
                                    licitacion_oferta_empresa = elem[21],
                                    licitacion_anio = elem[22],
                                    nro_contratacion = tipo_nro_contratacion,
                                    cuit_contratista = elem[25],
                                    beneficiario = elem[26],
                                    mano_obra = elem[27],
                                    compromiso = elem[28],
                                    expediente_numero = elem[29],
                                    destacada = elem[30],
                                    ba_elije = elem[31],
                                    pliego_descarga = elem[32],
                                    estudio_ambiental_descarga = elem[33],
                                    financiamiento = elem[34]
                                        )
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla viajes.", e)

    @classmethod
    def nueva_obra(cls):
        obra1 = Obra('Proyecto','Escuelas', 'Ministerio de Educación', 'Belgrano','2016-01-0007-00')
        obra1.nuevo_proyecto()
        obra1.iniciar_contratacion()

        #'2016-01-0007-00', '120', '50'

prueba1 = GestionarObra()
prueba1.limpiar_datos()
prueba1.conectar_db
prueba1.mapear_orm()
prueba1.cargar_datos()
prueba1.nueva_obra()
