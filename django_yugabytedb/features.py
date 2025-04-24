from django.db.backends.postgresql.features import (
    DatabaseFeatures as PGDatabaseFeatures,
)
from django.utils.functional import cached_property
from django import __version__ as _ver
import os

class DatabaseFeatures(PGDatabaseFeatures):

    # Minimum version of yugabytedb
    minimum_database_version = (2,14)

    # Refer https://github.com/yugabyte/yugabyte-db/issues/7764

    allows_group_by_lob = False
    supports_deferrable_unique_constraints = False
    uses_savepoints = True
    can_release_savepoints = True

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
    indexes_foreign_keys = True
    can_clone_databases = False
    supports_ignore_conflicts = True
    supports_covering_indexes = True

    supports_collation_on_charfield = False
    supports_collation_on_textfield = False
    supports_non_deterministic_collations = False
    supports_tablespaces = False

    @cached_property
    def django_test_expected_failures(self):
        base_expected_failures = super().django_test_expected_failures
        base_expected_failures.update({
            # Deferrable constraints not honoured in child table deferred UPDATE scenario. 
            # GH Issue: https://github.com/yugabyte/yugabyte-db/issues/9288
            'migrations.test_operations.OperationTests.test_add_field_m2m',
            'migrations.test_operations.OperationTests.test_create_model_m2m',

            # Lack of Pessimistic Locking support which will need app to retry the transaction.
            'migrations.test_operations.OperationTests.test_run_sql',

            # INDEX on column of type 'JSONB' not yet supported
            'schema.tests.SchemaTests.test_func_index_json_key_transform',
            'schema.tests.SchemaTests.test_func_index_json_key_transform_cast',
            
        })


        if float(_ver[0:3]) <= 4.0 :
            base_expected_failures.update({

            # YB does not allow changing the column type from integer to serial
            'schema.tests.SchemaTests.test_alter_int_pk_to_autofield_pk',
            # YB does not allow changing the column type from serial to integer
            'schema.tests.SchemaTests.test_alter_auto_field_to_integer_field',

              })
            
        expected_failures = base_expected_failures 

        yb_version = os.getenv('YB_VERSION')
        yb_version_major = yb_version.split('.')[0]
        yb_version_minor = yb_version.split('.')[1]

        if float(yb_version[0:4]) <= 2.18:
            expected_failures.update({
                # Backfilling of existing rows when new column is added with default value is not yet implemented in yugabytedb. 
                # The test inserts data and then tries to add columns with default value. 
                # GH Issue : https://github.com/yugabyte/yugabyte-db/issues/4415
                'migrations.test_operations.OperationTests.test_add_binaryfield',
                'migrations.test_operations.OperationTests.test_add_charfield',
                'migrations.test_operations.OperationTests.test_add_textfield',
                'migrations.test_operations.OperationTests.test_alter_order_with_respect_to',
                'schema.tests.SchemaTests.test_add_datefield_and_datetimefield_use_effective_default',
                'schema.tests.SchemaTests.test_add_field_default_dropped',
                'schema.tests.SchemaTests.test_add_field_default_transform',
                'schema.tests.SchemaTests.test_add_field_use_effective_default',
                

                # Yugabyte does not allow changing column type from integer to bigint.
                'migrations.test_operations.OperationTests.test_alter_fk_non_fk', 
                # GH Issue: https://github.com/yugabyte/yugabyte-db/issues/7762
                'migrations.test_operations.OperationTests.test_autofield__bigautofield_foreignfield_growth',

                # YB does not allow changing the column test_blog.Blog.id type from smallint to integer
                'migrations.test_operations.OperationTests.test_smallfield_autofield_foreignfield_growth',
                'migrations.test_operations.OperationTests.test_smallfield_bigautofield_foreignfield_growth',

                # Yugabyte does not allow changing the column type from varchar(255) to text
                'schema.tests.SchemaTests.test_alter',

                # CREATE TABLE "INTEGERPK" ("i" integer NOT NULL PRIMARY KEY, "j" integer NOT NULL UNIQUE);
                # INSERT INTO "INTEGERPK" ("j") VALUES (1) RETURNING "INTEGERPK"."i";
                # Does not work with yugabytedb without the PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY clause.
                'schema.tests.SchemaTests.test_alter_int_pk_to_bigautofield_pk',

                # Yugabyte does not allow changing the column type from varchar(31) to integer
                'schema.tests.SchemaTests.test_char_field_with_db_index_to_fk',

                # The test is renaming the column 'name' to 'display_name'. 
                # The size of column 'name' is varchar(255). 
                # The column 'display_name' is getting renamed with varchar(254) in the test. 
                # Yugabyte does not support changing the column type from varchar(255) to varchar(254). Hence the column is not getting renamed to 'display_name'
                'schema.tests.SchemaTests.test_rename',

                # Yugabyte does not allow changing the column type from text to integer 
                'schema.tests.SchemaTests.test_text_field_with_db_index_to_fk',


            })

            if float(_ver[0:3]) >= 4.2:
                expected_failures.update({
                # Backfilling of existing rows when new column is added with default value is not yet implemented in yugabytedb. 
                # The test inserts data and then tries to add columns with default value. 
                # GH Issue : https://github.com/yugabyte/yugabyte-db/issues/4415
                'schema.tests.SchemaTests.test_add_db_comment_and_default_charfield',
            })

        if (yb_version_major == '2024' and yb_version_minor == '1') or float(yb_version[0:4]) < 2.23:
            expected_failures.update({
                # Alter table Add column Unique is not yet supported. 
                # GH Issue: https://github.com/yugabyte/yugabyte-db/issues/1124
                'schema.tests.SchemaTests.test_add_field_o2o_nullable',

                # ALTER TABLE name ADD [COLUMN] [IF NOT EXISTS] colname integer GENERATED ALWAYS AS IDENTITY [PRIMARY KEY] is not supported. 
                # GH Issue: https://github.com/yugabyte/yugabyte-db/issues/1124
                'schema.tests.SchemaTests.test_add_auto_field',

                # Dropping a primary key constraint is not yet supported
                # GH Issue: https://github.com/yugabyte/yugabyte-db/issues/8735
                'schema.tests.SchemaTests.test_alter_not_unique_field_to_primary_key',
                'schema.tests.SchemaTests.test_primary_key',
                
                # Alter table Add column Unique is not yet supported. 
                # GH Issue: https://github.com/yugabyte/yugabyte-db/issues/1124
                'schema.tests.SchemaTests.test_indexes',

            })


        return expected_failures
