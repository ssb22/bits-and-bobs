#!/usr/bin/env python3
"""Text-to-Speech Reader using Gemini API and sox
(sentence by sentence).  Set GEMINI_API_KEY in environment.
Can get "model overloaded" errors if Google servers are busy."""

from google import genai # pip install google-genai
import nltk # pip install nltk (or apt install python3-nltk)

import sys,os,re,tempfile,subprocess,wave
from nltk.tokenize import sent_tokenize
try: nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt')
client = genai.Client()
def readSentence(text):
    types=genai.types
    response = client.models.generate_content(model="gemini-2.5-flash-preview-tts",contents=text,config=types.GenerateContentConfig(response_modalities=["AUDIO"],speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Sulafat')))))
    with tempfile.NamedTemporaryFile(suffix='.wav') as tmp_file:
        w=wave.open(tmp_file,'wb')
        w.setnchannels(1),w.setsampwidth(2),w.setframerate(24000),w.writeframes(response.candidates[0].content.parts[0].inline_data.data),w.close()
        subprocess.run(['play','-q',tmp_file.name],check=True)
    
def split_into_sentences(text):
    try: return [s.strip() for s in sent_tokenize(text) if s.strip()]
    except: return [s.strip() for s in re.split(r'[.!?。！？]+', text) if s.strip()]

def main():
    text = sys.stdin.read().strip()
    if 'gradint.py' in sys.argv[0]:
        language,text = text.split(None,1) # assume we're a Gradint shim expecting justSynthesize line on stdin
    if not text:
        print("No text provided") ; return
    print("Press Ctrl+C to stop")
    try:
        for sentence in split_into_sentences(text):
            readSentence(sentence)
    except KeyboardInterrupt: print("\nPlayback interrupted")
if __name__ == "__main__": main()
