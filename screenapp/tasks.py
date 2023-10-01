
import boto3
from celery import shared_task
from django.conf import settings
from .models import Video
from whisper import get_object_content

@shared_task
def transcribe_video(video_id):
    video = Video.objects.get(pk=video_id)
    video.status = 'transcribing'
    video.save()

    # Fetch video content from S3 using Whisper
    video_content = get_object_content(video.file.path)

    # Perform transcription using AWS Transcribe (you'll need to install the AWS SDK and configure credentials)
    transcribe = boto3.client('transcribe', region_name='your-aws-region')
    response = transcribe.start_transcription_job(
        TranscriptionJobName=f'transcription-{video_id}',
        LanguageCode='en-US',
        MediaFormat='mp4',
        Media={
            'MediaFileUri': video_content,
        },
        OutputBucketName='your-transcription-output-bucket',
    )

    # Update the video transcription job name and status
    video.transcription_job_name = response['TranscriptionJob']['TranscriptionJobName']
    video.status = 'transcription_in_progress'
    video.save()
