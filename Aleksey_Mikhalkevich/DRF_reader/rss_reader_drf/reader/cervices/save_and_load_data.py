import datetime

from ..models import News, Feed


LIST_OF_DATE_FORMATS = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y%m%d",
            "%Y-%m-%dT%H:%M:%SZ",
        ]


def get_date_in_correct_format(date_str):
    """
    The method gets a string containing the date and
    converts it according to known formats.
    If the conversion failed returns None.

    :param date_str: a string containing the date
    :return: a date in format %Y-%m-%d or None
    """
    for date_format in LIST_OF_DATE_FORMATS:
        try:
            date_time_obj = datetime.datetime.strptime(
                date_str, date_format
            )
            return date_time_obj.date()
        except ValueError:
            # if the correct format wasn't received,
            # proceed to the next format in LIST_OF_DATE_FORMATS
            pass

    return None


def interface_from_save(data):
    channel_data, news = data[0], data[1:]
    obj, created = Feed.objects.get_or_create(**channel_data)
    for one_news in news:
        one_news = one_news | {"channel_title": obj}
        print(one_news)
        one_news["pub_date"] = get_date_in_correct_format(one_news["pub_date"])
        print(one_news)
        News.objects.get_or_create(**one_news)


def interface_from_load():
    pass
