Interested in contributing?
---------------------------

Submitted code must adhere to the `black`_ style format. The documentation should follow the `numpy docstring guidelines`_. To pass the formatting tests, you can use the `black package`_ and `isort package`_ in the following manner before submitting. 

.. code-block:: bash

   import black
   import isort
   
   black {source_file_or_directory}
   isort {source_file}

.. _`black`: https://black.readthedocs.io/en/stable/the_black_code_style/index.html
.. _`numpy docstring guidelines`: https://numpydoc.readthedocs.io/en/latest/format.html
.. _`black package`: https://pypi.org/project/black/
.. _`isort package`: https://pypi.org/project/isort/
