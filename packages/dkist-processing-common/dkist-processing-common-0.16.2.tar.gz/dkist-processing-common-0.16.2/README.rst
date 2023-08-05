dkist-processing-common
=======================

This repository works in concert with `dkist-processing-core <https://pypi.org/project/dkist-processing-core/>`_ and `dkist-processing-*instrument*` to
form the DKIST calibration processing stack.

Usage
-----

The classes in this repository should be used as the base of any DKIST processing pipeline tasks. Science tasks should subclass `ScienceTaskL0ToL1Base`.

Each class is built on an abstract base class with the `run` method left for a developer to fill out with the required steps that the task should take.
This class is then used as the callable object for the workflow and scheduling engine.

Example
-------
.. code-block:: python

    from dkist_processing_common.tasks.base import ScienceTaskL0ToL1Base


    class RemoveArtifacts(ScienceTaskL0ToL1Base):
        def run(self):
            # task code here
            total = 2 + 5

Deployment
----------
dkist-processing-common is deployed to `PyPI <https://pypi.org/project/dkist-processing-common/>`_

Development
-----------
.. code-block:: bash

    git clone git@bitbucket.org:dkistdc/dkist-processing-common.git
    cd dkist-processing-common
    pre-commit install
    pip install -e .[test]
    pytest -v --cov dkist_processing_common
