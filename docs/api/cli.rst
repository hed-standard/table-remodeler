Command-Line Interface
======================

Command-line tools for executing remodeling workflows.

run_remodel
-----------

Main command for executing remodeling operations on datasets.

.. code-block:: bash

   run_remodel data_dir model_path [options]

**Usage Example:**

.. code-block:: bash

   run_remodel /path/to/dataset operations.json --verbose

**Module Reference:**

.. automodule:: remodel.cli.run_remodel
   :members: main, parse_arguments
   :undoc-members:

run_remodel_backup
------------------

Command for creating backups of datasets before remodeling.

.. code-block:: bash

   run_remodel_backup data_dir [options]

**Usage Example:**

.. code-block:: bash

   run_remodel_backup /path/to/dataset --backup-name my_backup

**Module Reference:**

.. automodule:: remodel.cli.run_remodel_backup
   :members: main, parse_arguments
   :undoc-members:

run_remodel_restore
-------------------

Command for restoring datasets from backups.

.. code-block:: bash

   run_remodel_restore data_dir [options]

**Usage Example:**

.. code-block:: bash

   run_remodel_restore /path/to/dataset --backup-name my_backup

**Module Reference:**

.. automodule:: remodel.cli.run_remodel_restore
   :members: main, parse_arguments
   :undoc-members:

Common Options
--------------

All CLI commands share some common options:

* ``-v, --verbose``: Output detailed progress information
* ``-bn, --backup-name``: Name of the backup to use
* ``-bd, --backup-dir``: Directory for backup storage
* ``-t, --task-names``: Specify task names to process
* ``-x, --exclude-dirs``: Directories to exclude from processing

For complete option lists, use ``--help`` with any command:

.. code-block:: bash

   run_remodel --help
   run_remodel_backup --help
   run_remodel_restore --help
