import datetime
from pathlib import Path

from django.db.models import Q

from ..models import News, Feed
from ..serializers import NewsSerializer, FeedSerializer
from .conversion_to_pdf import convertor_to_pdf
from .conversion_to_html import convert_to_html


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

    if to_pdf:
        path = Path(Path(__file__).parent.parent, "media")
        convertor_to_pdf(data, path, error_message)

    if to_html:
        path = Path(Path(__file__).parent.parent, "media")
        convert_to_html(data, path, error_message)


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
        if news:
            data = news[:limit]
            data = get_full_data_if_enter_date(data)
        else:
            error_message.append(f"No news was found for this date - {date}")
            return "errors", error_message
    else:
        news = News.objects.filter(Q(pub_date=date) & Q(channel_title__source=source))
        if news:
            data = news[:limit]
            data = get_full_data_if_enter_date_and_source(data, source)
        else:
            error_message.append(
                f"No news was found for this date - {date}, and this source - {source}"
            )
            return "errors", error_message

    if to_pdf:
        path = Path(Path(__file__).parent.parent, "media")
        convertor_to_pdf(data, path, error_message)

    if to_html:
        path = Path(Path(__file__).parent.parent, "media")
        convert_to_html(data, path, error_message)

    return data


def get_full_data_if_enter_date_and_source(data, source):
    channel_data = Feed.objects.filter(source=source)
    channel_data = FeedSerializer(channel_data, many=True)
    data = NewsSerializer(data, many=True)
    return channel_data.data + data.data


def get_full_data_if_enter_date(data):
    list_of_source = set()
    new_data = []
    for news in data:
        list_of_source.add(news.channel_title)
    for source in list_of_source:
        channel_data = Feed.objects.filter(source=source.source)
        channel_data = FeedSerializer(channel_data, many=True)
        temp_data = list(
            filter(lambda x: x.channel_title.channel_title == channel_data.data[0]["channel_title"], data)
        )
        temp_data = NewsSerializer(temp_data, many=True)
        new_data += [channel_data.data + temp_data.data]

    return new_data
