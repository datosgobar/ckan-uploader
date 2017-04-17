# -*- coding:utf-8 -*-
from models import Dataset, Distribution, Errs
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
        import logging
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('{}.controller'.format(__name__))
        self.errs = []
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
        if not isinstance(id_or_name, str) or not isinstance(search_for_datasets, bool):
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
            dist_by_name = [_name for _name in all_distributions]
            return id_or_name in dist_by_ids or id_or_name in dist_by_name

    @staticmethod
    def _render_name(title=None, _encoding='utf-8'):
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
                text = unicode(text, _encoding)
            except NameError:  # unicode is a default on python 3
                pass
            text = unicodedata.normalize('NFD', text)
            text = text.encode('ascii', 'ignore')
            text = text.decode("utf-8")
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
        try:
            dataset.name = self._render_name(dataset.title)
            dataset.groups = self.build_groups(dataset.groups)
            self.my_remote_ckan.action.package_update(**dataset.__dict__)
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
            - id_or_name: str(). nombre o id del dataset requerido

        Returns:
            - dict():
            - None: No existe el recurso.
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

    def save(self, dataset=None):
        """
        Guarda un dataset dentro de CKAN.

        Si el dataset existe, lo actualiza, si no, lo creo.
        De la misma manera son tratadas las distribuciones que el mismo contenga.

        Args:
            - dataset: Dataset().
        Returns:
             - bool():
                - True se salvo correctamente el dataset.
                - False: Fallo la carga del dataset.
        """
        status = False
        if not isinstance(dataset, (Dataset, list)):
            raise TypeError
        if isinstance(dataset, list):
            # Si es una lista, solo voy a intentar salvar los
            #  que son instancias de la clase Dataset.
            for o in dataset:
                if isinstance(o, dataset):
                    self.save(o)
                else:
                    # Si dataset[n] no es Dataset lo omito.
                    self.log.info('Se omite {} por no ser una instancia de Dataset().'.format(o))
                    pass
        if 'resources' in dataset.__dict__.keys():
            distributions = dataset.resources
        ds_name = self._render_name(dataset.title)
        if self.exists(id_or_name=ds_name):
            # Actualizo el dataset.
            self.log.info('El dataset \"{}\" existe, por tanto, se actualizara...'.format(ds_name))
            if self.update_dataset(dataset=dataset):
                self.log.info('Dataset \"{}\" actualizado correctamente.'.format(ds_name))
                status = True
        else:
            # Caso contrario, lo creo.
            self.log.info('El dataset \"{d}\" no existe. Creando dataset \"{d}\"...'.format(d=ds_name))
            if self.create_dataset(dataset=dataset):
                self.log.info('Dataset \"{}\" fue creado con exito.'.format(ds_name))
                status = True
        return status
