import base64
import mimetypes
from pathlib import Path

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework.generics import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GetNewsSerializer, FeedSerializer, NewsSerializer
from .cervices.rss_parser import rss_parser_interface
from .models import Feed, News


class GetNewsView(APIView):
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
        path = Path(Path(__file__).parent, "media", "feed.pdf")
        # with open(path, "rb") as file:
        #     mime_type, _ = mimetypes.guess_type(path)
        #     response = HttpResponse(file, content_type='application/pdf')
        #     filename = "feed.pdf"
        #     response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        #         filename)
        #     print("LOL")
        #     return response
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GetNewsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            result = rss_parser_interface(serializer.data)

            if serializer.data["to_pdf"]:
                print("lol")
                path = Path(Path(__file__).parent, "media", "feed.pdf")
                with open(path, "rb") as file:
                    mime_type, _ = mimetypes.guess_type(path)
                    response = HttpResponse(file, content_type='application/pdf', status=status.HTTP_201_CREATED)
                    filename = "feed.pdf"
                    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                        filename)
                    response["Content-Type"] = 'application/pdf'
                    print("LOL")
                    print(response)
                    return redirect("news:download_pdf")

            if result is None:
                return Response(result, status=status.HTTP_204_NO_CONTENT)
        return Response(result, status=status.HTTP_201_CREATED)


class DownloadPdfView(APIView):

    def get(self, request):
        print("lol")
        path = Path(Path(__file__).parent, "media", "feed.pdf")
        with open(path, "rb") as file:
            mime_type, _ = mimetypes.guess_type(path)
            response = HttpResponse(file, content_type='application/pdf')
            filename = "feed.pdf"
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                filename)
            response["Content-Type"] = 'application/pdf'
            print("LOL")
            print(response)
            return response




class FeedListView(generics.ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class FeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class NewsListView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

