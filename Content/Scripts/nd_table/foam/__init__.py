"""
foam3_py — a Python port of FOAM3's Java file-type conversion code
(foam.lib.parse, foam.lib.json, foam.lib.csv, foam.lib.xml, foam.lib.html,
foam.lib.formatter).

Subpackages mirror the Java layout one-to-one:

    foam3_py.parse       parser combinator framework
    foam3_py.json        JSON parsers + outputters
    foam3_py.csv         CSV parsers + outputter
    foam3_py.xml         XML outputter
    foam3_py.html        HTML outputter
    foam3_py.formatter   FObject formatter base + JSONFObjectFormatter

The port is faithful to the Java semantics — same class names, same parse
contracts, same outputter behaviour. Java's FObject/PropertyInfo concept maps
to plain Python objects (dataclasses, classes with ``__dict__``, dicts) — see
``formatter.FObject`` for the duck-typing rules.

Quick start:

    from foam3_py.json import loads, dumps
    obj = loads('{"name":"foo","count":3}')   # -> {'name': 'foo', 'count': 3}
    print(dumps(obj))                          # -> {"name":"foo","count":3}
"""

__version__ = "0.1.0"
