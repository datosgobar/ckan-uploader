#!/usr/bin/env python
# -*- coding: utf8 -*-

from nose.tools import *
import unittest
import responses
from ckan_uploader.ckan_uploader import CKANUploader
import json
from os import path
from ckan_uploader.models import Dataset

here = path.dirname(path.abspath(__file__))
CKAN_APIKEY = 'b110b824-dd96-46f0-b25c-bed1fc21bcfa'
CKAN_HOST = 'http://localhost:5000'

EXAMPLE_DATASET = json.load(open(path.join(here, 'testing_data/dataset.ok.json')))
EXAMPLE_BAD_DATASET = json.load(open(path.join(here, 'testing_data/dataset.fail.json')))
DISTRIBUTION_OK = json.load(open(path.join(here, 'testing_data/distribution.ok.json')))

my_mock_responses = {
    'package_list':
        {
            'case1': json.dumps(json.load(open(path.join(here, 'testing_data/package_list-case1.json'))))
        },
    'package_show':
        {
            'case1': json.dumps(json.load(open(path.join(here, 'testing_data/package_show-case1.json'))))
        },
    'package_search':
        {
            'case1': json.dumps(json.load(open(path.join(here, 'testing_data/package_search-case1.json'))))
        }
}


def class_decorating_meta(prefix, *decorators):
    '''
    modified from: http://stackoverflow.com/a/6308016
    '''
    class DecoratingMetaclass(type):
        def __new__(self, class_name, bases, namespace):
            for key, value in list(namespace.items()):
                if not key.startswith(prefix):
                    continue
                if not callable(value):
                    continue
                for decorator in decorators:
                    value = decorator(value)
                namespace[key] = value

            return type.__new__(self, class_name, bases, namespace)

    return DecoratingMetaclass


