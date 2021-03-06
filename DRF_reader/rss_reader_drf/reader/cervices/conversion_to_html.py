from pathlib import Path

from jinja2 import Environment, select_autoescape, FileSystemLoader

FILE_NAME_HTML = "feed.html"

def make_dir(path):
    """
    Creating a folder at the got path.
    If the folder already exists does nothing.

    :param path: the path where the folder should be created
    """
    if not Path(path).exists():
        p = Path(path)
        p.mkdir(parents=True)


def is_list(obj):
    """
    Check obj is list.

    :param obj: object
    :return: True or False
    """
    return isinstance(obj, list)


def get_env():
    """
    Init Environment for jinja2
    :return: env
    """
    path = Path(__file__).parent
    path = Path(path, "templates")
    env = Environment(
        loader=FileSystemLoader(path),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def get_content(data, env):
    """
    Creating a dictionary with content and a
    dictionary with tests for env.

    :param data: news
    :param env: env
    :return: content
    """
    if not is_list(data[0]):
        data = [data]
    content = {
        "title": "Feeds",
        "feeds": data
    }
    env.tests["is_list"] = is_list
    return content


def convert_to_html(data, path, error_message):
    """
    Еhe function gets a list of dictionaries with
    news, a path, and a verbose flag.
    Initializes the Environment of jinja2, gets the HTML template,
    runs the render, and saves the file to the received path.

    :param data: a list of dictionaries with news
    :param path: the path to save the file
    :param verbose: verbose mode
    """

    env = get_env()
    content = get_content(data, env)
    template = env.get_template("template.html")
    result = template.render(content)
    path = Path(path)
    try:
        make_dir(path)
        with open(Path(path, FILE_NAME_HTML), "w", encoding="utf-8") as file:
            file.write(result)
    except Exception:
        error_print("Failed to create file")
