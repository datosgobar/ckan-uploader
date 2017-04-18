# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from models import Dataset, Distribution, MyLogger
from ckanapi import NotAuthorized, ValidationError


class CKANUploader(object):
    def __init__(self, ckan_url=None, ckan_api_key=None):
        """
        Inicializacion del Modulo CKANUploader

        Args:
        ====
            ckan_api_key: Str().
                    - Este campo no puede ser vacio. len(obj) == 0
                    - API-KEY de CKAN para realizar tareas dentro de CKAN
                      Se requiere que el usuario propietario de la API-KEY tenga permisos.
                      de actualizacion y carga de activos de datos.

            ckan_url: Str().
                     - Este campo no puede ser vacio, len(obj) == 0.
                     - URL al portal de datos.

        """
        if None in [ckan_api_key, ckan_url] or \
                not isinstance(ckan_url, str) or \
                not isinstance(ckan_api_key, str):
            raise TypeError
        if 0 in [len(ckan_api_key), len(ckan_url)]:
            # Si alguno de los argumentos provistos es de logitud 0
            # "suelto" una exception ValueError
            raise ValueError
        self.host_url = ckan_url
        self.api_key = ckan_api_key
        self.ua = 'ckan_uploader/1.0 (+https://github.com/datosgobar/ckan_uploader)'
        self.log = MyLogger(logger_name='{}.controller'.format(__name__),
                            log_level='INFO')
        import ckanapi
        self.my_remote_ckan = ckanapi.RemoteCKAN(self.host_url, apikey=self.api_key, user_agent=self.ua)

    def exists(self, id_or_name='', search_for_datasets=True):
        """
        Chequea la existencia de un Dataset o un recurso.

        Args:
        ====
            - id_or_name: str(). ID o Nombre del objeto que se requiere chequear.
                          Para datasets, se admite que se use Name o ID, mientras que para
                          distribuciones, solo se podra buscar mediante ID.

            - search_for_datasets: bool(). FLAG,
                - True: Se busca un Dataset.
                - False: Se busca un distribucion.
                - default: True(Busqueda para datasets)

        Returns:
        =======
            - bool():
                - True: Existe el objeto buscado.
                - False: No existe el objeto buscado.
        """
        # Si el tipo de los argumentos provistos no es el esperado,
        # salgo con una exception TypeError.
        if not isinstance(id_or_name, (str, unicode)) or not isinstance(search_for_datasets, bool):
            raise TypeError

        # Si id_or_name es una cadena vacia, salgo con un exception ValueError.
        if len(id_or_name) == 0:
            raise ValueError
        # Si el flag search_for_datasets == True, busco sobre los datasets.
        if search_for_datasets:
            avalailable_datasets = self.my_remote_ckan.action.package_list()
            return id_or_name in avalailable_datasets
        else:
            # Considero que estoy buscando una distribution
            all_distributions = self.get_all_distrubutions()
            dist_by_ids = [_id for _id in all_distributions.keys()]
            dist_by_names = [all_distributions[_id] for _id in all_distributions.keys()]
            return id_or_name in dist_by_ids or id_or_name in dist_by_names

    def _render_name(self, title=None, _encoding='utf-8'):
        """
        Formatea cadenas de textos a formato de nombres para ckan.

        Este metodo aplica las siguientes transformaciones:
        - Cambiar espacios por guiones medios.
        - Toda la frase en minusculas.
        - Quita caracteres que no sean alfanumericos.

        Args:
            - name: str() o unicode().
        Returns:
            - str:
        """
        import re
        import unicodedata

        def strip_accents(text):
            """Quitar acentos."""
            try:
                try:
                    text = unicode(text, _encoding)
                except NameError:
                    pass
                text = unicodedata.normalize('NFD', text)
                text = text.encode('ascii', 'ignore')
                text = text.decode("utf-8")
            except Exception as e:
                self.log.error(str(e))
            return str(text)

        text = strip_accents(title.lower())
        text = re.sub('[ ]+', '-', text)
        text = re.sub('[^0-9a-zA-Z_-]', '', text)
        return text

    def create_dataset(self, dataset=None):
        """
        Crea un nuevo dataset en un CKAN remoto.

        Args:
             - dataset:
        Returns:
             - TODO.
        """
        status = False
        if not isinstance(dataset, Dataset):
            raise TypeError
        try:
            dataset.name = self._render_name(dataset.title)
            dataset.groups = self.build_groups(dataset.groups)
            self.my_remote_ckan.action.package_create(**dataset.__dict__)
            status = True
        except NotAuthorized:
            self.log.error('No posee los permisos requeridos para crear el dataset {}.'
                           ''.format(dataset.title))
        except ValidationError:
            self.log.error('No es posible crear el dataset \"{}\", el mismo ya existe.'
                           ''.format(dataset.title))
        return status

    def update_dataset(self, dataset=None):
        """
        Actualizar Datasets o Distribuciones.

        Args:
            - dataset: Dataset().
        """
        if not isinstance(dataset, Dataset):
            raise TypeError
        status = False
        update_this_dataset = dataset.__dict__
        unrequired_keys = ['required_keys', 'context']
        for k in unrequired_keys:
            if k in update_this_dataset.keys():
                del update_this_dataset[k]
        try:
            update_this_dataset['name'] = self._render_name(dataset.title)
            update_this_dataset['groups'] = self.build_groups(dataset.groups)
            self.my_remote_ckan.action.package_update(**update_this_dataset)
            status = True
        except NotAuthorized:
            self.log.error('No posee los permisos requeridos para crear el dataset {}.'
                           ''.format(dataset.title))
        except ValidationError:
            self.log.error('No es posible crear el dataset \"{}\", el mismo ya existe.'
                           ''.format(dataset.title))
        return status

    def get_distributions(self, id_or_name=None, all_platform=False):
        """
        Retona lista de distribuciones contenidas dentro de un Dataset.

        Args:
            - id_or_name:
                - Str().
                - ID o NAME de un dataset.
                - Si id_or_name no es unicode o str, sale con una exception TypeError.
                - Si el id_or_name no existe dentro de la plataforma, sale con una Exception ValueError.
        Returns:
            - List()
        """
        # Validaciones de campos:
        if not isinstance(id_or_name, (str, unicode)) or \
                not isinstance(all_platform, bool):
            err_msg = 'Los Argumentos provistos no son validos...'
            self.log.error(err_msg)
            raise TypeError(err_msg)
        # Chequeo que exista el dataset seleccionado.
        if not self.exists(id_or_name=id_or_name):
            err_msg = 'No existe Dataset con ID o NAME == {}'.format(id_or_name)
            self.log.error(err_msg)
            raise ValueError(err_msg)

    def get_all_distrubutions(self):
        """
        Diccionario de distrubuciones disponibles en el CKAN remoto: self.ckan_url.

        Args:
        ====
            - None.

        Returns:
        ========
            - dict().
        """
        distributions = {}
        all_datasets = self.my_remote_ckan.action.package_list()
        for dataset in all_datasets:
            ds_dist = self.my_remote_ckan.call_action('package_show', {'id': dataset})
            ds_dist = ds_dist['resources']
            for d in ds_dist:
                distributions.update({d['id']: d['name']})
        return distributions

    @staticmethod
    def diff_datasets(dataset_a=None, dataset_b=None):
        """
        Compara dos datasets y retorna la diferencia aditiva de ambos.

        Cuando se realiza la diferencia, el valor que prevalece es el de
        dataset_b.

        Args:
        ====
            - dataset_a:
                - Dataset().
                - Solo admite ser de tipo Dataset().

            - dataset_b:
                - Dataset().
                - Solo admite ser de tipo Dataset().

        Returns:
        =======
            - Dataset().

        Exceptions:
        ==========
            TypeError:
                - Uno o ambos argumentos, no son de clase Dataset.
        """
        for v in [dataset_a, dataset_b]:
            if not isinstance(v, Dataset):
                raise TypeError('Para comparar los datasets ambos deben ser de clase Dataset.')
        diff_ds = {}
        omit_this_keys = ['required_keys', 'context']
        for k, v in dataset_a.__dict__.items():
            if k not in omit_this_keys:
                if v != dataset_b.__dict__[k]:
                    diff_ds.update({k: dataset_b.__dict__[k]})
                else:
                    diff_ds.update({k: v})
        return Dataset(datadict=diff_ds,
                       _distributions=dataset_a.__dict__['resources'],
                       _distribution_literal=True)

    def freeze_dataset(self, id_or_name):
        """
        Crea una imagen temporal del contenido de un dataset.

        Args:
        ====
            - id_or_name:
                - str().
                - Id o Nombre del dataset que deseo freezar.
        Returns:
        =======
            - Dataset: Si el objeto es localizable & "Freezable".

        Exceptions:
        ==========
            - ValueError:
                - id_or_name esta unicode o str pero es del len == 0.
            - TypeError:
                - id_or_name no es un str o unicode.
        """
        stored_dataset = self.retrieve_dataset_metadata(id_or_name)
        if stored_dataset:
            freezed_dataset = {"license_title": stored_dataset['license_title'],
                               "maintainer": stored_dataset['maintainer'],
                               "private": stored_dataset['private'],
                               "maintainer_email": stored_dataset['maintainer_email'],
                               "id": stored_dataset['id'],
                               "owner_org": stored_dataset['owner_org'],
                               "author": stored_dataset['author'],
                               "isopen": stored_dataset['isopen'],
                               "author_email": stored_dataset['author_email'],
                               "state": stored_dataset['state'],
                               "license_id": stored_dataset['license_id'],
                               "type": stored_dataset['type'],
                               "groups": [g['name'] for g in stored_dataset['groups']],
                               "creator_user_id": stored_dataset['creator_user_id'],
                               "name": stored_dataset['name'],
                               "url": stored_dataset['url'],
                               "notes": stored_dataset['notes'],
                               "title": stored_dataset['title'],
                               "license_url": stored_dataset['license_url']}
            return Dataset(datadict=freezed_dataset,
                           _distribution_literal=True,
                           _distributions=stored_dataset['resources'])

    def get_datasets_list(self, only_names=True):
        """
        Obtener lista de Datasets y Recursos remotos.

        Args:
            - only_names = bool(). FLAG.
                            - True: Lista con solo los nombres de los dataset de self.ckan_url.
                            - False: Lista con todos los datos de los dataset de self.ckan_url.

        Returns:
        ========
            - list().
                - len(list) == 0: No existen datos.
                - len(list) == n, lista de n datasets.

        Exceptions:
        ==========
            - TypeError:
                - only_names no es de clase bool.
        """
        if not isinstance(only_names, bool):
            err_msg = 'El agumento \"only_names\" requiere ser de tipo \"bool\".'
            self.log.error(err_msg)
            raise TypeError(err_msg)
        if only_names:
            return self.my_remote_ckan.action.package_list()
        else:
            return self.my_remote_ckan.action.package_search()['results']

    def retrieve_dataset_metadata(self, id_or_name=None):
        """
        Retorna metadata de un dataset.

        Args:
        ====
            - id_or_name: str(). nombre o id del dataset requerido

        Returns:
        =======
            - dict():
            - None: No existe el recurso.

        Exceptions:
        ==========
            - TypeError:
                - id_or_name no es de clase str o unicode.
        """
        if not isinstance(id_or_name, (unicode, str)):
            raise TypeError
        try:
            ds = self.my_remote_ckan.call_action('package_show',
                                                 data_dict={'id': id_or_name})
            return ds
        except Exception as e:
            self.log.error(e)

    def build_groups(self, groups=None, _selected_keys=None):
        """Formatea los grupos para poder incluirlos dentro de la creacion | actualizacion de los datasets."""
        fixed_groups = []
        if not isinstance(groups, list):
            raise TypeError('El argumento \"groups\" requiere ser una lista.')
        if None in [_selected_keys]:
            requiered_keys = ['id']
        elif isinstance(_selected_keys, list):
            requiered_keys = _selected_keys
        else:
            err_msg = 'El Argumento \"_selected_keys\" no puede ser \"{}\"'.format(type(_selected_keys))
            self.log.error(err_msg)
            raise TypeError(err_msg)
        platform_groups_list = self.my_remote_ckan.action.group_list()
        if False in [True for g in groups if g in platform_groups_list]:
            err_msg = 'No esposible seleccionar el grupo especifico.'
            self.log.error(err_msg)
            raise ValueError(err_msg)
        for g in groups:
            mg = self.my_remote_ckan.call_action('group_show', data_dict={'id': g})
            fix_me = {}
            for rk in requiered_keys:
                fix_me.update({rk: mg[rk]})
            fixed_groups.append(fix_me)
        return fixed_groups

    def _push_distribution(self, _d=None):
        """
        Carga a CKAN una distribucion.

        Returns:
             - bool.
                - True, exito al salvar la distribucion.
                - False, ocurrio un fallo al salvar la distribucion.

        """
        status = False
        if not isinstance(_d, Distribution):
            raise TypeError('Distrubucion invalida.')
        _dis = _d.__dict__
        _dis.update({'name': _d.name,
                     'description': _d.description.decode('utf-8')})
        try:
            del _dis['required_keys']
        except KeyError:
            pass

        if 'file' in _d.__dict__.keys():
            # Metodo UPLOAD.
            _dis.update({'upload': open(_d.file, 'rb'),
                         'url_type': 'upload',
                         'datastore_active': True})

        else:
            # Metodo 'LINK'
            self.log.info('Push method: LINK')
            print _dis['url']
            _dis.update({'link': _dis['url'],
                         'url_type': 'link',
                         'datastore_active': False})

        try:
            self.my_remote_ckan.action.resource_create(**_dis)
            status = True
        except NotAuthorized:
            self.log.critical('No posee permisos para actualizar|crear distribuciones.')
        except ValidationError:
            self.log.critical('No es posible actualizar|crear el distribuciones con la data provista.')
        return status

    def save(self, _obj=None):
        """
        Guarda un _obj dentro de CKAN.

        Si el _obj existe, lo actualiza, si no, lo creo.
        De la misma manera son tratadas las distribuciones que el mismo contenga.

        Args:
            - _obj: _obj().
        Returns:
             - bool():
                - True se salvo correctamente el _obj.
                - False: Fallo la carga del _obj.
        """
        ds_status = False
        dis_status = False
        distributions = []
        if type(_obj) not in [Dataset, list, Distribution]:
            raise TypeError
        if isinstance(_obj, list):
            # Si es una lista, solo voy a intentar salvar los
            #  que son instancias de la clase _obj.
            for o in _obj:
                if isinstance(o, (Dataset, Distribution)):
                    self.save(o)
                else:
                    # Si _obj[n] no es _obj o Distribution lo omito.
                    self.log.info('Se omite {} por no ser una instancia de '
                                  '_obj() o de Distribution.'.format(o))
        if isinstance(_obj, Dataset):
            if 'resources' in _obj.__dict__.keys():
                distributions = _obj.resources
                _obj.resources = []
            ds_name = self._render_name(title=_obj.title)
            if self.exists(id_or_name=ds_name.decode('utf-8 ')):
                # Actualizo el _obj.
                self.log.info('El _obj \"{}\" existe, por tanto, se actualizara.'.format(ds_name))
                # Antes de actualizar debo bajar toda la metadata del dataset,
                # para que no se sobre escriba de manera erroenea el mismo al
                # realizar el update.
                ds_remote = self.freeze_dataset(ds_name)
                if self.update_dataset(dataset=self.diff_datasets(ds_remote, _obj)):
                    self.log.info('_obj \"{}\" actualizado correctamente.'.format(ds_name))
                    ds_status = True
            else:
                # Caso contrario, lo creo.
                self.log.info('El _obj \"{d}\" no existe. Creando _obj \"{d}\"...'.format(d=ds_name))
                if self.create_dataset(dataset=_obj):
                    self.log.info('_obj \"{}\" fue creado con exito.'.format(ds_name))
                    ds_status = True
            if len(distributions) > 0:
                self.log.info('Guardando distribuciones({})...'.format(len(distributions)))
                for d in distributions:
                    d.package_id = ds_name
                    self.save(d)
            return ds_status
        import helpers
        if isinstance(_obj, Distribution):
            if isinstance(_obj, Distribution):
                dist_name = _obj.name
                self.log.info('Salvando Distribucion \"{}\".'.format(dist_name))
                if self.exists(id_or_name=_obj.name, search_for_datasets=False):
                    self.log.info('Actualizando distribucion \"{}\".'.format(dist_name))
                else:
                    self.log.info('La distribucion \"%s\" no existe,'
                                  ' creando nueva distribucion.' % dist_name)
                    if self._push_distribution(_obj):
                        dis_status = True
        elif helpers.list_of(_obj, Distribution):
            for m in _obj.__dict__.keys():
                self.save(m)
        return dis_status and ds_status
