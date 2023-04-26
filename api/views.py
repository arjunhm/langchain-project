from django.shortcuts import render
from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status

from api.models import Post
from api.serializer import PostSerializer

from utils import linkedin_api
from utils.langchain_api import LinkedInPostGenerator

# Create your views here.


class LinkedInPostAPI(views.APIView):
    permission_classes = []  # permissions.IsAuthenticated
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        post_id = request.GET.get("post_id")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(post)
        return Response({"post": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        topic = request.data.get("topic")
        llm = LinkedInPostGenerator()

        image_url = llm.generate_image(topic)
        text_response = llm.generate_text(topic)

        post = Post.objects.create(
            topic=topic, content=text_response, image_url=image_url
        )

        # * Create LinkedInPost
        linkedin_response = linkedin_api.create_linkedin_post(post)

        serializer = self.serializer_class(post)
        return Response(
            {"post": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        post_id = request.GET.get("post_id")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        post.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
