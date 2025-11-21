Core Components
===============

Core classes for managing remodeling operations, backups, and validation.

Dispatcher
----------

The main orchestrator for executing remodeling operations.

.. autoclass:: remodel.dispatcher.Dispatcher
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Key Methods

   .. automethod:: run_operations
   .. automethod:: parse_operations
   .. automethod:: get_data_file_names

BackupManager
-------------

Manages dataset backups before and during remodeling operations.

.. autoclass:: remodel.backup_manager.BackupManager
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Key Methods

   .. automethod:: create_backup
   .. automethod:: restore_backup
   .. automethod:: get_backup

RemodelerValidator
------------------

Validates remodeling operation specifications against JSON schema.

.. autoclass:: remodel.remodeler_validator.RemodelerValidator
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Key Methods

   .. automethod:: validate
