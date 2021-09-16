import logging

from django.db.backends.postgresql.schema import (
    DatabaseSchemaEditor as PGDatabaseSchemaEditor,
)
logger = logging.getLogger('yb_backend.schema')

class DatabaseSchemaEditor(PGDatabaseSchemaEditor):
    def _alter_field(self, model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params, strict=False):
        # Refer https://github.com/yugabyte/yugabyte-db/issues/7762
        if old_type != new_type:
            # Increasing the size of varchar is supported
            if old_type.lower().startswith("varchar(") and new_type.lower().startswith("varchar("):
                conv = lambda i: i or 8
                o_len = int(old_type[8:conv(old_type.index(")"))])
                n_len = int(new_type[8:conv(new_type.index(")"))])
                if o_len > n_len:
                    logger.warning("Warning: YB does not allow changing the column %s type from %s to %s " % (
                    old_field, old_type, new_type))
                    return
            else:
                logger.warning("Warning: YB does not allow changing the column %s type from %s to %s " % (old_field, old_type, new_type))
                return
        super()._alter_field(model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params, strict)
