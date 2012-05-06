# -*- coding: utf-8 -*-
from sadisplay import __version__


def plantuml(desc):
    """Generate plantuml class diagram

    :param desc: result of sadisplay.describe function

    Return plantuml class diagram string
    """

    classes, relations, inherits = desc

    CLASS_TEMPLATE = "Class %(name)s {\n%(cols)s\n%(props)s\n%(methods)s\n}\n"

    COLUMN_TEMPLATE = "\t%(name)s \t\t%(type)s"

    PROPERTY_TEMPLATE = "\t+\t\t%(name)s"

    METHOD_TEMPLATE = "\t%(name)s()"

    INHERIT_TEMPLATE = "%(parent)s <|-- %(child)s\n"

    RELATION_TEMPLATE = "%(from)s <--o %(to)s: %(by)s\n"

    result = ['@startuml']

    for cls in classes:
        renderd = CLASS_TEMPLATE % {
                'name': cls['name'],
                'cols': '\n'.join([
                    COLUMN_TEMPLATE % {'type': c[0], 'name': c[1]}
                        for c in cls['cols']
                ]),
                'props': '\n'.join([
                    PROPERTY_TEMPLATE % {'name': p}
                        for p in cls['props']
                ]),
                'methods': '\n'.join([
                    METHOD_TEMPLATE % {'name': m}
                        for m in cls['methods']
                ]),
            }

        result.append(renderd)

    for item in inherits:
        result.append(INHERIT_TEMPLATE % item)

    for item in relations:
        result.append(RELATION_TEMPLATE % item)

    result += [
        'right footer generated by sadisplay v%s' % __version__,
        '@enduml',
    ]

    return '\n'.join(result)


def dot(desc):
    """Generate dot file

    :param desc: result of sadisplay.describe function

    Return string
    """

    classes, relations, inherits = desc

    CLASS_TEMPLATE = """
        %(name)s [label=<
        <TABLE BGCOLOR="lightyellow" BORDER="0"
            CELLBORDER="0" CELLSPACING="0">
                <TR><TD COLSPAN="2" CELLPADDING="4"
                        ALIGN="CENTER" BGCOLOR="palegoldenrod"
                ><FONT FACE="Helvetica Bold" COLOR="black"
                >%(name)s</FONT></TD></TR>%(cols)s%(props)s%(methods)s
        </TABLE>
    >]
    """

    COLUMN_TEMPLATE = """<TR><TD ALIGN="LEFT" BORDER="0"
        ><FONT FACE="Bitstream Vera Sans">%(name)s</FONT
        ></TD><TD ALIGN="LEFT"
        ><FONT FACE="Bitstream Vera Sans">%(type)s</FONT
        ></TD></TR>"""

    PROPERTY_TEMPLATE = """<TR><TD ALIGN="LEFT" BORDER="0"
        BGCOLOR="palegoldenrod"
        ><FONT FACE="Bitstream Vera Sans">%(name)s</FONT></TD
        ><TD BGCOLOR="palegoldenrod" ALIGN="LEFT"
        ><FONT FACE="Bitstream Vera Sans">PROPERTY</FONT
        ></TD></TR>"""

    METHOD_TEMPLATE = """<TR><TD ALIGN="LEFT" BORDER="0"
        BGCOLOR="palegoldenrod"
        ><FONT FACE="Bitstream Vera Sans">%(name)s()</FONT></TD
        ><TD BGCOLOR="palegoldenrod" ALIGN="LEFT"
        ><FONT FACE="Bitstream Vera Sans">METHOD</FONT
        ></TD></TR>"""

    EDGE_INHERIT = "\tedge [\n\t\tarrowhead = empty\n\t]"
    INHERIT_TEMPLATE = "\t%(child)s -> %(parent)s \n"

    EDGE_REL = "\tedge [\n\t\tarrowhead = ediamond\n\t\tarrowtail = open\n\t]"
    RELATION_TEMPLATE = "\t%(from)s -> %(to)s [label = \"%(by)s\"]"

    result = ["""
        digraph G {
            label = "generated by sadisplay v%s";
            fontname = "Bitstream Vera Sans"
            fontsize = 8

            node [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
                shape = "plaintext"
            ]

            edge [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
            ]
    """ % __version__]

    for cls in classes:
        renderd = CLASS_TEMPLATE % {
                'name': cls['name'],
                'cols': ' '.join([
                    COLUMN_TEMPLATE % {'type': c[0], 'name': c[1]}
                        for c in cls['cols']
                ]),
                'props': ' '.join([
                    PROPERTY_TEMPLATE % {'name': p}
                        for p in cls['props']
                ]),
                'methods': ' '.join([
                    METHOD_TEMPLATE % {'name': m}
                        for m in cls['methods']
                ]),
            }

        result.append(renderd)

    result += [EDGE_INHERIT]
    for item in inherits:
        result.append(INHERIT_TEMPLATE % item)

    result += [EDGE_REL]
    for item in relations:
        result.append(RELATION_TEMPLATE % item)

    result += [
        '}'
    ]

    return '\n'.join(result)
