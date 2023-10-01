from django.shortcuts import render
from rest_framework import viewsets,parsers
from rest_framework.views import APIView
from rest_framework.response import Response 
import boto3 
from botocore.exceptions import NoCredentialsError
from rest_framework import status
from .models import ScreenVideo
from .serializers import ScreenVideoSerializer
from rest_framework import generics
from django.conf import settings
import json
import boto3
from django.conf import settings
from django.http import JsonResponse
from django.views import generic


from rest_framework.parsers import MultiPartParser ,FileUploadParser
# Create your views here.

from screenrecords.settings import AWS_STORAGE_BUCKET_NAME

s3 = boto3.client('s3')

"""class ScreenUploadVideoView(APIView):
    queryset= ScreenVideo.objects.all()
    serializer_class= ScreenVideoSerializer
    
    def create(self,request):
        serializer=ScreenVideoSerializer(data=request.data)

        if serializer.is_valid():
            video_title=serializer.validated_data['title']
            video_file=serializer.validated_data['video_file']

            s3=boto3.client('s3')

            try:
                s3.upload_fileobj(
                    video_file,
                    AWS_STORAGE_BUCKET_NAME,
                    f'videos/{video_title}/{video_file.name}'
                )
                return Response({'message':"video uploaded"})
            except NoCredentialsError:
                return Response({"message":"aws credentials not found"})    

        else:
            return Response(serializers.errors, status=400)     
            """
      

"""class ScreenVideoViewSet(viewsets.ViewSet):
    queryset= ScreenVideo.objects.all()
    serializer_class= ScreenVideoSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        video_file = request.data.get('video')
        if not video_file:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Video object and save it to the database
        video = Video.objects.create(title=request.data.get('title', ''), file=video_file)

        return Response({'id': video.id, 'title': video.title}, status=status.HTTP_201_CREATED)
        """

class ScreenVideoViewSet(viewsets.ModelViewSet):
    queryset= ScreenVideo.objects.all()
    serializer_class= ScreenVideoSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
  


class ScreenVideoUploadView(generics.CreateAPIView):
    queryset= ScreenVideo.objects.all()
    serializer_class= ScreenVideoSerializer
    #parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['video_file']

        # Save the uploaded video file to S3
        s3 = boto3.client('s3')
        s3.upload_fileobj(file_obj, AWS_STORAGE_BUCKET_NAME, file_obj.name)

        # You can optionally save the S3 URL in your database
        video_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_obj.name}"

        return Response({'message': 'Video uploaded successfully'}, status=status.HTTP_201_CREATED)





"""class ScreenUploadView(APIView):
    
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = VideoSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

"""
class ScreenVideoDetailView(generics.RetrieveAPIView):
    queryset = ScreenVideo.objects.all()
    serializer_class = ScreenVideoSerializer
    def retrieve(self, request,*args, **kwargs):
        video = self.get_object()

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        try:
            response = s3.get_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=str(video.video_file)
            )
            video_data = response['Body'].read()
            return Response(video_data, content_type=response['ContentType'])
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class VideoTranscriptionView(generics.UpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def perform_update(self, serializer):
        video = serializer.instance
        if video.status == 'pending':
            transcribe_video.delay(video.id)
        serializer.save()
"""



 
 
"""class SignedURLView(generic.View):
    def post(self, request, *args, **kwargs):
        session = boto3.session.Session()
        client = session.client(
            "s3",
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
 
        url = client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": "media",
                "Key": f"uploads/{json.loads(request.body)['fileName']}",
            },
            ExpiresIn=300,
        )
        return JsonResponse({"url": url})"""
