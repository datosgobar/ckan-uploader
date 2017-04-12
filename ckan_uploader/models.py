# -*- coding: utf-8 -*-


class CKANElement(object):
    """Clase generica para contener elementos elementos de CKAN."""

    def __init__(self, _required_keys=None, datadict=None, forced_keys=None):
        if not isinstance(_required_keys, list):
            raise TypeError('El argumento \"_required_keys\" requiere ser de tipo \"list\"')
        self.required_keys = _required_keys
        self._load(datadict, forced_keys)

    def _load(self, datadict=None, _forced_keys=None):
        # Chequeo que dataset sea un Diccionario.
        if not isinstance(datadict, dict):
            raise TypeError("El argumento \"datadict\" debe ser un diccionario.")
        # Chequeo que dataset posea todas las claves que
        # requiero para crear una instancia de Dataset
        for rk in self.required_keys:
            # Si la clave requerida, no existe dentro de "datadict"
            # salgo con una exception KeyError.
            if rk not in datadict.keys():
                raise KeyError('La clave: {}, es requerida.'.format(rk))
            else:
                # si la clave existe, la agrego.
                setattr(self, rk, datadict[rk])
        if None not in [_forced_keys] and isinstance(_forced_keys, dict):
            for k, v in _forced_keys.items():
                setattr(self, k, v)


class Dataset(CKANElement):
    """Clase contenedora para Datasets."""

    def __init__(self, datadict=None, _distributions=None):
        required_keys = ["license_title", "maintainer", "private",
                         "maintainer_email", "author", "author_email",
                         "state", "type", "groups", "license_id",
                         "owner_org", "url", "notes", "owner_org",
                         "license_url", "title", "title", "name"]
        super(Dataset, self).__init__(_required_keys=required_keys,
                                      datadict=datadict,
                                      forced_keys={'resources': _distributions or []})


class Distribution(CKANElement):
    """Clase contenedora para Distributions."""

    def __init__(self, datadict=None):
        required_keys = ["package_id", "size", "state", "license_id", "hash",
                         "description", "format", "url_type", "mimetype", "name", "url"]
        super(Distribution, self).__init__(required_keys, datadict)
