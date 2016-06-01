from django import template

register = template.Library()


@register.filter
def arabic_numerals(number):
    number_string = str(number)
    dic = {
        '0': u'۰',
        '1': u'١',
        '2': u'٢',
        '3': u'۳',
        '4': u'۴',
        '5': u'۵',
        '6': u'۶',
        '7': u'۷',
        '8': u'۸',
        '9': u'۹',
    }
    return ''.join([dic[digit] for digit in number_string])
