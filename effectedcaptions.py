import torch
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import face_recognition
from faster_whisper import WhisperModel

# Function to extract audio from the video
def extract_audio_from_video(video_file, audio_file="temp_audio.wav"):
    video_clip = VideoFileClip(video_file)
    video_clip.audio.write_audiofile(audio_file)
    return audio_file

# Function to detect faces and calculate caption positions
def detect_faces_and_caption_positions(frame, gap=50):
    face_locations = face_recognition.face_locations(frame)
    caption_positions = []
    for face_location in face_locations:
        top, right, bottom, left = face_location
        caption_position = (left, bottom + gap)  # Position for the caption
        caption_positions.append((face_location, caption_position))
    return caption_positions

# Function to get face positions for each frame
def get_face_positions(video_file, gap=50, interval_seconds=0):
    video_clip = VideoFileClip(video_file)
    face_positions = []

    # If interval_seconds is set to 0, only process the first frame
    if interval_seconds == 0:
        frame = video_clip.get_frame(0)
        frame_rgb = frame[:, :, ::-1]  # Convert BGR to RGB
        face_positions = detect_faces_and_caption_positions(frame_rgb, gap)
    else:
        # Process frames at the specified interval
        total_duration = int(video_clip.duration)
        for t in range(0, total_duration, interval_seconds):
            frame = video_clip.get_frame(t)
            frame_rgb = frame[:, :, ::-1]
            positions = detect_faces_and_caption_positions(frame_rgb, gap)
            face_positions.append((t, positions))

    return face_positions


# Function to overlay captions
def overlay_captions(video_file, segments, caption_positions):
    video = VideoFileClip(video_file)
    clips = [video]
    video_clip = VideoFileClip('clip.mp4')
    for segment in segments:
        for word in segment.words:
            # Find the position for this word's timestamp
            position = None
            for time, positions in caption_positions:
                if time <= word.start < time + video_clip.fps:  # Assuming one second interval
                    position = positions[0][1] if positions else None  # Use the first face position if available
                    break

            if position is None:
                continue  # Skip if no position found

            txt_clip = TextClip(word.word.upper(), fontsize=70, color='Blue', font='sans-serif')
            txt_clip = txt_clip.set_position(position).set_duration(word.end - word.start).set_start(word.start)
            clips.append(txt_clip)

    final_video = CompositeVideoClip(clips)
    final_video.write_videofile("output_video.mp4", codec="libx264", fps=24)


# Main processing steps
video_file = 'clip.mp4'
audio_file = extract_audio_from_video(video_file)

# Initialize the Whisper model for transcription
model = WhisperModel("large-v2", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_file, beam_size=5, word_timestamps=True)
print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

# Get face positions for each frame
face_positions = get_face_positions(video_file)
overlay_captions(video_file, segments, face_positions)
