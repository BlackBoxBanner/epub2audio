import argparse
from TTS.api import TTS
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import torch
import os

# Create the argument parser
parser = argparse.ArgumentParser(description='Convert text from an EPUB file to speech.')

# Add the file path argument
parser.add_argument('--file_path', type=str, help='Path to the EPUB file')

# Add the output path argument
parser.add_argument('--output_path', type=str, help='Path to save the output speech files')

# Add the from number argument
parser.add_argument('--from_chapter',type=int, nargs='?', help='Number indicate from what chapter',default=None)

# Add the to number argument
parser.add_argument('--to_chapter',type=int, nargs='?', help='Number indicate to what chapter',default=None)

# Parse the arguments
args = parser.parse_args()

# Check if the file path argument is provided
if not args.file_path:
    raise ValueError("File path is required")

# Check if the output path argument is provided
if not args.output_path:
    raise ValueError("Output path is required")

if args.to_chapter:
    if args.from_chapter > args.to_chapter:
        raise ValueError("invalid to chapter argument")

# Create the output directory if it doesn't exist
if not os.path.exists(args.output_path):
    os.makedirs(args.output_path)

# Load the EPUB file
book = epub.read_epub(args.file_path)

module_name = "tts_models/en/vctk/vits"
device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS(model_name=module_name, vocoder_path="vocoder_models/en/vctk/hifigan_v2", config_path=False).to(device)

for index, item in enumerate(book.get_items()):
    padded_number = str(index).zfill(5)
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        xhtml = item.get_content()
        soup = BeautifulSoup(xhtml)
        content = (
            soup.get_text()
            .replace("“", "'")
            .replace("”", "'")
            .replace("…", "...")
            .replace("‘", "'")
            .replace("’", "'")
            .replace("[", "")
            .replace("]", "")
            .replace("{", "")
            .replace("}", "")
            .replace("*", "")
            .replace("$", "")
            .replace("#", "")
            .replace("-", " ")
            .replace("@", "")
            .replace("%", "")
            .replace("^", "")
            .replace("|", "")
            .replace("\n", " ")
            .replace("~", "")
            .replace("'͡'", "")
            .replace(":", ",")
            .replace("...", " dot dot dot")
            .replace("<", "")
            .replace(">", "")
            .replace("", "")
        )
        if args.from_chapter is not None:
            if args.to_chapter is not None:
                if index >= args.from_chapter and index <= args.to_chapter:
                    tts.tts_to_file(
                        text=content, file_path=f"{args.output_path}/{padded_number}_chapter {index}.mp3", speed="1", speaker="p273", emotion="happy"
                    )
                else:
                    print(f"chapter {index} will not be converted")
            else:
                if index >= args.from_chapter:
                    tts.tts_to_file(
                        text=content, file_path=f"{args.output_path}/{padded_number}_chapter {index}.mp3", speed="1", speaker="p273", emotion="happy"
                    )
                else:
                    print(f"chapter {index} will not be converted")
        else:
            print(f"converting chapter {index}")
            tts.tts_to_file(
                    text=content, file_path=f"{args.output_path}/{padded_number}_chapter {index}.mp3", speed="1", speaker="p273", emotion="happy"
                )      
        
        
