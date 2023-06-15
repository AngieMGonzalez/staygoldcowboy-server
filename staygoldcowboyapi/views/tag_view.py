"""View module for handling requests about Tags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from staygoldcowboyapi.models import Tag


class TagView(ViewSet):
    """SGC Tag view"""

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized tag instance
        """

        new_tag = Tag.objects.create(
            medium=request.data["medium"]
        )
        serializer = TagSerializer(new_tag)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized tag
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get All Tags

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Handle PUT requests for a tag - replaces entire object
        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.medium = request.data["medium"]
            tag.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist:
            return Response("Oops, 404 Tag not found", status=status.HTTP_404_NOT_FOUND)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags
    """
    class Meta:
        model = Tag
        fields = (
            'id', 
            'medium'
            )
