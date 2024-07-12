import os
import csv
import argparse
import random
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
import genanki


def translate_flashcards(input_csv, output_csv, credentials, target_language):
    # Set up Google Cloud Translate client
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
    client = translate.Client()

    # Read the input CSV file, translate each row, and write to the output CSV file
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Translated']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            english_text = row['English']
            translation = client.translate(
                english_text, target_language=target_language)
            row['Translated'] = translation['translatedText']
            writer.writerow(row)
            print(f"Translated '{english_text}' to '{row['Translated']}'")

    print(f"Translations complete. Output written to {output_csv}")


def generate_audio_files(csv_file, credentials, language_code, voice_name, speaking_rate):
    # Set up Google Cloud Text-to-Speech client
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
    client = texttospeech.TextToSpeechClient()

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            text = row['Translated']
            audio_filename = f"{text}.mp3"

            # Construct the request
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code, name=voice_name, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speaking_rate)

            # Perform the text-to-speech request
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config)

            # Save the audio file
            with open(audio_filename, 'wb') as out:
                out.write(response.audio_content)
            print(f"Audio content written to file {audio_filename}")

    print("Audio generation complete!")


def generate_anki_deck(csv_file, output_file, deck_name, deck_id):
    # Create the deck
    deck = genanki.Deck(deck_id, deck_name)

    # Read the CSV file, add notes to the deck
    media_files = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            text = row['Translated']
            audio_filename = f"{text}.mp3"

            # Add note to the deck
            note = genanki.Note(
                model=genanki.BASIC_MODEL,
                fields=[text + f'<br>[sound:{audio_filename}]', row['English']]
            )
            deck.add_note(note)
            media_files.append(audio_filename)

    # Create the package and include media files
    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(output_file)

    print(f"Anki deck '{deck_name}' created successfully as {output_file}!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate Anki deck from English flashcards.')
    parser.add_argument(
        'input_csv', help='Path to the input CSV file with English text')
    parser.add_argument(
        'credentials', help='Path to the Google Cloud service account JSON key file')
    parser.add_argument(
        'output_apkg', help='Path to the output Anki package file (.apkg)')
    parser.add_argument('deck_name', help='Name of the Anki deck')
    parser.add_argument(
        'language_code', help='Target language code for translation and TTS (e.g., "ru" for Russian)')
    parser.add_argument('--voice_name', default='ru-RU-Standard-C',
                        help='Voice name for TTS (default: ru-RU-Standard-C)')
    parser.add_argument('--speaking_rate', type=float, default=0.75,
                        help='Speaking rate for TTS (default: 0.75)')
    args = parser.parse_args()

    translated_csv = 'translated_flashcards.csv'
    deck_id = random.randrange(1 << 30, 1 << 31)

    # Step 1: Translate English to target language
    translate_flashcards(args.input_csv, translated_csv,
                         args.credentials, args.language_code)

    # Step 2: Generate audio files
    generate_audio_files(translated_csv, args.credentials,
                         args.language_code, args.voice_name, args.speaking_rate)

    # Step 3: Create Anki deck
    generate_anki_deck(translated_csv, args.output_apkg,
                       args.deck_name, deck_id)
