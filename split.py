import os
import time
import logging
from utils import getTranscriptFiles, srt_to_transcript, split_waveform_by_timestamps

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("logs.txt"), stream_handler],
)

ROOT = os.getcwd()

isCleanAudio = True if os.path.isdir("clean_audio") else False

filesDir = os.path.join(ROOT, "clean_output" if isCleanAudio else "output")
wavsDir = os.path.join(ROOT, "clean_audio" if isCleanAudio else "audio")
outputDir = os.path.join(ROOT, "clean_splitwavs" if isCleanAudio else "splitwavs")
os.makedirs(outputDir, exist_ok=True)
files = getTranscriptFiles(filesDir)

for filepath, showname, filename in files:
    start_time = time.time()
    episode = filename.split("_-_")[0] if "_-_" in filename else filename.split(".")[0]
    transcript = srt_to_transcript(filepath)
    input_file = os.path.join(wavsDir, showname, filename.replace(".srt", ".wav"))
    split_waveform_by_timestamps(input_file, outputDir, transcript, showname, episode)
    execution_time = time.time() - start_time
    logging.info(f"{showname}/{filename}|{execution_time}")
