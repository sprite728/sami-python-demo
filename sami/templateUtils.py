from django.template.defaulttags import register
import datetime

@register.filter
def get_item(dictionary, key):
    """Helper function to retrieve a value from a dictionary on a django template

                Args:
                    dictionary: python dictionary
                    key: key of the element to be retrieved
                Returns: value associated with the key
                """
    value = dictionary.get(key)
    if (value != None):
        return value
    else:
        return '---'

@register.filter
def get_date(timestamp):
    """convert unix timestamp to date

                Args:
                    timestamp: timestamp
                Returns: formatted date
                """
    #samsung server returns timestamps with the last 3 digits corresponding to miliseconds, so we remove those to do the conversion
    timestamp = timestamp/1000
    return datetime.datetime.fromtimestamp(timestamp).strftime('%b %d, %Y %H:%M')
