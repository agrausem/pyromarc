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

Install
=======

Pyromarc is only working under *Python 3.2* for the moment. To install the module, use pip :: 

    $> pip install pyromarc


Reading
=======

ISO2709
-------

Load MIRs from ISO2709 ::

    from pyromarc import reader

    mirs = reader('/path/to/records.iso2709', 'ISO2709')
    for mir in mirs:
        do_something_with(mir)

Or, with a filehandler ::

    from pyromarc import readerb

    with open('/path/to/records/example.iso2709', 'rb') as filehandler:
        mirs = readerb(filehandler, 'ISO2709')
        for mir in mirs:
            do_something_with(mir)


Msgpack
-------

Load MIRs from stdin ::

    import sys
    from pyromarc import readerb

    mirs = readerb(sys.stdin, 'MsgPack')
    for mir in mirs:
        do_something_with(mir)


Writing
=======

ISO2709
-------

Write MIRs in file ::

    from pyromarc import writer

    [...]
    writer('/path/to/records.iso2709', mirs, 'ISO2709')

Writing ISO2709 records in JSON ::

    from pyromarc import reader, writer

    mirs = reader('/path/to/records.iso2709', 'ISO2709')
    writer('/path/to/records.json', mirs, 'Json')


MsgPack
-------

Writing on stdout ::

    import sys
    from pyromarc import writerb

    [...]
    writerb(sys.stdout, mirs, 'MsgPack')
