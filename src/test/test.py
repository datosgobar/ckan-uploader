#!/usr/bin/env python
# -*- coding: utf8 -*-
from nose.tools import *
from src.models import MyLogger, CKANElement, Errs, Dataset, Distribution
from src.helpers import list_of, get_mimetype, build_hash
from src.uploader import CKANUploader

local_test = True

if local_test:
    # Localhost
    CKAN_APIKEY = 'b110b824-dd96-46f0-b25c-bed1fc21bcfa'
    CKAN_HOST = 'http://localhost:5000'
else:
    # CKANDemo
    CKAN_HOST = 'http://demo.ckan.org'
    CKAN_APIKEY = 'c381dae0-fe59-48ee-b543-a240e0087dfa'

EXAMPLE_DATASET = {"license_title": "Una Licencia",
                   "maintainer": "Un mantenedor",
                   "private": False,
                   "maintainer_email": "mantenedor@mail.com",
                   "id": "12345678-aaaa-bbbb-cccc-1234567890123",
                   "owner_org": "12345678-aaaa-bbbb-cccc-1234567890123",
                   "author": "un autor",
                   "author_email": "autor@mail.com",
                   "state": "active",
                   "license_id": "cc-by",
                   "type": "dataset",
                   "groups": ["un-grupo-de-ejemplo", "otro-grupo-de-ejemplos"],
                   "creator_user_id": "12345678-aaaa-bbbb-cccc-1234567890123",
                   "name": "",
                   "isopen": True,
                   "url": "",
                   "notes": "Una descripcion para este dataset",
                   "title": "Un titulo para el dataset.",
                   "license_url": "http://www.opendefinition.org/licenses/cc-by"}

EXAMPLE_BAD_DATASET = {"license_title": "Una Licencia",
                       "maintainer": "Un mantenedor",
                       "private": False,
                       "maintainer_email": "mantenedor@mail.com",
                       "id": "12345678-aaaa-bbbb-cccc-1234567890123",
                       "owner_org": "12345678-aaaa-bbbb-cccc-1234567890123",
                       "author": "un autor",
                       "author_email": "autor@mail.com",
                       "state": "active",
                       "type": "dataset",
                       "groups": ["un-grupo-de-ejemplo", "otro-grupo-de-ejemplos"],
                       "creator_user_id": "12345678-aaaa-bbbb-cccc-1234567890123",
                       "name": "",
                       "isopen": True,
                       "url": "",
                       "notes": "Una descripcion para este dataset",
                       "title": "Un titulo para el dataset.",
                       "license_url": "http://www.opendefinition.org/licenses/cc-by"}

DISTRIBUTION_OK = {"state": 'active',
                   "license_id": 'un id de licencia',
                   "description": 'Description para mi distribution',
                   "url": 'http://host.com',
                   "name": 'Nombre de mi distrubution'}


@raises(ValueError)
def test_01_miss_args():
    """
    Crear instancia de CKANUploader

    Hipotesis:
    =========
        Si no existen argumento la creacion del nueva instancia deberia lanzar,
        una exception de tipo ValueError.


    """
    cl = CKANUploader()
    print cl.host_url  # Esta linea no sera ejecutada


@raises(ValueError)
def test_02_wrong_types():
    """
    Crear instancia de CKANUploader con datos erroneos.

    Hipotesis:
    =========
        Si los argumentos provistos no son str(),
        deberia lanzar una exception de tipo ValueError

    """
    cl = CKANUploader({}, [])
    print cl.host_url  # Esta linea no sera ejecutada


@raises(ValueError)
def test_03_bad_apikey():
    """
    Crear instancia de CKANUploader con datos erroneos.

    Hipotesis:
    =========
        Si los argumentos provistos son str(), pero alguno de ellos posee len = 0
        deberia arrojarse una exception de tipo ValueError

    """
    cl = CKANUploader(CKAN_HOST, '')


def test_04_correct_init():
    """
    Crear instancia de CKANUploader con datos erroneos.

    Hipotesis:
    =========
        Si los argumentos provistos son str() y validos, la lib deberia inicializarse sin problemas.

    """
    cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
    print cl.host_url  # Imprimimos las url de nuestro ckan remoto.


def test_05_search_for_a_dataset():
    """
    Buscar Dataset.

    Hipotesis:
    =========
        Cualquiera fuera el caso de test, exists simpre retorna bool.

    """
    cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
    assert_equals(isinstance(cl.exists('my_dataset'), bool), True)


def test_06_search_for_a_distribution():
    """
    Buscar Distributions.

    Hipotesis:
    =========
        Cualquiera fuera el caso de test, exists simpre retorna bool.

    """
    cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
    assert_equals(isinstance(cl.exists('my_distribution', search_for_datasets=False), bool), True)


