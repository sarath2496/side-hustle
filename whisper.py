import logging
from ai_tools.whisper.constants import Whisper
from utils.decorators import typecheck

#logging.basicConfig()
#logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

class WhisperTimestampedFast(Whisper):
    
    @typecheck(object, str, str)
    def _transcribe_audio_to_text(self, audio_path: str, language: str = Whisper.default_language(), *args, **kwargs):
        """
        Transcribes an audio file to text using the Whisper ASR system with timestamped outputs.

        Parameters:
        - audio_path (str): Path to the audio file to be transcribed.
        - language (str, optional): Language code for transcription. Defaults to the system's default language.

        Returns:
        - dict: Result containing the transcribed text along with timestamps and other related information.

        Usage:
        >>> asr_system = WhisperTimestamped() 
        >>> result = asr_system.transcribe_audio_to_text('path/to/audio/file.wav', 'en')
        >>> print(result['text'])
        "Hello, how are you?"

        Notes:
        - This function relies on the Whisper ASR system, and assumes that necessary models and configurations 
          are properly set up.
        - The function also makes use of type checking to ensure correct data types for the function arguments.

        Raises:
        - FileNotFoundError: If the provided audio file path does not exist.
        - ValueError: If an unsupported language code is provided.
        """
        segments, info = self.whisper_fast_model().transcribe(
            audio=audio_path,
            language=language,
            task='transcribe',
            beam_size=kwargs.get('beam_size', self.beam_size),
            vad_filter=kwargs.get('vad', self.vad),
            word_timestamps=kwargs.get('word_timestamps', True),
            temperature=kwargs.get('temperature', self.temperature),
            condition_on_previous_text=False
        )

        whisper_response = {
            'segments': []
        }

        for segment in segments:
            words = []

            if segment.words is not None:
                for word in segment.words:
                    fixed_text = word.word
                    word_start = word.start
                    word_end = word.end

                    if word_start is None:
                        continue

                    if word_end is None:
                        continue

                    for suppress_string in self.STRINGS_TO_SUPPRESS:
                        fixed_text = fixed_text.replace(suppress_string, '')

                    words.append(
                        {
                            'start': word_start,
                            'end': word_end,
                            'text': self.censor_word(word=fixed_text)
                        }
                    )

            whisper_response['segments'].append(
                {
                    'id': segment.id,
                    'seek': segment.seek,
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text,
                    'tokens': segment.tokens,
                    'temperature': segment.temperature,
                    'avg_logprob': segment.avg_logprob,
                    'compression_ratio': segment.compression_ratio,
                    'no_speech_prob': segment.no_speech_prob,
                    'words': words
                }
            )

        return whisper_response
