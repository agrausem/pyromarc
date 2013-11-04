========
Pyromarc
========

.. image:: https://secure.travis-ci.org/agrausem/pyromarc.png?branch=master
    :target: https://travis-ci.org/agrausem/pyromarc

.. image:: https://coveralls.io/repos/agrausem/pyromarc/badge.png?branch=master
    :target: https://coveralls.io/r/agrausem/pyromarc?branch=master

MARC::MIR est une spécification de représentation mémoire (sous la forme de
tableau de tableaux) de données bibliographiques cataloguée en MARC. elle
permet d'établir des ponts simples entre les différents outils exitants de
traitement, sérialisation, indexation, ...

https://github.com/eiro/p5-marc-mir
https://github.com/eiro/p5-marc-mir-template
https://metacpan.org/module/MARCC/marc-mir-0.4/lib/MARC/MIR.pod

Pyromarc se veut être une implementation python du pendant Perl. Objectifs du
sprint de la pycon 2013:

* serialisation/désérialisation ISO2709
* implementation d'un DSL pythonic permettant de manipuler les enregistrements
  avec la même simplicité que l'implémentation Perl
* implementation de MARC::MIR::Template
* serialisation/désérialisation msgpack
