# Anki Deck Generator

<p align="center">
   <img src="https://git.zaaane.com/zane/anki-deck-generator/raw/branch/main/docs/diagram.png" alt="Diagram" />
</p>

[Anki](https://github.com/ankitects/anki) is the most popular flash card program out there.
The public decks I've come across vary in quality and making your own is all the rage.

This script takes a list of English words and:
1. Translates each one using Google Translate
2. Generates an audio file of the word/phrase being pronounced in the target language
3. Puts it all into an Anki deck (.apkg)

## Prerequisites

1. **Google Cloud Setup:**
   - Enable the [Google Cloud Translate API](https://cloud.google.com/translate/docs/setup) and [Google Cloud Text-to-Speech API](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries).
   - Create a service account and download the JSON key file.

2. **Install Required Libraries:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Script

The `generate_anki_deck.py` script automates the entire process.

```bash
python generate_anki_deck.py input_csv output_dir google_credentials_json output_apkg deck_name language_code [--voice_name VOICE_NAME] [--speaking_rate SPEAKING_RATE]
```

- `input_csv`: Path to the input CSV file with English text.
- `google_credentials_json`: Path to the Google Cloud service account JSON key file.
- `output_apkg`: Path to the output Anki package file (.apkg).
- `deck_name`: Name of the Anki deck.
- `language_code`: Target language code for translation and TTS (e.g., "ru" for Russian).
- `--voice_name`: (Optional) Voice name for TTS (default: `ru-RU-Standard-C`).
- `--speaking_rate`: (Optional) Speaking rate for TTS (default: `0.75`).

Example:
```bash
python generate_anki_deck.py examples/flashcards.csv google_credentials.json ru_food_beginner.apkg "[RU] Food - Beginner I" ru --voice_name ru-RU-Standard-C --speaking_rate 0.75
```

### Customizing for Other Languages

To customize for other languages:
1. **Change the `language_code` argument** to the desired target language code (e.g., `es` for Spanish).
2. **Adjust the `voice_name` and `speaking_rate` arguments** as needed. Refer to the [Google Cloud Text-to-Speech documentation](https://cloud.google.com/text-to-speech/docs/voices) for available voice names and language codes.

### Input CSV Format

The input CSV should have the following format:

```csv
English
Hello
Thank you
```