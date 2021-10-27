from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GetNewsSerializer


class GetNews(APIView):
    def get(self, request):
        """
        When the user make get request he received
        help information about:
        `how to make a request for parse news`
        """
        data = {
            "url": "Url for parse. May be null",
            "pub_date": "Publication date in format YearMonthDay: 20211023. May be blank",
            "limit": "Number of news. May be null",
            "json": "Get news in JSON format. Default value true",
            "to-pdf": "Convert received news to PDF. Default value false",
            "to-html": "Convert received news to HTML. Default value false"
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GetNewsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



