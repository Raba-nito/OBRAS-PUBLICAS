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
        cls.df.dropna(subset=['entorno', 'nombre','etapa', 'tipo', 'comuna', 'direccion','licitacion_oferta_empresa', 'licitacion_anio', 'estudio_ambiental_descarga'],axis = 0, inplace = True)
        data_unique_entorno= list(cls.df['entorno'].unique())
        
        cls.df_limpio = data_unique_entorno

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
        db.create_tables([TipoEntorno,ObrasPublicas, Etapas, TipoContratacion, Empresa])

    @classmethod
    def cargar_datos(cls):
        for elem in cls.df_limpio:
            print("Elemento:", elem)
            try:
                TipoEntorno.create(nombre=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla tipo entorno", e)
        print("Se han persistido los tipos de transporte en la BD.")

        print("Recorremos las filas del archivo csv e insertamos los valores en la tabla 'ObrasPublicas' de la BD")
        
        for elem in cls.df.values:
            tipo_entorn= TipoEntorno.get(TipoEntorno.nombre == elem[1])
            try:
                ObrasPublicas.create(tipo_entorno=tipo_entorn,id_obra=elem[1], 
                                        nombre=elem[2], etapa=elem[3], tipo = elem[4], area_responsable = elem[5],
                                        descripcion=elem[6], monto_contrato=elem[7],
                                        comuna =elem[8], barrio =elem[9], direccion = elem[10],
                                        latitud = elem[11],longitud = elem[12],
                                        fecha_inicio = elem[13], fecha_fin_inicial = elem[14], plazo_meses = elem[15],
                                        porcentaje_valance = elem[16],
                                        imagen_1 = elem[17], imagen_2 = elem[18], imagen_3 = elem[19],imagen_4 = elem[20],
                                        licitacion_oferta_empresa = elem[21],
                                        licitacion_anio = elem[22],
                                        contratacion_tipo = elem[23],
                                        nro_contratacion = elem[24],
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
        
        etapa_proyecto = Etapas(etapa='Proyecto')
        etapa_en_ejecucion = Etapas(etapa='En ejecucion')
        etapa_finalizacion = Etapas(etapa='Finalizacion')

        #nro_contratacion1 = TipoContratacion(nro_contratacion = 'Licitacion publica')
        
        nro_expediente_si = Empresa(nro_expediente = 'SI')
        nro_expediente_no= Empresa(nro_expediente = 'NO')

        try:
            etapa_proyecto.save()
            etapa_en_ejecucion.save()
            etapa_finalizacion.save()
        #    nro_contratacion1.save()
            nro_expediente_si.save()
            nro_expediente_no.save()
        except IntegrityError as e:
            print("Error al insertar en la tabla categories.", e)
        
        
        opcion = 0
        while opcion != 2:
            print("La etapa de la obra debe ser 'FINALIZACION','EN EJECUCION', 'PROYECTO'")


            etapas = input("Ingrese la etapa de la obra: ")
            try:
                Etapas.get(Etapas.etapa == etapas)
            except DoesNotExist as e:
                print("Error al ingresar dato nulo")
                continue
   
            tipoObra = input("Ingrese su tipo de obra: ")
            areaResponsable = input("Ingrese el area responsable de la obra: ")
            barrio = input("Ingrese el barrio donde pertenece la obra: ")
            empresa = input("Ingrese la empresa que desea registrar: ")
            nro_expediente = input("Ingrese SI/NO para el expediente: ")
            try:
                Empresa.get(Empresa.nro_expediente == nro_expediente)
            except DoesNotExist as e:
                print("Error al ingresar dato nulo en el ingreso para el expediente")
                continue
            destacada = input("Que tan destacada es la Obra?: ")
            mano_obra = int(input("Cantidad de mano de Obra?: "))
            porcentaje_avance = int(input("Ingrese el porcentaje que va la obra: "))

            nueva_obra = Obra(etapas, tipoObra, areaResponsable, barrio, empresa, nro_expediente, destacada, mano_obra)
            nueva_obra.nuevo_proyecto()

            opcion += 1
        #• Este método debe retornar la nueva instancia de obra.

    #def obtener_indicadores():
        #que debe incluir las sentencias necesarias para obtener
        #información de las obras existentes en la base de datos SQLite a través de sentencias
        #ORM.

prueba1 = GestionarObra()
prueba1.limpiar_datos()
prueba1.conectar_db
prueba1.mapear_orm()
prueba1.cargar_datos()
#prueba1.nueva_obra()
