from google.cloud import translate
import google.auth
import logging


# def translate_text(source_lang, target_lang, text):
#     """Translates text into the target language.
#     Target must be an ISO 639-1 language code.
#     See https://g.co/cloud/translate/v2/translate-reference#supported_languages
#     """
#     translate_client = translate.Client()

#     # Text can also be a sequence of strings, in which case this method
#     # will return a sequence of results for each text.
#     result = translate_client.translate(
#         text, target_language=target_lang)

#     print(u'Text: {}'.format(result['input']))
#     print(u'Translation: {}'.format(result['translatedText']))
#     print(u'Detected source language: {}'.format(
#         result['detectedSourceLanguage']))

def translate_text(target_lang, text):
    # Translates text into the target language.
    # Target must be an ISO 639-1 language code.
    # See https://g.co/cloud/translate/v2/translate-reference#supported_languages

    credentials, project_id = google.auth.default()

    # credentials, project_id = google.auth.default()
    translate_client = translate.Client(credentials=credentials)

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target_lang)

    response = dict()
    response['text'] = result['translatedText']
    return response
