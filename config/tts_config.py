# config/tts_config.py

def get_voice(gender: str) -> str:
    """
    Maps gender to Sarvam TTS voice codes
    """
    gender = gender.lower()

    if gender == "male":
        return "hitesh"
    elif gender == "female":
        return "manisha"
    else:
        raise ValueError("Unsupported gender. Use 'male' or 'female'.")
