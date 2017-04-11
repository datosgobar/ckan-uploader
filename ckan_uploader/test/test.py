from ckan_uploader.uploader import CKANUploader
from nose.tools import *


@raises(TypeError)
def test_01_miss_args():
    """
    Crear instancia de CKANUploader

    Hipotesis:
    =========
        Si no existen argumento la creacion del nueva instancia deberia lanzar,
        una exception de tipo TypeError.


    """
    cl = CKANUploader()


@raises(TypeError)
def test_02_wrong_types():
    """
    Crear instancia de CKANUploader con datos erroneos.

    Hipotesis:
    =========
        Si los argumentos provistos no son str(),
        deberia lanzar una exception de tipo TypeError

    """
    cl = CKANUploader({}, [])


@raises(ValueError)
def test_03_bad_apikey():
    """
    Crear instancia de CKANUploader con datos erroneos.

    Hipotesis:
    =========
        Si los argumentos provistos son str(), pero alguno de ellos posee len = 0
        deberia arrojarse una exception de tipo ValueError

    """
    cl = CKANUploader('http://demo.ckan.org', '')


def test_04_correct_init():
    """
    Crear instancia de CKANUploader con datos erroneos.

    Hipotesis:
    =========
        Si los argumentos provistos son str() y validos, la lib deberia inicializarse sin problemas.

    """
    cl = CKANUploader('http://demo.ckan.org', 'c381dae0-fe59-48ee-b543-a240e0087dfa')


def test_05_search_for_a_dataset():
    """
    Buscar Dataset.

    Hipotesis:
    =========
        Cualquiera fuera el caso de test, exists simpre retorna bool.

    """
    cl = CKANUploader('http://demo.ckan.org', 'c381dae0-fe59-48ee-b543-a240e0087dfa')
    assert_equals(isinstance(cl.exists('my_dataset'), bool), True)


def test_06_search_for_a_distribution():
    """
    Buscar Distributions.

    Hipotesis:
    =========
        Cualquiera fuera el caso de test, exists simpre retorna bool.

    """
    cl = CKANUploader('http://demo.ckan.org', 'c381dae0-fe59-48ee-b543-a240e0087dfa')
    assert_equals(isinstance(cl.exists('my_distribution', search_for_datasets=False), bool), True)


def test_07_get_datasets_list_returns_always_a_list():
    """
    Obtener lista de datasets.

    Hipotesis:
    =========
        Cualquiera fuera el caso de test, get_datasets_list(), responde una lista.

    """
    cl = CKANUploader('http://demo.ckan.org', 'c381dae0-fe59-48ee-b543-a240e0087dfa')
    assert_equals(isinstance(cl.get_datasets_list(), list), True)


def test_08_get_all_distributions_returns_always_a_dict():
    """
    Obtener lista de datasets.

    Hipotesis:
    =========
        Cualquiera fuera el caso de test, get_datasets_list(), responde un diccionario.

    """
    cl = CKANUploader('http://demo.ckan.org', 'c381dae0-fe59-48ee-b543-a240e0087dfa')
    assert_equals(isinstance(cl.get_all_distrubutions(), dict), True)
