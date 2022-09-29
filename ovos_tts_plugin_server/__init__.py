import requests
from ovos_plugin_manager.templates.tts import TTS, TTSValidator


class OVOSServerTTS(TTS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, audio_ext="wav",
                         validator=OVOSServerTTSValidator(self))
        self.host = self.config.get("host") or "http://0.0.0.0:9666"

    def get_tts(self, sentence, wav_file, lang=None, voice=None):
        lang = lang or self.lang
        voice = voice or self.voice
        data = requests.get(f"{self.host}/synthesize/{sentence}",
                            params={"lang": lang, "voice": voice}).content
        with open(wav_file, "wb") as f:
            f.write(data)
        return wav_file, None


class OVOSServerTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(OVOSServerTTSValidator, self).__init__(tts)

    def validate_lang(self):
        pass

    def validate_connection(self):
        pass

    def get_tts_class(self):
        return OVOSServerTTS


OVOSServerTTSConfig = {}

# jarbas public demo instances
jarbas_hosted = {
    "S.A.M.": ("https://sam.jarbasai.online", "male"),
    "PicoTTS": ("https://pico.jarbasai.online", "female"),
    "Glados": ("https://glados.jarbasai.online", "female"),
    "Alan Pope [Mimic 1]": ("https://mimic.jarbasai.online", "male"),
    "R2D2": ("https://r2d2.jarbasai.online", "neutral")
}

OVOSServerTTSConfig["en-us"] = [
    {"lang": "en-us",
     "url": url,
     "gender": gender,
     "display_name": f"{display_name} (jarbasai.online)",
     "offline": False}
    for display_name, (url, gender) in jarbas_hosted.items()
]
