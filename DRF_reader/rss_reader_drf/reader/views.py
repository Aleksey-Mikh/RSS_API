from pathlib import Path

from django.http.response import HttpResponse
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GetNewsSerializer, FeedSerializer, NewsSerializer
from .cervices.rss_parser import rss_parser_interface
from .models import Feed, News


class GetNewsView(APIView):
    """
    Class which has two methods: GET and POST,
    and implement parsing script if method is POST.
    """

    def get(self, request):
        """
        When the user make get request he received
        help information about:
        `how to make a request for parse news`
        """
        data = {
            "source": "Url for parse. May be null",
            "pub_date": "Publication date in format YearMonthDay: 20211023. May be blank",
            "limit": "Number of news. May be null",
            "json": "Get news in JSON format. Default value true",
            "to-pdf": "Convert received news to PDF. Default value false",
            "to-html": "Convert received news to HTML. Default value false"
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Implemented parsing script.
        If the user has set the value to_pdf=True or to_html=True,
        loads the conversion to the selected format
        """
        serializer = GetNewsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            result = rss_parser_interface(serializer.data)

            if serializer.data["to_pdf"]:
                path = Path(Path(__file__).parent, "media", "feed.pdf")
                with open(path, "rb") as file:
                    response = HttpResponse(file, content_type='application/pdf', status=status.HTTP_201_CREATED)
                    filename = "feed.pdf"
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    return response

            if serializer.data["to_html"]:
                path = Path(Path(__file__).parent, "media", "feed.html")
                with open(path, "r", encoding="utf-8") as file:
                    response = HttpResponse(file, content_type='application/html', status=status.HTTP_201_CREATED)
                    filename = "feed.html"
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    return response

            if result is None:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
        return Response(result, status=status.HTTP_201_CREATED)


class DownloadPdfView(APIView):
    """Implemented extra download PDF file"""

    def get(self, request):
        path = Path(Path(__file__).parent, "media", "feed.pdf")
        with open(path, "rb") as file:
            response = HttpResponse(file, content_type='application/pdf', status=status.HTTP_201_CREATED)
            filename = "feed.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response


class DownloadHTMLView(APIView):
    """Implemented extra download HTML file"""

    def get(self, request):
        path = Path(Path(__file__).parent, "media", "feed.html")
        with open(path, "r", encoding="utf-8") as file:
            response = HttpResponse(file, content_type='application/html', status=status.HTTP_201_CREATED)
            filename = "feed.html"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response


class FeedListView(generics.ListCreateAPIView):
    """
    Used for read-write endpoints to represent
    a collection of model instances.
    Provides get and post method handlers.
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class FeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Used for read-write-delete endpoints
    to represent a single model instance.
    Provides get, put, patch and delete method handlers.
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class NewsListView(generics.ListCreateAPIView):
    """
    Used for read-write endpoints to represent
    a collection of model instances.
    Provides get and post method handlers.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Used for read-write-delete endpoints
    to represent a single model instance.
    Provides get, put, patch and delete method handlers.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
