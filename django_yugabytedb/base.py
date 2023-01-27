from django.core.exceptions import ImproperlyConfigured
from django.utils.version import get_version_tuple


try:
    import psycopg2 as Database
    import psycopg2.extensions
    import psycopg2.extras
except ImportError as e:
    raise ImproperlyConfigured("Error loading psycopg2 module: %s" % e)


def psycopg2_version():
    version = psycopg2.__version__.split(' ', 1)[0]
    return get_version_tuple(version)


PSYCOPG2_VERSION = psycopg2_version()

if PSYCOPG2_VERSION < (2, 5, 4):
    raise ImproperlyConfigured("psycopg2_version 2.5.4 or newer is required; you have %s" % psycopg2.__version__)

from .client import DatabaseClient  # NOQA
from .creation import DatabaseCreation  # NOQA
from .features import DatabaseFeatures  # NOQA
from .introspection import DatabaseIntrospection  # NOQA
from .operations import DatabaseOperations  # NOQA
from .schema import DatabaseSchemaEditor  # NOQA


from django.db.backends.postgresql.base import (
    DatabaseWrapper as PGDatabaseWrapper,
)


class DatabaseWrapper(PGDatabaseWrapper):
    vendor = 'yugabyte'
    display_name = 'YugabyteDB'
    # Override some types from the postgresql adapter.
    # Refer https://github.com/yugabyte/yugabyte-db/issues/7761
    data_types = dict(
        PGDatabaseWrapper.data_types,
        IPAddressField = 'varchar(15)',
        GenericIPAddressField = 'varchar(39)',
    )
    SchemaEditorClass = DatabaseSchemaEditor
    creation_class = DatabaseCreation
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations
    client_class = DatabaseClient

   # def savepoint(self):
        # We override savepoint function to overcome the issue mentioned here
        # https://code.djangoproject.com/ticket/28263
        # https://code.djangoproject.com/ticket/32527
        # https://github.com/yugabyte/yugabyte-db/issues/7760
        #return 1

    def get_connection_params(self):
        conn_params =  super().get_connection_params()
        settings_dict = self.settings_dict
        load_balance = settings_dict.get("LOAD_BALANCE")
        topology_keys = settings_dict.get("TOPOLOGY_KEYS")
        if load_balance:
            conn_params["load_balance"] = load_balance
        if topology_keys:
            conn_params["topology_keys"] = topology_keys
        
        return conn_params

