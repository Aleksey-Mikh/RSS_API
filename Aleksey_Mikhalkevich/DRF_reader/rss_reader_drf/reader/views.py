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
            "url": "url for parse",
            "limit": "number of news",
            "pub_date": "data",
            "json": "get news in json format",
            "to-pdf": "convert to pdf",
            "to-html": "convert to html"
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GetNewsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print("---"*60, "parsing")
        return Response(serializer.data, status=status.HTTP_201_CREATED)