def test_07_get_datasets_list_returns_always_a_list():
    """
    Obtener lista de datasets.

    Hipotesis:
    =========
        Cualquiera fuera el caso de test, get_datasets_list(), responde una lista.

    """
    cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
    assert_equals(isinstance(cl.get_datasets_list(), list), True)


def test_08_get_all_distributions_returns_always_a_dict():
    """
    Obtener lista de datasets.

    Hipotesis:
    =========
        Cualquiera fuera el caso de test, get_datasets_list(), responde un diccionario.

    """
    cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
    assert_equals(isinstance(cl.get_all_distrubutions(), dict), True)


# ERRs Test

def test_01_models_mylogger_class():
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


def test_02_models_mylogger_class():
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


def test_03_models_mylogger_class():
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
def test_04_models_mylogger_class():
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
def test_05_models_mylogger_class():
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
def test_06_models_mylogger_class():
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
def test_07_models_mylogger_class():
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
def test_08_models_mylogger_class():
    """
    Test MyLogs class.

    Hipotesis:
    =========
       Si intento seleccionar un log_level inexistente, salgo con una Exception ValueError.
    """
    mylogger_instance = MyLogger(log_level='NO-EXISTE', logger_name='Test')
    mylogger_instance.error('Este mensaje nunca va a ser loggeado por un fallo '
                            'en la creacion de la instancia')


def test_01_models_CKANElement_class():
    """
    Test CKANElement Class

    Hipotesis:
    =========
        La suma de las claves requeridas mas las claves forzadas
        es igual al cls.__dict__.

    """
    example_requiered_keys = {
        'requiered_key1': 'value_01',
        'requiered_key2': 'value_02',
        'requiered_key3': 'value_03',
        'requiered_key4': 'value_04',
        'requiered_key5': 'value_05',
    }
    example_forced_keys = {
        'forced_key1': 'value01',
        'forced_key2': 'value02',
    }

    ce = CKANElement(_forced_keys=example_forced_keys,
                     _required_keys=example_requiered_keys.keys(),
                     context='dataset',
                     datadict=example_requiered_keys)
    result = example_requiered_keys
    result.update(example_forced_keys)
    class_as_dict = ce.__dict__
    del class_as_dict['required_keys']
    del class_as_dict['context']
    assert_equals(class_as_dict, result)


@raises(TypeError)
def test_02_models_CKANElement_class():
    """
    Test CKANElement Class 02.
    Hipotesis:
    =========
        Si intento crear una instancia de la clase CKANElement sin argumentos,
        salgo con una Exception TypeError.

    """
    ce = CKANElement()
    print ce.context


@raises(KeyError)
def test_03_models_CKANElement_class():
    """
    Test CKANElement Class 03.

    Hipotesis:
    =========
        Si falta una clave requerida salgo con una Exception KeyError.

    """
    example_requiered_keys = ['requiered_key1',
                              'requiered_key2',
                              'requiered_key3',
                              'requiered_key4',
                              'requiered_key5']
    example_forced_keys = {
        'forced_key1': 'value01',
        'forced_key2': 'value02',
    }

    # Elimino dos claves requeridas
    mydatadict = {'requiered_key1': 'value_01',
                  'requiered_key2': 'value_02',
                  'requiered_key3': 'value_03'}

    ce = CKANElement(_forced_keys=example_forced_keys,
                     _required_keys=example_requiered_keys,
                     context='dataset',
                     datadict=mydatadict)
    print ce.context


@raises(TypeError)
def test_04_models_CKANElement_class():
    """
    Test CKANElement Class 04.

    Hipotesis:
    =========
        Si el argumento datadict de otra clase que no sea dict, salgo con una exception TypeError.

    """
    example_requiered_keys = ['requiered_key1',
                              'requiered_key2',
                              'requiered_key3',
                              'requiered_key4',
                              'requiered_key5']
    example_forced_keys = {
        'forced_key1': 'value01',
        'forced_key2': 'value02',
    }

    # Elimino dos claves requeridas
    mydatadict = 'genero un exception TypeError'

    ce = CKANElement(_forced_keys=example_forced_keys,
                     _required_keys=example_requiered_keys,
                     context='dataset',
                     datadict=mydatadict)
    print ce.context


