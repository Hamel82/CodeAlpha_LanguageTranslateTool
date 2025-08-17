from flask import Flask, render_template, request, jsonify, send_file
import requests, uuid, json
import os
import azure.cognitiveservices.speech as speechsdk
import tempfile
from langdetect import detect

LANG_TO_VOICE = {
    'af': 'af-ZA-AdriNeural',
    'am': 'am-ET-MekdesNeural',
    'ar': 'ar-AE-FatimaNeural',
    'az': 'az-AZ-BabekNeural',
    'bg': 'bg-BG-KalinaNeural',
    'bn': 'bn-BD-NabanitaNeural',
    'bs': 'bs-BA-VesnaNeural',
    'ca': 'ca-ES-JoanaNeural',
    'cs': 'cs-CZ-VlastaNeural',
    'cy': 'cy-GB-NiaNeural',
    'da': 'da-DK-ChristelNeural',
    'de': 'de-DE-KatjaNeural',
    'el': 'el-GR-AthinaNeural',
    'en': 'en-US-AvaMultilingualNeural',
    'es': 'es-ES-ElviraNeural',
    'et': 'et-EE-AnuNeural',
    'fa': 'fa-IR-DilaraNeural',
    'fi': 'fi-FI-NooraNeural',
    'fil': 'fil-PH-AngelaNeural',
    'fr': 'fr-FR-DeniseNeural',
    'ga': 'ga-IE-OrlaNeural',
    'gu': 'gu-IN-DhwaniNeural',
    'he': 'he-IL-HilaNeural',
    'hi': 'hi-IN-SwaraNeural',
    'hr': 'hr-HR-GabrijelaNeural',
    'hu': 'hu-HU-NoemiNeural',
    'hy': 'hy-AM-AnahitNeural',
    'id': 'id-ID-GadisNeural',
    'is': 'is-IS-GudrunNeural',
    'it': 'it-IT-ElsaNeural',
    'ja': 'ja-JP-NanamiNeural',
    'jv': 'jv-ID-SitiNeural',
    'kk': 'kk-KZ-AigulNeural',
    'km': 'km-KH-PisethNeural',
    'kn': 'kn-IN-SapnaNeural',
    'ko': 'ko-KR-SunHiNeural',
    'lo': 'lo-LA-ChanthavongNeural',
    'lt': 'lt-LT-OnaNeural',
    'lv': 'lv-LV-EveritaNeural',
    'mk': 'mk-MK-MarijaNeural',
    'ml': 'ml-IN-SobhanaNeural',
    'mn': 'mn-MN-YesuiNeural',
    'mr': 'mr-IN-AarohiNeural',
    'ms': 'ms-MY-YasminNeural',
    'mt': 'mt-MT-GraceNeural',
    'my': 'my-MM-ThiriNeural',
    'ne': 'ne-NP-HemkalaNeural',
    'nl': 'nl-NL-FennaNeural',
    'no': 'nb-NO-IselinNeural',
    'or': 'or-IN-SunitaNeural',
    'pa': 'pa-IN-GaganNeural',
    'pl': 'pl-PL-ZofiaNeural',
    'ps': 'ps-AF-LatifaNeural',
    'pt': 'pt-BR-FranciscaNeural',
    'ro': 'ro-RO-AlinaNeural',
    'ru': 'ru-RU-SvetlanaNeural',
    'si': 'si-LK-ThiliniNeural',
    'sk': 'sk-SK-ViktoriaNeural',
    'sl': 'sl-SI-PetraNeural',
    'so': 'so-SO-UbaxNeural',
    'sq': 'sq-AL-AnilaNeural',
    'sr': 'sr-RS-SophieNeural',
    'sv': 'sv-SE-SofieNeural',
    'sw': 'sw-KE-ZuriNeural',
    'ta': 'ta-IN-PallaviNeural',
    'te': 'te-IN-ShrutiNeural',
    'th': 'th-TH-PremwadeeNeural',
    'tr': 'tr-TR-EmelNeural',
    'uk': 'uk-UA-PolinaNeural',
    'ur': 'ur-PK-AsadNeural',
    'uz': 'uz-UZ-MadinaNeural',
    'vi': 'vi-VN-HoaiMyNeural',
    'zh': 'zh-CN-XiaoxiaoNeural',
    'zu': 'zu-ZA-ThandoNeural',
}


app = Flask(__name__)

# Route pour afficher la page HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer la traduction
@app.route('/translate', methods=['POST'])
def translate():
    print(request.get_json())
    key  = ""

    endpoint = "https://api.cognitive.microsofttranslator.com"

    location = "francecentral"

    path = '/translate'

    constructed_url = endpoint + path

    data = request.get_json()

    # 🔹 Retrieving fields from the JSON sent by JS
    text = data.get('text')
    source = data.get('source')
    target = data.get('target')

    if source == "auto":
        try:
            source = detect(text)
        except:
            source = "en"

    params = {
        'api-version': '3.0',
        'from': source,
        'to': target
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'Text': text
    }]

    response_obj = requests.post(constructed_url, params=params, headers=headers, json=body)
    print(f"Response Text: {response_obj.text}")
    response = response_obj.json()
    return jsonify({
        'translated_text': response[0]['translations'][0]['text']
    })

@app.route('/synthetize', methods=['POST'])
def synthetize():

    data = request.get_json()
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if lang == "auto":
        try:
            lang = detect(text)
        except:
            lang = "en"  # fallback par défaut

    voice = LANG_TO_VOICE.get(lang, "en-US-AvaMultilingualNeural")


    # This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
    # Replace with your own subscription key and endpoint, the endpoint is like : "https://YourServiceRegion.api.cognitive.microsoft.com"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), endpoint=os.environ.get('ENDPOINT'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The neural multilingual voice can speak different languages based on the input text.
    speech_config.speech_synthesis_voice_name=voice

    # recorde temporary audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_file:
        audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_file.name)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return send_file(audio_file.name, mimetype="audio/wav")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and endpoint values?")
            return {"error": "Synthèse failed"}, 500
    return {"error": "Unknown error occured"}, 500


if __name__ == '__main__':
    app.run(debug=True)