class BaseCsv(ABC):    

    @abstractmethod
    def csv_response(self):
        """Crea las cabeceras del objeto response y lo retorna."""

    @abstractmethod
    def init_csv(self): 
        """Inicializa el archivo csv, insertando las cabeceras y las columnas."""
    
    @abstractmethod
    def write_csv(self):
        """Escribe los registros en el archivo csv inicializado."""
            

class ExecSp:
    query: str
    params: tuple | None
    with_params: bool = False

    def __init__(self, query: str, params: tuple = None) -> None:
        self.query = query
        self.params = params

        if params:
            self.with_params = True

    def execute_sp(self):
        if self.with_params:
            self.data = execute_query_with_params(self.query, self.params)
        else:
            self.data = execute_query_without_params(self.query, self.params)
        return self.data
    


from abc import ABC, abstractmethod


class BaseCsv(ABC):    

    @abstractmethod
    def csv_response(self):
        """Crea las cabeceras del objeto response y lo retorna."""

    @abstractmethod
    def get_response(self):
        """"""
        return self.response

    @abstractmethod
    def init_csv(self): 
        """Inicializa el archivo csv, insertando las cabeceras y las columnas."""
    
    @abstractmethod
    def write_csv(self):
        """Escribe los registros en el archivo csv inicializado."""
            

class ExecSp:
    query: str
    params: tuple | None
    with_params: bool = False

    def __init__(self, query: str, params: tuple = None) -> None:
        self.query = query
        self.params = params

        if params:
            self.with_params = True

    def execute_sp(self):
        if self.with_params:
            self.data = execute_query_with_params(self.query, self.params)
        else:
            self.data = execute_query_without_params(self.query, self.params)
        return self.data


class BaseCsv(ABC):    

    @abstractmethod
    def csv_response(self):
        """Crea las cabeceras del objeto response y lo retorna."""

    @abstractmethod
    def init_csv(self): 
        """Inicializa el archivo csv, insertando las cabeceras y las columnas."""
    
    @abstractmethod
    def write_csv(self):
        """Escribe los registros en el archivo csv inicializado."""
            

class ExecSp:
    query: str
    params: tuple | None
    with_params: bool = False

    def __init__(self, query: str, params: tuple = None) -> None:
        self.query = query
        self.params = params

        if params:
            self.with_params = True

    def execute_sp(self):
        if self.with_params:
            self.data = execute_query_with_params(self.query, self.params)
        else:
            self.data = execute_query_without_params(self.query, self.params)
        return self.data
    



***
class CsvBuilder:
    time_stamp = datetime.now()
    headers = (
                ['Fecha de corte: ', time_stamp.strftime("%Y-%m-%d"), ' ' + time_stamp.strftime("%H:%M:%S")],
                ['Fecha de la base de datos ', 'del año de:', time_stamp.strftime("%Y-%m-%d"), ' del mes: ', time_stamp.strftime("%H:%M:%S")]
            )
    columns = [
            'JURISDICCIÓN',
            'CESSA',
            'UNIDAD',
            'NB',
            'NOMBRE',
            'APELLIDO PATERNO',
            'APELLIDO MATERNO',
            'CURP',
            'EDAD',
            'CELULAR',
            'CELULAR CONTACTO',
            'DERECHOHABIENCIA',
            'NACIONALIDAD',
            'ENTIDAD DE NACIMIENTO',
            'ESTADO CIVIL',
            'ESCOLARIDAD',
            'OCUPACIÓN',
            'CONSIDERA INDÍGENA',
            'LENGUA INDÍGENA',
            'RELIGIÓN',
            'EDAD PAREJA',
            'ESTATURA',
            'PESO',
            'RIESGO',
            'GESTAS',
            'PARTOS',
            'ABORTOS',
            'CESAREAS',
            'ÓBITOS',
            'EDAD 1ER EMBARAZO',
            'ENFERMEDADES HIPERTENSIVAS',
            'HEMORRAGIAS',
            'NÚMERO DE CONSULTAS',
            'FECHA DE ULTIMA REGLA',
            'FECHA PROBABLE DE PARTO',
            'INICIO CONTROL PRENATAL',
            'SEMANAS DE GESTACIÓN',
            'VACUNA TETÁNICA',
            'VACUNA INFLUENZA',
            'VACUNA COVID',
            'LUGAR PARTO',
            'EDAD PRIMER USO',
            'ANTICONCEPTIVO',
            'ÚLTIMO PAPANICOLAOU',
            'ENF TRASMISIÓN SEXUAL',
            'NÚMERO PAREJAS SEXUALES',
            'PRUEBA VIH',
            'FECHA PRUEBA VIH',
            'RESULTADO PRUEBA VIH',
            'PRUEBA SEGUNDA VIH',
            'FECHA PRUEBA SEGUNDA VIH',
            'RESULTADO PRUEBA SEGUNDA VIH',
            'TERCERA PRUEBA VIH',
            'FECHA PRUEBA TERCERA  VIH',
            'RESULTADO PRUEBA TERCERA  VIH',
            'PRUEBA SÍFILIS',
            'FECHA PRUEBA SÍFILIS',
            'RESULTADO PRUEBA SÍFILIS',
            'SEGUNDA PRUEBA SÍFILIS',
            'FECHA  SEGUNDA PRUEBA SÍFILIS',
            'RESULTADO SEGUNDA PRUEBA SÍFILIS',
            'IVU',
            'TIPO SANGRE',
            'DIABETES',
            'ASMA',
            'HIPERTENSIÓN',
            'ENFERMEDAD CARDIOVASCULAR',
            'CÁNCER',
            'EPOC',
            'TUBERCULOSIS',
            'TIROIDES',
            'INSUFICIENCIA RENAL',
            'LUPUS',
            'VIH',
            'OTROS',
            'TIPO RESOLUCIÓN',
            'FECHA RESOLUCIÓN',
            'EDAD GESTACIONAL',
            'METODO ELEGIDO POSTEVENTO',
            'PLANIFICACIÓN POSTEVENTO',
            'FECHA DEFUNCIÓN',
            'FOLIO DEFUNCIÓN',
            'LOCALIDAD',
            'CALLE',
            '# INTERIOR',
            '#EXTERIOR',
            'CP',
            'ESTADO DE RESIDENCIA',
            'OBSERVACIONES'
        ]

    def __init__(self, table, busqueda_anio, busqueda, perfil=None) -> None:
        self.table = table
        self.perfil = perfil
        if self.table == 'SinMetodoElegidoPostEvento':
            params = (perfil.tipo, perfil.fk_unidad.id, busqueda_anio, busqueda )
            str_query = 'EXEC F_T_SIN_METODO_ELEGIDO_POSTEVENTO %s, %s, %s, %s'
            self.data = execute_query_with_params(str_query, params)
            self.file = TableToCsv(self.data, self.headers, self.columns)            
            self.file.write_csv()
        elif self.table == 'PUERPERIO_PATOLOGICO':
            params = (busqueda_anio, busqueda )
            str_query = 'EXEC F_T_PUERPERIO_PATOLOGICO %s, %s'
            self.data = execute_query_with_params(str_query, params)
            self.file = TableToCsv(self.data, self.headers, self.columns)
            self.file.write_csv()