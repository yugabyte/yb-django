from django.db.backends.postgresql.introspection import (
    DatabaseIntrospection as PGDatabaseIntrospection,
)


class DatabaseIntrospection(PGDatabaseIntrospection):
    # The default access method for Yugabyte is lsm as compared to postgres btree
    index_default_access_method = "lsm"