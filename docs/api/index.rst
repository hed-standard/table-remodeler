API reference
=============

This section contains the complete API reference for Table Remodeler.

.. toctree::
   :maxdepth: 2

   core
   operations
   cli

Package overview
----------------

The table-remodeler package is organized into three main modules:

* **Core**: Main dispatcher, backup manager, and validator classes
* **Operations**: All remodeling and summary operations for tabular data
* **CLI**: Command-line interface tools for remodeling workflows

Quick start
-----------

The primary entry point for programmatic use is the :class:`~remodeler.dispatcher.Dispatcher` class:

.. code-block:: python

   from remodeler import Dispatcher
   
   operations = [
       {"operation": "remove_columns", 
        "parameters": {"column_names": ["col1"]}}
   ]
   
   dispatcher = Dispatcher(operations, data_root="/path/to/data")
   dispatcher.run_operations()
