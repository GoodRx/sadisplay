# -*- coding: utf-8 -*-
import uuid
import types
from sqlalchemy.orm import class_mapper
from sqlalchemy import Column, Integer, ForeignKey


def describe(classes, methods=True):
    """
    """

    objects = []
    relations = []
    inherits = []

    for cls in classes:

        mapper = class_mapper(cls)

        entry = {
            'name': mapper.class_.__name__,
            'attributes': [(col.type.__class__.__name__, col.name)
                            for col in mapper.columns],
            'methods': [],
        }

        if methods:

            suffix = '%s' % str(uuid.uuid4())

            # Create the DummyClass subclass of mapper bases
            # for detecting mapper own methods

            params = {'__tablename__': 'dummy_table_%s' % suffix}

            if mapper.inherits:
                params['__mapper_args__'] = {'polymorphic_identity':
                        mapper.inherits.class_.__tablename__}

                # Get primary key
                pk = [col for col in mapper.columns if col.primary_key]

                # ForeignKey for inherited class
                params['dummy_id_col'] = Column(pk[0].type,
                        ForeignKey(pk[0]), primary_key=True)
            else:
                params['dummy_id_col'] = Column(Integer, primary_key=True)

            DummyClass = type('Dummy%s' % suffix,
                    mapper.class_.__bases__, params)

            base_keys = DummyClass.__dict__.keys()

            # Filter mapper methods
            for name, func in mapper.class_.__dict__.iteritems():
                if name not in base_keys:
                    if isinstance(func, types.FunctionType):
                        entry['methods'].append(name)

        objects.append(entry)

        # Detect relations by ForeignKey
        for col in mapper.columns:
            for fk in col.foreign_keys:
                table = fk.column.table
                for c in classes:
                    if table == c.__table__:
                        relations.append({
                            'from': cls.__name__,
                            'by': col.name,
                            'to': c.__name__,
                        })

        if mapper.inherits:
            inherits.append({
                'child': mapper.class_.__name__,
                'parent': mapper.inherits.class_.__name__,
            })

    return objects, relations, inherits


def plantuml(desc):

    classes, relations, inherits = desc

    CLASS_TEMPLATE = "Class %(name)s {\n%(attributes)s\n%(methods)s\n}\n"

    ATTRIBUTE_TEMPLATE = "\t%(type)s \t\t%(name)s"

    METHOD_TEMPLATE = "\t%(name)s()"

    INHERIT_TEMPLATE = "%(parent)s <|-- %(child)s\n"

    result = []
    for cls in classes:
        renderd = CLASS_TEMPLATE % {
                'name': cls['name'],
                'attributes': '\n'.join([
                    ATTRIBUTE_TEMPLATE % {'type': a[0], 'name': a[1]}
                        for a in cls['attributes']
                ]),
                'methods': '\n'.join([
                    METHOD_TEMPLATE % {'name': m}
                        for m in cls['methods']
                ]),
            }

        result.append(renderd)

    for item in inherits:
        result.append(INHERIT_TEMPLATE % item)

    return '\n'.join(result)
