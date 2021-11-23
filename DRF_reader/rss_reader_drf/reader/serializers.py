from rest_framework import serializers

from bs4 import BeautifulSoup

from .models import News, Feed, SourceForParse


class GetNewsSerializer(serializers.Serializer):
    """Request for parsing"""
    source = serializers.URLField(max_length=200, allow_null=True)
    pub_date = serializers.CharField(max_length=200, allow_blank=True)
    limit = serializers.IntegerField(min_value=0, allow_null=True)
    json = serializers.BooleanField(default=True)
    to_pdf = serializers.BooleanField(default=False)
    to_html = serializers.BooleanField(default=False)

    def create(self, validated_data):
        """:return serializable data"""
        return validated_data


class NewsSerializer(serializers.ModelSerializer):
    """Used for NewsListView and NewsDetailView"""
    channel_title = serializers.CharField(source="channel_title.channel_title")

    class Meta:
        """Metadata options"""
        model = News
        fields = "__all__"


class FeedSerializer(serializers.ModelSerializer):
    """Used for FeedListView and FeedDetailView"""

    class Meta:
        """Metadata options"""
        model = Feed
        fields = "__all__"


class SourceForParseSerializer(serializers.ModelSerializer):
    """Used for SourceForParseListView and SourceForParseDetailView"""

    class Meta:
        """Metadata options"""
        model = SourceForParse
        fields = "__all__"


def serialization_data(data, limit, list_error_message, source):
    """
    The function that processes the data with the soup class,
    gets the channel name and dictionaries with the news content
    and forms a list of it all.

    :param data: response text
    :param limit: limit of the news
    :param list_error_message: list with error messages
    :param source: link that is used in parse print
    :return: list of the dicts which contains information about news
    """
    list_items = list()

    soup = BeautifulSoup(data, "xml")

    # finish work if get False
    if not checking_the_source_is_the_rss(soup, list_error_message, source):
        return "errors", list_error_message

    channel = get_channel_data(soup, source)
    list_items.append(channel)

    items = soup.find_all("item")
    count_news = len(items)
    limit = check_limit(limit, count_news, list_error_message)

    if not limit:
        return None

    for item in items[:limit]:
        list_items.append(serialization_item(item))

    return list_items


def get_channel_data(soup, source):
    """
    Find channel title and return it or None.
    Write link to source in dict.

    :param soup: BeautifulSoup object
    :param source: source or the feed
    :return: dict which contain channel_data
    """
    try:
        channel_title = soup.find("title").get_text(strip=True)
    except AttributeError:
        channel_title = None

    channel = {
        "channel_title": channel_title,
        "source": source
    }
    return channel


def checking_the_source_is_the_rss(soup, list_error_message, source):
    """
    Find element version in xml tree and print warning if source isn't RSS.

    :param soup: BeautifulSoup object
    :param list_error_message: list with error messages
    :param source: link that is used in parse print
    :return: True if source is RSS or False if source isn't RSS
    """
    try:
        soup.find("rss").get("version")
        return True
    except AttributeError:
        list_error_message.append(
            f"{source!r} isn't a RSS. Please try to enter a correct URL. "
            f"If your sure that this URL is correct, please check your URL,"
            f" maybe it use old rss version and parser don't understand it."
        )
        return False


def check_limit(limit, count_news, list_error_message):
    """
    Checked limit and if limit is None or limit > count_news,
    and check if limit <= 0,
    redefined limit to count_news.

    :param limit: limit of the news
    :param count_news: the number of news on the site
    :param list_error_message: list with error messages
    :return: updated limit
    """
    if limit is None or limit > count_news:
        limit = count_news
    elif limit <= 0:
        list_error_message.append(
            "The limit is less than or equal to 0, news cannot be printed."
        )
        return False

    return limit


def serialization_item(item):
    """
    Function that processes the news and gets the values of an element
    to build a dictionary that will contain information about the news.

    :param item: one news
    :return: dict which contain information about news
    """
    try:
        title = item.find("title").get_text(strip=True)
        title = BeautifulSoup(title, 'html.parser')
        title = str(title)
    except AttributeError:
        title = None

    try:
        link = item.find("link").get_text(strip=True)
    except AttributeError:
        link = None

    try:
        author = item.find("author").get_text(strip=True)
    except AttributeError:
        author = None

    try:
        description_data = item.find("description").get_text(strip=True)
        soup = BeautifulSoup(description_data, 'html.parser')
        description = soup.get_text()
    except AttributeError:
        description = None

    try:
        content_encoded = item.find("content:encoded").get_text(strip=True)
        soup = BeautifulSoup(content_encoded, 'html.parser')
        content_encoded = soup.get_text()
    except AttributeError:
        content_encoded = None

    try:
        list_categories = []
        categories = item.find_all("category")

        for category in categories:
            category_content = category.get_text(strip=True)
            list_categories.append(category_content)

    except AttributeError:
        list_categories = None

    try:
        comments = item.find("comments").get_text(strip=True)
    except AttributeError:
        comments = None

    try:
        enclosure = item.find("enclosure").get("url")
    except AttributeError:
        enclosure = None

    try:
        images_list = []

        description_data = item.find("description").get_text(strip=True)
        soup = BeautifulSoup(description_data, 'html.parser')
        images = soup.find_all('img')

        for img in images:
            images_list.append(img.get("src"))

    except AttributeError:
        images_list = None

    try:
        guid = item.find("guid").get_text(strip=True)
    except AttributeError:
        guid = None

    try:
        pub_date = item.find("pubDate").get_text(strip=True)
    except AttributeError:
        pub_date = None

    try:
        source_content = item.find("source").get_text(strip=True)
    except AttributeError:
        source_content = None

    try:
        source_url = item.find("source").get("url")
    except AttributeError:
        source_url = ""

    # if description text in rss equals content_encoded
    # text - getting rid of duplicates
    if description == content_encoded:
        content_encoded = None

    # check media objects
    if images_list and enclosure:
        enclosure = images_list.append(enclosure)
    elif images_list:
        enclosure = images_list

    # check source
    if source_url and source_content:
        list_source = [source_content, source_url]
    elif source_url:
        list_source = source_url
    else:
        list_source = source_content

    item_dict = {
        "title": title,
        "pub_date": pub_date,
        "link": link,
        "author": author,
        "category": list_categories,
        "description": description,
        "more_description": content_encoded,
        "comments": comments,
        "media_objects": enclosure,
        "extra_links": guid,
        "source_feed": list_source,
    }

    return item_dict
