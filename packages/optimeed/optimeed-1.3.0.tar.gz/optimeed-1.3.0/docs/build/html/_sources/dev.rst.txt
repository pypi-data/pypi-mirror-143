Developer documentation
=======================

To regenerate API:
------------------
* uncomment line     # 'autoapi.extension'  in conf.py.
* run make html
* run hack.py script
* recomment line     # 'autoapi.extension'
* run make html
* Eventually update project on https://readthedocs.org/projects/optimeed/

To updata packages on PyPi:
---------------------------

* Change version in setup.py and in optimeed/__init__.py
* Create new wheel file code::`python setup.py sdist bdist_wheel`
* Upload it on pypi code::`twine upload dist/*`
