Project description 
===
Web-server that uses Docker + docker-compose. 
Implementing all parts of the task using the REST API:
* One-shot conversion from RSS to Human readable format
* Server-side news caching
* Conversion in epub, mobi, fb2 or other formats

---

## Contents
***
1. [Installation](#Installation)
2. [Usage](#Usage)
3. [Format converter](#Format-converter)
    * [Converter to PDF](#Converter-to-PDF)
    * [Converter to HTML](#Converter-to-HTML)
4. [What's in the future](#What's-in-the-future)

---

## Installation
To install, you need to make a clone of the repository:
```
>>> git clone https://github.com/Aleksey-Mikh/Homework.git -b master
```
After that, you need to go to the CLI_util directory:
```
>>> cd your_path/CLI_util/
```
Then you need to build the docker container:
```
>>> docker-compose up -d --build
```
And start creating databases:
```
>>> docker-compose exec drf_reader python manage.py migrate
```

---

## Usage

We can use http://127.0.0.1:8000/api or http://0.0.0.0:8000/api

Для получение новостей нужно отпрвить POST запрос на адрес http://127.0.0.1:8000/api/get_news/

      {
         "source": "https://people.onliner.by/feed",
         "pub_date": "",
         "limit": 1,
         "json": true,
         "to_pdf": true,
         "to_html": false
      }

![](gif/post.gif.mp4)