@raises(TypeError)
def test_05_models_CKANElement_class():
    """
    Test CKANElement Class 05.

    Hipotesis:
    =========
        Si el argumento requiered_keys de otra clase que no sea list, salgo con una exception TypeError.

    """
    example_requiered_keys = 'Esta no es una clase aceptable.'
    example_forced_keys = {
        'forced_key1': 'value01',
        'forced_key2': 'value02',
    }

    mydatadict = {'requiered_key1': 'value_01',
                  'requiered_key2': 'value_02'}

    ce = CKANElement(_forced_keys=example_forced_keys,
                     _required_keys=example_requiered_keys,
                     context='dataset',
                     datadict=mydatadict)
    print ce.context


def test_01_models_Distribution_class():
    """
    Test Distribution Class 01

    Hipotesis:
    =========
        Crear una instancia de Distribution.
    """
    my_distribution = Distribution(datadict=DISTRIBUTION_OK)
    assert_equals(my_distribution.context, 'distribution')


def test_02_models_Distribution_class():
    """
    Test Distribution Class 02

    Hipotesis:
    =========
        Crear una instancia de Distribution con un archivo en lugar de link.
    """
    import os
    file_content = 'columna1,columna2,columna3\n' \
                   '1,2,3\n' \
                   'a,b,c\n'
    with open('my_csv_example_file.csv', 'w') as tmp:
        tmp.write(file_content)
        tmp.close()
    my_distribution = Distribution(datadict=DISTRIBUTION_OK, _file='my_csv_example_file.csv')
    assert_equals(os.path.basename(my_distribution.file), 'my_csv_example_file.csv')
    os.remove('my_csv_example_file.csv')


@raises(AttributeError)
def test_03_models_Distribution_class():
    """
    Test Distribution Class 03

    Hipotesis:
    =========
        Si el archivo provisto para la nueva distribucion no existe, el mismo se omite.
    """
    my_distribution = Distribution(datadict=DISTRIBUTION_OK, _file='no-existe-este-archivo')
    # Como el archivo provisto no es valido, el atributo
    # "file" no deberia existir dentro de la clase.
    print my_distribution.file


def test_01_models_Dataset_class():
    """
    Test Dataset Class 01

    Hipotesis:
    =========
        Instanciar la clase Dataset.

    """

    my_new_dataset = EXAMPLE_DATASET

    my_dataset = Dataset(datadict=my_new_dataset)
    assert_equals(my_dataset.author_email, 'autor@mail.com')


@raises(KeyError)
def test_02_models_Dataset_class():
    """
    Test Dataset Class 02

    Hipotesis:
    =========
        Si falta alguna de las claves requeridas para crear el dataset, salgo
        con una Exception KeyError.

    """

    my_new_bad_dataset = EXAMPLE_BAD_DATASET
    my_dataset = Dataset(datadict=my_new_bad_dataset)
    # Esta linea no se ejecutara.
    assert_equals(my_dataset.author_email, 'autor@mail.com')


@raises(TypeError)
def test_03_models_Dataset_class():
    """
    Test Dataset Class 03

    Hipotesis:
    =========
       El argumento datadict, solo puede ser de tipo dict. Si esto ocurre,
       salgo con una exeption TypeError.

    """

    my_new_dataset = None
    my_dataset = Dataset(datadict=my_new_dataset)
    # Esta linea no se ejecutara.
    assert_equals(my_dataset.author_email, 'autor@mail.com')


def test_04_models_Dataset_class():
    """
    Test Dataset Class 04

    Hipotesis:
    =========
       La clase Dataset posee un argumento opcional llamado _distributions.
       Este argumento acepta objs de clase list() y Distribution, si el flag _distribution_literal== False.
       Si no es de ninguna de esas clases, se omiten las distribuciones.
    """

    my_new_dataset = EXAMPLE_DATASET
    my_dataset = Dataset(datadict=my_new_dataset, _distributions=1234)
    assert_equals(my_dataset.resources, [])


def test_05_models_Dataset_class():
    """
    Test Dataset Class 05

    Hipotesis:
    =========
       La clase Dataset posee un argumento opcional llamado _distributions.
       Este argumento acepta objs de clase list() y Distribution, si el flag _distribution_literal== False.
       por el contrario, el flag _distribution_literal si el mismo se encuentra en True, _distributions
       puede recibir listas de diccionarios como aceptables.
       Si no es de ninguna de esas clases, salgo con una exception TypeError
    """

    my_new_dataset = EXAMPLE_DATASET
    my_dataset = Dataset(datadict=my_new_dataset, _distributions=[{}, {}, {}], _distribution_literal=True)
    assert_equals(my_dataset.resources, [{}, {}, {}])


