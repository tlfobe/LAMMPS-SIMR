===========
LAMMPS-SIMR
===========


.. image:: https://img.shields.io/pypi/v/lammps_simr.svg
        :target: https://pypi.python.org/pypi/lammps_simr

.. image:: https://img.shields.io/travis/tlfobe/lammps_simr.svg
        :target: https://travis-ci.org/tlfobe/lammps_simr

.. image:: https://readthedocs.org/projects/lammps-simr/badge/?version=latest
        :target: https://lammps-simr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




This repo contains an implementation of the SIMR technique using LAMMPS simulation package

We primarily use signac, a python package, to streamline the naming and naviagation of the dataspace.

Scripts include:

1. init.py : creates signac workspace with needed files to run LAMMPS simulations

2. project.py : contains several operations which run and analyze each LAMMPS simulation. Using python project.py status, one can check on the status of each simulation

3. mapping.py : (WIP) uses signac framework to implement SIMR technique.

This repo is currently set up to simulate Bi2O3 systems.

* Free software: MIT license
* Documentation: https://lammps-simr.readthedocs.io.


Features
--------

* TODO
Finishing `mapping.py` script
Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
