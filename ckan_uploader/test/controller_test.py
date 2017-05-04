#!/usr/bin/env python
# -*- coding: utf8 -*-

from nose.tools import *
import responses
import unittest
from ckan_uploader.ckan_uploader import CKANUploader

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

my_mock_responses = {
    'package_list':
        {
            'case1':
                '''
                {
                  "help": "http://localhost:5000/api/3/action/help_show?name=package_list",
                  "success": true,
                  "result": ["dataset-01-test"]
                }
                '''
        },
    'package_show':
        {
            'case1':
                '''
                {
                    "help": "http://demo.ckan.org/api/3/action/help_show?name=package_show",
                    "success": true,
                    "result": {
                        "license_title": null,
                        "maintainer": null,
                        "relationships_as_object": [],
                        "private": false,
                        "maintainer_email": null,
                        "num_tags": 2,
                        "id": "0678bcc6-65b2-4a5c-b251-e1bb9b03aaf3",
                        "metadata_created": "2017-05-04T19:11:04.407375",
                        "metadata_modified": "2017-05-04T19:29:29.865995",
                        "author": null,
                        "author_email": null,
                        "state": "active",
                        "version": null,
                        "creator_user_id": "e4653e45-1ef4-4198-b515-ccb6d527f180",
                        "type": "dataset",
                        "resources": [{
                            "cache_last_updated": null,
                            "package_id": "0678bcc6-65b2-4a5c-b251-e1bb9b03aaf3",
                            "webstore_last_updated": null,
                            "datastore_active": false,
                            "id": "fa05d5c0-7a2d-4ea5-9539-08e9bbe71e23",
                            "size": null,
                            "state": "active",
                            "hash": "",
                            "description": "",
                            "format": "JPEG",
                            "last_modified": null,
                            "url_type": null,
                            "mimetype": null,
                            "cache_url": null,
                            "name": "Mi Recurso del Ejemplo",
                            "created": "2017-05-04T19:25:10.673417",
                            "url": "",
                            "webstore_url": null,
                            "mimetype_inner": null,
                            "position": 1,
                            "revision_id": "6100555d-78aa-4c7a-af8e-b3b108a87704",
                            "resource_type": null
                        }],
                        "num_resources": 2,
                        "tags": [{
                            "vocabulary_id": null,
                            "state": "active",
                            "display_name": "tag1",
                            "id": "de5c1397-92bd-49a5-a407-f248957bb9aa",
                            "name": "tag1"
                        }, {
                            "vocabulary_id": null,
                            "state": "active",
                            "display_name": "tag2",
                            "id": "af9fd176-159a-4b3d-992f-7c6b63454380",
                            "name": "tag2"
                        }],
                        "groups": [{
                            "display_name": "Mi grupo",
                            "description": "description del grupo.",
                            "image_display_url": "",
                            "title": "Recurso 02",
                            "id": "190fec73-93bb-42ca-b200-32073c7f9e09",
                            "name": "recurso-02"
                        }],
                        "license_id": null,
                        "relationships_as_subject": [],
                        "organization": {
                            "description": "Desc. de la organizacion.",
                            "created": "2017-05-04T18:39:20.234625",
                            "title": "Organization 01",
                            "name": "organization-01",
                            "is_organization": true,
                            "state": "active",
                            "image_url": "",
                            "revision_id": "062aea2f-57ed-4ea8-b444-907adcaf0a4d",
                            "type": "organization",
                            "id": "a8c81406-0c96-4b10-b4dc-606cf3777416",
                            "approval_status": "approved"
                        },
                        "name": "dataset-01-test",
                        "isopen": false,
                        "url": null,
                        "notes": null,
                        "owner_org": "a8c81406-0c96-4b10-b4dc-606cf3777416",
                        "extras": [],
                        "title": "Dataset 01 Test",
                        "revision_id": "ee7170dc-f1b1-465b-87b6-1d1a9d708d3a"
                    }
                }
                '''
        },
    'package_search':
        {
            'case1':
                '''
                {
                    "help": "http://localhost:5000/api/3/action/help_show?name=package_search",
                    "success": true,
                    "result": {
                        "count": 1,
                        "sort": "score desc, metadata_modified desc",
                        "facets": {},
                        "results": [{
                            "license_title": "Creative Commons Attribution",
                            "maintainer": "Some Maintainer",
                            "relationships_as_object": [],
                            "private": false,
                            "maintainer_email": "maintainer@email.com",
                            "num_tags": 3,
                            "id": "1111a111-2222-3333-d4dd-555e555555e5",
                            "metadata_created": "2016-11-30T22:22:48.635757",
                            "metadata_modified": "2017-02-22T19:11:11.510624",
                            "author": "Andino",
                            "author_email": "author@email.com",
                            "state": "active",
                            "version": null,
                            "creator_user_id": "15d5e48f-8593-4265-844c-35438718bda7",
                            "type": "dataset",
                            "resources": [{
                                "cache_last_updated": null,
                                "attributesDescription": "[]",
                                "package_id": "6897d435-8084-4685-b8ce-304b190755e4",
                                "webstore_last_updated": null,
                                "datastore_active": true,
                                "id": "6145bf1c-a2fb-4bb5-b090-bb25f8419198",
                                "size": null,
                                "state": "active",
                                "license_id": "cc-by",
                                "hash": "",
                                "description": "una description",
                                "format": "CSV",
                                "last_modified": "2016-11-30T22:24:01.225394",
                                "url_type": "upload",
                                "mimetype": null,
                                "cache_url": null,
                                "name": "Recurso de ejemplo",
                                "created": "2016-11-30T22:24:01.259909",
                                "url": "http://localhost:5000/dataset/6897d435-8084-4685-b8ce-304b190755e4/resource/6145bf1c-a2fb-4bb5-b090-bb25f8419198/download/recurso.csv",
                                "webstore_url": null,
                                "mimetype_inner": null,
                                "position": 0,
                                "revision_id": "93775e68-be07-43cb-a824-cac468f4ca94",
                                "resource_type": null
                            }],
                            "num_resources": 1,
                            "tags": [{
                                "vocabulary_id": null,
                                "state": "active",
                                "display_name": "Test",
                                "id": "02e60be2-e90e-4b7b-ad57-e8491b461585",
                                "name": "test"
                            }, {
                                "vocabulary_id": null,
                                "state": "active",
                                "display_name": "Demo",
                                "id": "ce375c0e-d8f2-493a-9e90-9552bad125fb",
                                "name": "demo"
                            }, {
                                "vocabulary_id": null,
                                "state": "active",
                                "display_name": "ckan-uploader",
                                "id": "3044895a-7953-4998-9030-18535e87d457",
                                "name": "ckan-uploader"
                            }],
                            "groups": [{
                                "display_name": "Tema (ejemplo)",
                                "description": "Ejemplo de un tema.",
                                "image_display_url": "http://localhost:5000/uploads/group/2016-11-30-222445.887067Portal-de-datos-grupos-02.svg",
                                "title": "Tema (ejemplo)",
                                "id": "ebfbfd0f-a248-4bee-bf86-7ccf3090a3fb",
                                "name": "tema-demo"
                            }],
                            "license_id": "cc-by",
                            "relationships_as_subject": [],
                            "organization": {
                                "description": "",
                                "created": "2016-11-30T22:06:03.490514",
                                "title": "Mi organizaci\u00f3n (Demo)",
                                "name": "mi-organizacion-demo",
                                "is_organization": true,
                                "state": "active",
                                "image_url": "",
                                "revision_id": "1de834ea-bc6f-4caa-8f1d-5e8ff5de7c3a",
                                "type": "organization",
                                "id": "199c68cf-0f42-4d40-824f-a6a9a5bef2a6",
                                "approval_status": "approved"
                            },
                            "name": "dataset-03-test",
                            "isopen": true,
                            "url": "https://github.com/datosgobar/portal-andino ",
                            "notes": "Este es un dataset de ejemplo, se incluye como material de ejemplo y no contiene ningun valor estadistico.",
                            "owner_org": "199c68cf-0f42-4d40-824f-a6a9a5bef2a6",
                            "extras": [{
                                "key": "Documentaci\u00f3n",
                                "value": "https://github.com/datosgobar/portal-andino/blob/master/README.md"
                            }, {
                                "key": "globalGroups",
                                "value": "[\"TECH\"]"
                            }, {
                                "key": "home_featured",
                                "value": "true"
                            }, {
                                "key": "language",
                                "value": "[\"spa\"]"
                            }, {
                                "key": "updateFrequency",
                                "value": "R/P1D"
                            }],
                            "license_url": "http://www.opendefinition.org/licenses/cc-by",
                            "title": "Dataset 03 Test",
                            "revision_id": "15582615-d949-4d66-b4f6-80c9df38ed13"
                        }
                        ],
                        "search_facets": {}
                    }
                }
                '''
        }
}


class TestCase(unittest.TestCase):
    """
    Tests para el controlador principal de la lib.
    """

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

    def test_04_correct_init(self):
        """
        Crear instancia de CKANUploader con datos erroneos.

        Hipotesis:
        =========
            Si los argumentos provistos son str() y validos, la lib deberia inicializarse sin problemas.

        """
        cl = CKANUploader(CKAN_HOST, CKAN_APIKEY)
        print cl.host_url  # Imprimimos las url de nuestro ckan remoto.

    @responses.activate
    def test_05_search_for_a_dataset(self):
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
        assert_equals(cl.exists('dataset-01-test'), True)

    @responses.activate
    def test_06_search_for_a_distribution(self):
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
        assert_equals(cl.exists('mi-recurso-del-ejemplo', search_for_datasets=False), True)

    @responses.activate
    def test_07_get_datasets_list_returns_always_a_list(self):
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

    @responses.activate
    def test_08_get_all_distributions_returns_always_a_dict(self):
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
        assert_equals(cl.get_all_distrubutions(), {u'fa05d5c0-7a2d-4ea5-9539-08e9bbe71e23': u'Mi Recurso del Ejemplo'})