def test_06_models_Dataset_class():
    """
    Test Dataset Class 04

    Hipotesis:
    =========
       Crear una Dataset con una distribucion.
    """
    my_distribution = Distribution(datadict=DISTRIBUTION_OK)
    my_new_dataset = EXAMPLE_DATASET
    my_dataset = Dataset(datadict=my_new_dataset,
                         _distributions=my_distribution)
    assert_equals(my_dataset.resources, [my_distribution])


def test_07_models_Dataset_class():
    """
    Test Dataset Class 04

    Hipotesis:
    =========
       Crear una Dataset con una lista de distribuciones.
    """
    my_distribution = Distribution(datadict=DISTRIBUTION_OK)
    my_other_distribution = Distribution(datadict=DISTRIBUTION_OK)
    my_new_dataset = EXAMPLE_DATASET
    my_dataset = Dataset(datadict=my_new_dataset,
                         _distributions=[my_distribution, my_other_distribution])
    assert_equals(my_dataset.resources, [my_distribution, my_other_distribution])


def test_01_models_errs_class():
    """
    Test Errs Class 01

    Hipotesis:
    =========
        Crear una instancia de Errs.
    """
    my_err = Errs(_context='testing', _description='un error de test', _type='error')
    expected_result = '{date}: ERROR: testing: un error de test.' \
                      ''.format(date=my_err.timestamp.format('YYYY-MM-DDTHH:mm:ss'))
    assert_equals(my_err.__str__(), expected_result)


@raises(TypeError)
def test_02_models_errs_class():
    """
    Test Errs Class 02

    Hipotesis:
    =========
        Todos los argumentos son requeridos, si alguno falta, salgo con una Exception TypeError.
    """
    my_err = Errs(_context=None, _description='un error de test', _type='error')
    # Estas lineas no se ejecutaran.
    expected_result = '{date}: ERROR: testing: un error de test.' \
                      ''.format(date=my_err.timestamp.format('YYYY-MM-DDTHH:mm:ss'))

    assert_equals(my_err.__str__(), expected_result)


@raises(ValueError)
def test_03_models_errs_class():
    """
    Test Errs Class 03

    Hipotesis:
    =========
        Los argumentos no pueden ser len(arg)==0.
    """
    my_err = Errs(_context='', _description='', _type='')
    # Estas lineas no se ejecutaran.
    expected_result = '{date}: ERROR: testing: un error de test.' \
                      ''.format(date=my_err.timestamp.format('YYYY-MM-DDTHH:mm:ss'))

    assert_equals(my_err.__str__(), expected_result)


def test_01_helpers_list_of():
    """
    Helpers Test 01 metodo list_of()

    Hipotesis:
    =========
        Es una lista donde todos sus elementos de clase srt.
    """
    my_list = ['srt1', 'str2', 'str2']
    assert_equals(list_of(my_list, str), True)


def test_02_helpers_list_of():
    """
    Helpers Test 02 metodo list_of()

    Hipotesis:
    =========
        No es una lista donde todos sus elementos son de clase srt.
    """
    my_list = ['srt1', 1234, 'str2']
    assert_equals(list_of(my_list, str), False)


@raises(TypeError)
def test_03_helpers_list_of():
    """
    Helpers Test 03 metodo list_of()

    Hipotesis:
    =========
        El argumento _list solo puede ser de clase list(), si esto no sucede, salgo
        con un exception TypeError.
    """
    my_list = 'Esto no es una lista.'
    assert_equals(list_of(my_list, str), False)


def test_01_helpers_get_mimetype():
    """
    Helpers Test 01 metodo get_mimetype()

    Hipotesis:
    =========
        Se informa de manera correcta el mime type de un archivo.
    """
    import os
    my_test_file = os.path.abspath(__file__)
    assert_equals('x-python' in get_mimetype(my_test_file), True)


def test_02_helpers_get_mimetype():
    """
    Helpers Test 02 metodo get_mimetype()

    Hipotesis:
    =========
        El metodo responde None, si el archivo no existe.
    """
    my_test_file = 'no-existe-este-archivo'
    assert_equals(get_mimetype(my_test_file), None)


def test_01_helpers_build_hash():
    """
    Helpers Test 01 metodo build_hash()

    Hipotesis:
    =========
        Realiza correctamente el calculo de hash.
    """
    import os
    with open('file.tmp', 'w') as tmp_file:
        tmp_file.write('hola mundo!')
        tmp_file.close()

    assert_equals(build_hash('file.tmp'), 'b351ed7759888fe8c3bafb8ef7952b80')
    os.remove('file.tmp')


def test_02_helpers_build_hash():
    """
    Helpers Test 02 metodo build_hash()

    Hipotesis:
    =========
        El metodo responde None si el archivo no existe.
    """
    assert_equals(build_hash('este-archivo-no-existe'), None)
