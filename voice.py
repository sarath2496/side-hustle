from utils.json_to_class import Converter
from ai_tools.elevenlabs.voice_settings import VoiceSettings

class Sample(Converter):
    def __init__(self, sample_id, file_name, mime_type, size_bytes, hash):
        self.sample_id = sample_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.size_bytes = size_bytes
        self.hash = hash

    def __repr__(self) -> str:
        return self.sample_id

class Recording(Converter):
    def __init__(self, recording_id, mime_type, size_bytes, upload_date_unix, transcription):
        self.recording_id = recording_id
        self.mime_type = mime_type
        self.size_bytes = size_bytes
        self.upload_date_unix = upload_date_unix
        self.transcription = transcription

    def __repr__(self) -> str:
        return self.recording_id

class VerificationAttempt(Converter):
    def __init__(self, text, date_unix, accepted, similarity, levenshtein_distance, recording):
        self.text = text
        self.date_unix = date_unix
        self.accepted = accepted
        self.similarity = similarity
        self.levenshtein_distance = levenshtein_distance
        self.recording = Recording.from_json(recording) if recording else None

    def __repr__(self) -> str:
        return self.text

class ManualVerificationFile(Converter):
    def __init__(self, file_id, file_name, mime_type, size_bytes, upload_date_unix):
        self.file_id = file_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.size_bytes = size_bytes
        self.upload_date_unix = upload_date_unix

    def __repr__(self) -> str:
        return self.file_name

class ManualVerification(Converter):
    def __init__(self, extra_text, request_time_unix, files):
        self.extra_text = extra_text
        self.request_time_unix = request_time_unix
        self.files = [ManualVerificationFile.from_json(f) for f in files] if files else []

    def __repr__(self) -> str:
        return self.extra_text

class FineTuning(Converter):
    def __init__(self, language, is_allowed_to_fine_tune, fine_tuning_requested, finetuning_state, verification_attempts, verification_failures, verification_attempts_count, slice_ids, manual_verification, manual_verification_requested):
        self.language = language
        self.is_allowed_to_fine_tune = is_allowed_to_fine_tune
        self.fine_tuning_requested = fine_tuning_requested
        self.finetuning_state = finetuning_state
        self.verification_attempts = [VerificationAttempt.from_json(v) for v in verification_attempts] if verification_attempts else []
        self.verification_failures = verification_failures or []
        self.verification_attempts_count = verification_attempts_count
        self.slice_ids = slice_ids or []
        self.manual_verification = ManualVerification.from_json(manual_verification) if manual_verification else None
        self.manual_verification_requested = manual_verification_requested

    def __repr__(self) -> str:
        return self.finetuning_state

class Sharing(Converter):
    def __init__(self, status, history_item_sample_id, original_voice_id, public_owner_id, liked_by_count, cloned_by_count, whitelisted_emails, name, labels, description, review_status, review_message, enabled_in_library):
        self.status = status
        self.history_item_sample_id = history_item_sample_id
        self.original_voice_id = original_voice_id
        self.public_owner_id = public_owner_id
        self.liked_by_count = liked_by_count
        self.cloned_by_count = cloned_by_count
        self.whitelisted_emails = whitelisted_emails or []
        self.name = name
        self.labels = labels
        self.description = description
        self.review_status = review_status
        self.review_message = review_message
        self.enabled_in_library = enabled_in_library

    def __repr__(self) -> str:
        return self.name

class Voice(Converter):
    def __init__(self, voice_id, name, samples, category, fine_tuning, labels, description, preview_url, available_for_tiers, settings, sharing, high_quality_base_model_ids):
        self.voice_id = voice_id
        self.name = name
        self.samples = [Sample.from_json(s) for s in samples] if samples else []
        self.category = category
        self.fine_tuning = FineTuning.from_json(fine_tuning) if fine_tuning else None
        self.labels = labels
        self.description = description
        self.preview_url = preview_url
        self.available_for_tiers = available_for_tiers or []
        self.settings = VoiceSettings.from_json(settings) if settings else None
        self.sharing = Sharing.from_json(sharing) if sharing else None
        self.high_quality_base_model_ids = high_quality_base_model_ids or []

    def __repr__(self) -> str:
        return self.name
    
    def get_voice_name(self):
        return self.name
    
    def get_voice_id(self):
        return self.voice_id
