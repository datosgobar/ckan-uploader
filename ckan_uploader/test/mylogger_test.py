from ckan_uploader.models import MyLogger
from nose.tools import *
import unittest


class TestCasesLogger(unittest.TestCase):
    """
    Tests para la clase 'MyLogger' de la lib.
    """

    def test_01_models_mylogger_class(self):
        """
        Crear logs.

        Hipotesis:
        =========
           El metodo .get_logs() sin argumentos, responde la lista total de entradas de logs.

        """
        mylogger_instance = MyLogger(log_level='INFO', logger_name='Testing')
        for i in range(10):
            mylogger_instance.error('Esto es un mensaje de error {}'.format(i))
        for i in range(5):
            mylogger_instance.info('Esto es un mensaje de info {}'.format(i))
        for i in range(10):
            mylogger_instance.warning('Esto es un mensaje de advertencia {}'.format(i))
        for i in range(5):
            mylogger_instance.critical('Esto es un mensaje de fallo critico {}'.format(i))
        assert_equals(len(mylogger_instance.get_logs()), 30)

    def test_02_models_mylogger_class(self):
        """
        Test MyLogs class.

        Hipotesis:
        =========
           El metodo .get_logs() con el argumento _filter_by_type, responde la lista
           de entradas de logs para el tipo especifico.

        """
        mylogger_instance = MyLogger(log_level='INFO', logger_name='Testing')
        for i in range(10):
            mylogger_instance.error('Esto es un mensaje de error {}'.format(i))
        for i in range(5):
            mylogger_instance.info('Esto es un mensaje de info {}'.format(i))
        for i in range(10):
            mylogger_instance.warning('Esto es un mensaje de advertencia {}'.format(i))
        for i in range(5):
            mylogger_instance.critical('Esto es un mensaje de fallo critico {}'.format(i))
        assert_equals(len(mylogger_instance.get_logs(_filter_by_type='error')), 10)
        assert_equals(len(mylogger_instance.get_logs(_filter_by_type='info')), 5)
        assert_equals(len(mylogger_instance.get_logs(_filter_by_type='warning')), 10)
        assert_equals(len(mylogger_instance.get_logs(_filter_by_type='critical')), 5)

    def test_03_models_mylogger_class(self):
        """
        Test MyLogs class.

        Hipotesis:
        =========
           El metodo .get_logs() para el argumento _filter_by_type acepta solo:
           ['INFO','DEBUG','ERROR','CRITICAL','WARNING', 'NOTSET'], por tanto,
           si se consulta por un tipo fuera de esta lista, retorna una lista
           vacia.

        """
        mylogger_instance = MyLogger(log_level='INFO', logger_name='Testing')
        for i in range(10):
            mylogger_instance.error('Esto es un mensaje de error {}'.format(i))
        assert_equals(len(mylogger_instance.get_logs(_filter_by_type='no-existe-este-tipo')), 0)

    @raises(TypeError)
    def test_04_models_mylogger_class(self):
        """
        Test MyLogs class.

        Hipotesis:
        =========
           Para instanciar la clase se requieren dos argumentos,
           log_level y logger_name, ambos deben ser de tipo str o unicode
           y no admiten len(arg)==0.
           Si esto ocurre para cualquiera de los argumentos, se sale con un Exception
           TypeError.
        """
        mylogger_instance = MyLogger(log_level=list('INFO'), logger_name='Testing')
        mylogger_instance.error('Este mensaje nunca va a ser loggeado por un fallo '
                                'en la creacion de la instancia')

    @raises(TypeError)
    def test_05_models_mylogger_class(self):
        """
        Test MyLogs class.

        Hipotesis:
        =========
           Para instanciar la clase se requieren dos argumentos,
           log_level y logger_name, ambos deben ser de tipo str o unicode
           y no admiten len(arg)==0.
           Si esto ocurre para cualquiera de los argumentos, se sale con un Exception
           TypeError.
        """
        mylogger_instance = MyLogger(log_level='INFO', logger_name=list('Testing'))
        mylogger_instance.error('Este mensaje nunca va a ser loggeado por un fallo '
                                'en la creacion de la instancia')

    @raises(ValueError)
    def test_06_models_mylogger_class(self):
        """
        Test MyLogs class.

        Hipotesis:
        =========
           Para instanciar la clase se requieren dos argumentos,
           log_level y logger_name, ambos deben ser de tipo str o unicode
           y no admiten len(arg)==0.
           Si esto ocurre para cualquiera de los argumentos, se sale con un Exception
           TypeError.
        """
        mylogger_instance = MyLogger(log_level='', logger_name='Testing')
        mylogger_instance.error('Este mensaje nunca va a ser loggeado por un fallo '
                                'en la creacion de la instancia')

    @raises(ValueError)
    def test_07_models_mylogger_class(self):
        """
        Test MyLogs class.

        Hipotesis:
        =========
           Para instanciar la clase se requieren dos argumentos,
           log_level y logger_name, ambos deben ser de tipo str o unicode
           y no admiten len(arg)==0.
           Si pasamos argumentos vacios para cualquiera de argumentos, se sale con un Exception
           ValueError.
        """
        mylogger_instance = MyLogger(log_level='INFO', logger_name='')
        mylogger_instance.error('Este mensaje nunca va a ser loggeado por un fallo '
                                'en la creacion de la instancia')

    @raises(ValueError)
    def test_08_models_mylogger_class(self):
        """
        Test MyLogs class.

        Hipotesis:
        =========
           Si intento seleccionar un log_level inexistente, salgo con una Exception ValueError.
        """
        mylogger_instance = MyLogger(log_level='NO-EXISTE', logger_name='Test')
        mylogger_instance.error('Este mensaje nunca va a ser loggeado por un fallo '
                                'en la creacion de la instancia')
