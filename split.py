import os
from utils import getTranscriptFiles, srt_to_transcript, split_waveform_by_timestamps

ROOT = os.getcwd()

filesDir = os.path.join(ROOT, "files")
wavsDir = os.path.join(ROOT, "mono")
outputDir = os.path.join(ROOT, "splitwavs")
os.makedirs(outputDir, exist_ok=True)
files = getTranscriptFiles(filesDir)

for filepath, showname, filename in files:
    episode = filename.split("_-_")[0]
    transcript = srt_to_transcript(filepath)
    input_file = os.path.join(wavsDir, showname, filename.replace(".srt", ".wav"))
    split_waveform_by_timestamps(input_file, outputDir, transcript, showname, episode)
