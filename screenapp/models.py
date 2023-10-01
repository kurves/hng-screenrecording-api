from django.db import models
import os
import subprocess
import whisper

# Create your models here.


class ScreenVideo(models.Model):
    title=models.CharField(max_length=100)
    video_file=models.FileField(upload_to="recorded_videos/")
    timestamp=models.DateTimeField(auto_now_add=True)
    transcription=models.TextField(blank=True,)
    #transcription_status = models.CharField(
        #max_length=20, default='queued', choices=[('queued', 'Queued'), ('transcribing', 'Transcribing'), ('completed', 'Completed')]
    #)


    def trancribe_audio(self,audio_path):
        model = whisper.load_model("base")
        result = model.transcribe(audio_path,content_type="audio/wav" , verbose=True)
       # response = openai.Transcription.create(
         #   audio=openai.Audio.from_file(audio_path, content_type="audio/wav"),
        #    model="whisper-large",)
        
        transcription_result = result['text']
        return transcription_result


    def transcribe_video(self):
        video_path=self.video_file.video_path

        audio_path=os.path.join('media','temp_audio.wav')
        transcription_path=os.path.join('media','transcription.txt')

        subprocess.run(['ffmpeg','-i',video_path,'-vn','-acodec','pcm_s161e','-ar','44100','-ac','2',audio_path])

        api_key = openai_secret_manager.get_secret("api_whisper_key") 
        openai.api_key = api_key["api_key"]

        transcription_result = trancribe_audio(audio_path)

        with open(transcription_path, 'w') as file:
            file.write(transcription_result)
        self.transcription = transcription_result
        self.save()    
    def __str__(self):
        return self.title 


