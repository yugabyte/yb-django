from django.db.backends.postgresql.features import (
    DatabaseFeatures as PGDatabaseFeatures,
)


class DatabaseFeatures(PGDatabaseFeatures):
    # Refer https://github.com/yugabyte/yugabyte-db/issues/7764

    allows_group_by_lob = False
    supports_deferrable_unique_constraints = False
    uses_savepoints = False
    can_release_savepoints = False

    # With YB, transactions may start generating conflicts if one transaction does
    # "select for update". While in Postgres, the transactions wait. To overcome
    # this, YB users should implement a retry logic
    has_select_for_update = True
    has_select_for_update_of = True
    has_select_for_no_key_update = True
    supports_select_for_update_with_limit = True

    has_select_for_update_nowait = False
    has_select_for_update_skip_locked = False
    can_introspect_materialized_views = False
    can_rollback_ddl = False
    indexes_foreign_keys = False
    can_clone_databases = False
    supports_ignore_conflicts = False
    supports_covering_indexes = True

    supports_collation_on_charfield = False
    supports_collation_on_textfield = False
    supports_non_deterministic_collations = False
    supports_tablespaces = False