import requests

from ..serializers import serialization_data

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/94.0.4606.61 Safari/537.36",
    "accept": "*/*",
    "Content-Type": "charset=UTF-8"
}


class RSSParser:
    """
    Class that regulates the parsing relationship between
    the user and the site that program are trying to parse.
    """

    def __init__(self, **kwargs):
        """
        Init class and init argparse
        """
        self.source = kwargs["source"]
        self.limit = kwargs["limit"]
        self.json = kwargs["json"]
        self.date = kwargs["pub_date"]
        self.to_html = kwargs["to_html"]
        self.to_pdf = kwargs["to_pdf"]
        self.serializable_data = None
        self.error_message = []

    def parsing(self):
        """
        Gets the response object and checks that it isvalid
        and call serialization_data to get serializable_data
        """
        response = self._get_html()

        if self._isvalid(response):
            serializable_data = serialization_data(
                response.text, self.limit, self.error_message, self.source
            )

            if isinstance(serializable_data, tuple):
                self.error_message.append("Data wasn't received")
                return "errors", self.error_message

            self.serializable_data = serializable_data
        else:
            return "errors", self.error_message

    def _isvalid(self, response):
        """Check if response is valid"""
        if response is None:
            self.error_message.append(
                f"The program stop running with error, when it "
                f"try to get information from {self.source!r}"
            )
            return None

        elif response.status_code == 200:
            return True
        else:
            self._check_error_status_code(response.status_code)

    def check_date_and_source(self):
        """
        Check date and source value and allowed standard start if
        source was enter and date is None, if source is None
        print error, if date was enter call storage_control.

        :return: True if source is enter and date is None
        """
        print(f"{self.date=}, {self.source=}")
        if not self.date and self.source is not None:
            print("-" * 20, "if self.date and self.source is not None", "-" * 20)
            return True
        elif self.date:
            print("-" * 20, "elif self.date is not None:", "-" * 20)
            # storage_control(
            #     date=self.date, source=self.source, verbose=self.verbose,
            #     json=self.json, limit=self.limit, to_html=self.to_html,
            #     to_pdf=self.to_pdf, colorize=self.colorize
            # )
        elif self.source is None:
            self.error_message.append(f"A source wasn't enter. Source is {self.source}")

    def save_data_in_db(self):
        """
        Check the self.json value and
        if self.json is True - outputs json to the console
        if self.json is False - outputs news
        in a standard format to the console
        """
        if self.serializable_data is None:
            return None

        # storage_control(
        #     data=self.serializable_data, source=self.source,
        #     verbose=self.verbose, to_html=self.to_html,
        #     to_pdf=self.to_pdf, colorize=self.colorize
        # )

    def _get_html(self):
        """
        Executes a get request at the url specified by the user
        and check encoding of response data.

        :return response obj
        """
        response = requests.get(self.source, headers=HEADERS)

        # if site gives invalid encoding this line trying to correct it
        response.encoding = response.apparent_encoding
        return response

    def _check_error_status_code(self, status_code):
        """
        Check status code and print error message.

        :param status_code: http status code
        """
        if 400 <= status_code <= 499:
            if status_code == 404:
                self.error_message.append(f"{self.source!r}: 404 Page Not Found")
            else:
                self.error_message.append(
                    "Error seems to have been caused "
                    "by the client. Check url which you give."
                )
        elif 500 <= status_code <= 599:
            self.error_message.append("The server failed to execute a request")
        else:
            self.error_message.append(
                "Error which can't be processed because "
                "status code don't defined"
            )


def start_parsing(reader):
    """Load parsing and print data"""
    if reader.check_date_and_source():
        result = reader.parsing()
        if isinstance(result, tuple):
            return result[1]
        reader.save_data_in_db()

        return reader.serializable_data


def rss_parser_interface(data):
    """Init reader"""
    reader = RSSParser(
        source=data["source"],
        limit=data["limit"],
        json=data["json"],
        pub_date=data["pub_date"],
        to_html=data["to_html"],
        to_pdf=data["to_pdf"],
    )
    return start_parsing(reader)
