# -*- coding: utf-8 -*-


class Dataset(object):
    """Clase contenedora para Datasets."""
    def __init__(self, datadict=None):
        self.required_keys = ["license_title", "maintainer", "private",
                              "maintainer_email", "metadata_created",
                              "author", "author_email", "state", "type",
                              "resources", "tags", "groups", "license_id",
                              "organization", "url", "notes", "owner_org",
                              "extras", "license_url", "title",
                              "metadata_modified", "title", "name"]
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


class Distribution(object):
    """Clase Contenedora para distribuciones.
    """
    def __init__(self):
        pass