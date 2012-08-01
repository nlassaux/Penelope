from django import template


register = template.Library()


@register.simple_tag
def number_human(value, separator=' ', precision=2, delimeter_count=3, decimal_separator=','):
    #    Converts an integer or floating-point number or a string to a string
    #    containing the delimiter character (default comma)
    #    after every delimeter_count digits (by default 3 digits)

    f = ''
    if isinstance(value, float):
        negative = value < 0
        s = '%s.%df' % ('%', precision) % (abs(value))
        p = s.find(decimal_separator)
        if p > -1:
            f = s[p:]
            s = s[:p]
    elif isinstance(value, int):
        negative = value < 0
        s = str(abs(value))
    else:
        negative = False
        s = value
        p = s.find(decimal_separator)
        if p > -1:
            f = s[p:p + precision + 1]
            if f == decimal_separator:
                f = ''
            s = s[:p]

    groups = []
    while s:
        groups.insert(0, s[-delimeter_count:])
        s = s[:-delimeter_count]

    return '%s%s%s' % ('-' if negative else '', separator.join(groups), f)
