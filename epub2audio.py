#!/usr/bin/env python

import argparse
from TTS.api import TTS
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import torch
import os

# Constants
SPEAKER = "p273"
EMOTION = "happy"

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Convert text from an EPUB file to speech.')

    # Add the file path argument
    parser.add_argument('--file_path', type=str, help='Path to the EPUB file')

    # Add the output path argument
    parser.add_argument('--output_path', type=str, help='Path to save the output speech files')

    # Add the from number argument
    parser.add_argument('--from_chapter', type=int, nargs='?', help='Number indicate from what chapter', default=None)

    # Add the to number argument
    parser.add_argument('--to_chapter', type=int, nargs='?', help='Number indicate to what chapter', default=None)

    # Parse the arguments
    args = parser.parse_args()

    # Check if the file path argument is provided
    if not args.file_path:
        raise ValueError("File path is required")

    # Check if the output path argument is provided
    if not args.output_path:
        raise ValueError("Output path is required")

    if args.to_chapter and args.from_chapter > args.to_chapter:
        raise ValueError("Invalid to chapter argument")

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    module_name = "tts_models/en/vctk/vits"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tts = TTS(model_name=module_name, vocoder_path="vocoder_models/en/vctk/hifigan_v2", config_path=False).to(device)

    book = epub.read_epub(args.file_path)

    for index, item in enumerate(book.get_items()):
        if item.get_type() ==  ebooklib.ITEM_DOCUMENT:
            xhtml = item.get_content()
            soup = BeautifulSoup(xhtml)
            content = clean_text(soup.get_text())

            if is_chapter_within_range(index, args.from_chapter, args.to_chapter):
                convert_to_speech(tts, content, args.output_path, index)

def clean_text(text):
    # Clean the text as needed
    replacements = {
        "“": "'",
        "”": "'",
        "…": "...",
        "‘": "'",
        "’": "'",
        "[": "",
        "]": "",
        "{": "",
        "}": "",
        "*": "",
        "$": "",
        "#": "",
        "-": " ",
        "@": "",
        "%": "",
        "^": "",
        "|": "",
        "\n": " ",
        "~": "",
        "'͡'": "",
        ":": ",",
        "...": " dot dot dot",
        "<": "",
        ">": "",
        "": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def is_chapter_within_range(chapter_index, from_chapter, to_chapter):
    if from_chapter is not None:
        if to_chapter is not None:
            return from_chapter <= chapter_index <= to_chapter
        return from_chapter <= chapter_index
    return True

def convert_to_speech(tts, text, output_path, chapter_index):
    output_file_path = os.path.join(output_path, f"chapter {chapter_index}.wav")
    print(f"Converting chapter {chapter_index}")
    tts.tts_to_file(text=text, file_path=output_file_path, speed="1", speaker=SPEAKER, emotion=EMOTION)
