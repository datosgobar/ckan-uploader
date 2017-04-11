# -*- coding:utf-8 -*-


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

    def update(self, datadict=None):
        """
        Actualizar Datasets o Distribuciones.

        :return:
        """

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
            raise TypeError('El agumento \"only_names\" requiere ser de tipo \"bool\".')
        if only_names:
            return self.my_remote_ckan.action.package_list()
        else:
            return self.my_remote_ckan.action.package_search()['results']