class TestCasesController(unittest.TestCase):
    """
    Tests para el controlador principal de la lib.
    """
    __metaclass__ = class_decorating_meta('test_',
                                          responses.activate)

    @classmethod
    def setUpClass(cls):
        # Inicializo una instancia correcta de CKANUploader
        cls.cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)

    @raises(ValueError)
    def test_01_miss_args(self):
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
    def test_02_wrong_types(self):
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
    def test_03_bad_apikey(self):
        """
        Crear instancia de CKANUploader con datos erroneos.

        Hipotesis:
        =========
            Si los argumentos provistos son str(), pero alguno de ellos posee len = 0
            deberia arrojarse una exception de tipo ValueError

        """
        cl = CKANUploader(CKAN_HOST, '')
        print cl.host_url  # Esta linea no sera ejecutada.

    @classmethod
    def test_04_correct_init(cls):
        """
        Crear instancia de CKANUploader con datos erroneos.

        Hipotesis:
        =========
            Si los argumentos provistos son str() y validos, la lib deberia inicializarse sin problemas.

        """

        print cls.cl.host_url  # Imprimimos las url de nuestro ckan remoto.

    @classmethod
    def test_05_render_name(cls):
        """
        Renderizar un Dataset.title a un Dataset.name.

        Hipotesis:
        =========
            Deben ser removidos los acentos, caracteres especiales y espacios replazados con guion medio.

        """
        assert_equal(cls.cl.render_name('Un nombre con eñe'), 'un-nombre-con-ene')

    def test_06_freeze_dataset(self):
        """
        Freezar el contenido de un Dataset existente dentro de CKAN.

        Hipotesis:
        =========
            Feezar un dataset, implicaria traer toda la informacion de un dataset
            remoto y convertirla en un models.Dataste(), sin perdida de datos.

        """
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_show',
            'body': my_mock_responses['package_show']['case1'],
            'content_type': 'application/json'
        })

        ddict = json.loads(my_mock_responses['package_show']['case1'])
        test_ds = Dataset(datadict=ddict['result'],
                          _distributions=ddict['result']['resources'],
                          _distribution_literal=True)
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        assert_equals(sorted(test_ds.__dict__.keys()),
                      sorted(cl.freeze_dataset('Dataset 01 Test').__dict__.keys()))
        assert_equals(sorted(test_ds.__dict__.values()),
                      sorted(cl.freeze_dataset('Dataset 01 Test').__dict__.values()))

    def test_07_diff_datasets_identity(self):
        """
        Comprobar la identidad de Dataset.

        Hipotesis:
        =========
            Dataset(A) diff Dataset(A) == None.
        """
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        ddict = json.loads(my_mock_responses['package_show']['case1'])
        test_ds = Dataset(datadict=ddict['result'],
                          _distributions=ddict['result']['resources'],
                          _distribution_literal=True)
        assert_equals(sorted(test_ds.__dict__.keys()),
                      sorted(cl.diff_datasets(dataset_a=test_ds, dataset_b=test_ds).__dict__.keys()))
        assert_equals(sorted(test_ds.__dict__.values()),
                      sorted(cl.diff_datasets(dataset_a=test_ds, dataset_b=test_ds).__dict__.values()))

    @raises(TypeError)
    def test_08_diff_datasets_bad_types(self):
        """
        Fallo en tipo de diff_datasets.

        Hipotesis:
        =========
            El metodo diff_datasets deberia arrojar un TypeError si alguno de sus argumentos,
            dataset_a o dataset_b no son de tipo models.Dataset

        """
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        ddict = json.loads(my_mock_responses['package_show']['case1'])
        test_ds = Dataset(datadict=ddict['result'],
                          _distributions=ddict['result']['resources'],
                          _distribution_literal=True)
        cl.diff_datasets(dataset_a=test_ds, dataset_b='Fuerzo raise TypeError')

    def test_09_search_for_a_dataset(self):
        """
        Buscar Dataset.

        Hipotesis:
        =========
            Cualquiera fuera el caso de test, exists simpre retorna bool.

        """
        # Preparo mock de CKAN-response.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_list',
            'body': my_mock_responses['package_list']['case1'],
            'content_type': 'application/json'
        })
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        assert_equals(cl.exists(cl.render_name('Dataset 01 Test')), True)

    def test_10_search_for_a_distribution(self):
        """
        Buscar Distributions.

        Hipotesis:
        =========
            Cualquiera fuera el caso de test, exists simpre retorna bool.

        """
        # Preparo mock de CKAN-response: package_list.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_list',
            'body': my_mock_responses['package_list']['case1'],
            'content_type': 'application/json'

        })
        # Preparo mock de CKAN-response: package_show.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_show',
            'body': my_mock_responses['package_show']['case1'],
            'content_type': 'application/json'
        })
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        assert_equals(cl.exists('mi-recurso-del-ejemplo', search_for_datasets=False, _fformat='JPEG'), True)

    def test_11_get_datasets_list_returns_always_a_list(self):
        """
        Obtener lista de datasets.

        Hipotesis:
        =========
            Cualquiera fuera el caso de test, get_datasets_list(), responde una lista.

        """
        # Preparo mock de CKAN-response: package_list.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_list',
            'body': my_mock_responses['package_list']['case1'],
            'content_type': 'application/json'

        })
        # Preparo mock de CKAN-response: package_show.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_show',
            'body': my_mock_responses['package_show']['case1'],
            'content_type': 'application/json'
        })
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        assert_equals(cl.get_datasets_list(), ['dataset-01-test'])

    def test_12_get_all_distributions_returns_always_a_dict(self):
        """
        Obtener lista de datasets.

        Hipotesis:
        =========
            Cualquiera fuera el caso de test, get_datasets_list(), responde un diccionario.

        """
        # Preparo mock de CKAN-response: package_list.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_list',
            'body': my_mock_responses['package_list']['case1'],
            'content_type': 'application/json'

        })
        # Preparo mock de CKAN-response: package_show.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_show',
            'body': my_mock_responses['package_show']['case1'],
            'content_type': 'application/json'
        })
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        assert_equals(cl.get_all_distrubutions(),
                      {u'fa05d5c0-7a2d-4ea5-9539-08e9bbe71e23':
                          {
                            u'name': u'Mi Recurso del Ejemplo',
                            u'format': u'JPEG'
                          }
                      })

    def test_13_get_resource_id(self):
        """

        :return:
        """
        # Preparo mock de CKAN-response: package_list.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_list',
            'body': my_mock_responses['package_list']['case1'],
            'content_type': 'application/json'

        })
        # Preparo mock de CKAN-response: package_show.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_show',
            'body': my_mock_responses['package_show']['case1'],
            'content_type': 'application/json'
        })
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        assert_equals(
            cl.get_resource_id(
                cl.render_name('Mi Recurso del Ejemplo')),
            'fa05d5c0-7a2d-4ea5-9539-08e9bbe71e23')

    def test_14_retrieve_dataset_metadata(self):
        """

        :return:
        """
        # Preparo mock de CKAN-response: package_list.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_list',
            'body': my_mock_responses['package_list']['case1'],
            'content_type': 'application/json'

        })
        # Preparo mock de CKAN-response: package_show.
        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:5000/api/action/package_show',
            'body': my_mock_responses['package_show']['case1'],
            'content_type': 'application/json'
        })
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        print cl.retrieve_dataset_metadata('dataset-01-test')