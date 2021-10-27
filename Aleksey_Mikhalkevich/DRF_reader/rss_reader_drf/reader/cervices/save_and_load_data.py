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


def interface_from_save(data, to_pdf, to_html, error_message):
    channel_data, news = data[0], data[1:]
    obj, created = Feed.objects.get_or_create(**channel_data)

    for one_news in news:
        one_news = one_news | {"channel_title": obj}
        date = get_date_in_correct_format(one_news["pub_date"])

        if date is not None:
            one_news["pub_date"] = date
            News.objects.get_or_create(**one_news)
        else:
            error_message.append(
                f"The site {obj.source} uses an unsupported"
                f" date format. Storage data has failed."
            )
            return "errors", error_message


def interface_from_load(date, source, limit, to_pdf, to_html, error_message):
    date = get_date_in_correct_format(date)
    if date is None:
        error_message.append(
            f"{date!r} is an incorrect date. "
            f"Please try to enter the date in a correct format"
        )
        return "errors", error_message

    if date and source is None:
        news = News.objects.filter(pub_date=date)
        return news[:limit]
    else:
        news = News.objects.filter(pub_date=date, channel_title__source=source)
        return news[:limit]


