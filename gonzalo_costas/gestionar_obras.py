
import pandas as pd
from modelo_orm import *
from abc import ABC


class GestionarObra(ABC):
    df = None
    df_limpio = None

    @classmethod
    def extraer_datos(cls):
        #que debe incluir las sentencias necesarias para manipular el dataset a
        #través de un objeto Dataframe del módulo “pandas”.
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
        #que debe incluir las sentencias necesarias para realizar la “limpieza” de
        #los datos nulos y no accesibles del Dataframe.
        #(Pandas elimina filas sólo con valores NaN para una columna en particular 
        #usando el método DataFrame.dropna())
        cls.extraer_datos()
        cls.df.dropna(subset=['entorno', 'financiamiento'],axis = 0, inplace = True)
        data_unique_entorno= list(cls.df['entorno'].unique())
    
        print(cls.df.head())
        print(cls.df.count())
        print(cls.df.columns)
        
        cls.df_limpio = data_unique_entorno

    @classmethod
    def conectar_db(cls):
        #que debe incluir las sentencias necesarias para realizar la conexión a la
        #base de datos “obras_urbanas.db”.
        try:
            print('base de datos conectada')
            cls.db = db.connect()
        except OperationalError as e:
            print("Error al conectar con la BD.", e)
            exit()
        

    #def mapear_orm():
        #que debe incluir las sentencias necesarias para realizar la creación de la
        #estructura de la base de datos (tablas y relaciones) utilizando el método de instancia
        #“create_tables(list)” del módulo peewee.
    
    @classmethod
    def cargar_datos(cls):
        #que debe incluir las sentencias necesarias para persistir los datos de las
        #obras (ya transformados y “limpios”) que contiene el objeto Dataframe en la base de datos
        #relacional SQLite. Para ello se debe utilizar el método de clase Model create() en cada una
        #de las clase del modelo ORM definido.


        for elem in cls.df_limpio:
            print("Elemento:", elem)
            try:
                TipoEntorno.create(nombre=elem)
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla tipo entorno", e)
        print("Se han persistido los tipos de transporte en la BD.")

        print("Recorremos las filas del archivo csv e insertamos los valores en la tabla 'viajes' de la BD")
        cls.extraer_datos()
        for elem in cls.df.values:
            tipo_entorn= TipoEntorno.get(TipoEntorno.nombre == elem[0])
            try:
                IndentificacionObra.create(tipo_entorno=tipo_entorn,id_obra=elem[1], nombre=elem[2], etapa=elem[3], area_responsable = elem[4], descripcion=elem[5], monto_contrato=elem[6])
            except IntegrityError as e:
                print("Error al insertar un nuevo registro en la tabla viajes.", e)

    #def nueva_obra():
        #que debe incluir las sentencias necesarias para crear nuevas instancias de
        #Obra. Se deben considerar los siguientes requisitos:
        #• Todos los valores requeridos para la creación de estas nuevas instancias deben ser
        #ingresados por teclado.
        #• Para los valores correspondientes a registros de tablas relacionadas (foreign key), el
        #valor ingresado debe buscarse en la tabla correspondiente mediante sentencia de
        #búsqueda ORM, para obtener la instancia relacionada, si el valor ingresado no existe
        #en la tabla, se le debe informar al usuario y solicitarle un nuevo ingreso por teclado.
        #• Para persistir en la BD los datos de la nueva instancia de Obra debe usarse el método
        #save() de Model del módulo peewee.
        #• Este método debe retornar la nueva instancia de obra.

    #def obtener_indicadores():
        #que debe incluir las sentencias necesarias para obtener
        #información de las obras existentes en la base de datos SQLite a través de sentencias
        #ORM.

prueba1 = GestionarObra()
prueba1.limpiar_datos()
print(prueba1)
prueba1.conectar_db
print(prueba1)
prueba1.cargar_datos()
print(prueba1)