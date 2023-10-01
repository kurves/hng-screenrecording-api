import os
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
from django.conf import settings
import boto3
from .models import ScreenVideo

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.video_chunks = []
        self.file_name = None

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        chunk_data = data.get('chunk_data')
        file_name = data.get('file_name')

        if chunk_data and file_name:
            if not self.file_name:
                self.file_name = file_name

            self.video_chunks.append(chunk_data)
            await self.send(text_data=json.dumps({'message': 'Chunk received successfully'}))
        elif not chunk_data and self.video_chunks:
            await self.send(text_data=json.dumps({'message': 'Recording stopped'}))
            await self.save_and_upload_video()

    async def save_and_upload_video(self):
        try:
            # Assemble the video from chunks
            video_data = b''.join(self.video_chunks)

            # Save the video to a temporary file or database
            temp_file_path = os.path.join(settings.MEDIA_ROOT, self.file_name)
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(video_data)

            # Upload the video to Amazon S3
            s3 = boto3.client('s3')
            s3_key = f'recordings/{self.file_name}'
            with open(temp_file_path, 'rb') as video_file:
                s3.upload_fileobj(video_file, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

            # Delete the temporary file
            os.remove(temp_file_path)

            await self.send(text_data=json.dumps({'message': 'Video saved and uploaded successfully'}))

        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))