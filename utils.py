import os
from datetime import timedelta

import torchaudio


def getTranscriptFiles(transcriptDir):
    dirs = [
        (os.path.join(transcriptDir, dir), dir)
        for dir in sorted(os.listdir(transcriptDir))
        if ".DS_Store" not in dir
    ]

    files = [
        (os.path.join(dir, file), showname, file)
        for dir, showname in dirs
        for file in sorted(os.listdir(dir))
        if ".srt" in file
        if ".DS_Store" not in file
    ]
    return files


def timeToSeconds(time):
    hhmmss = time.split(",")[0]
    ms = time.split(",")[1]
    hh = hhmmss.split(":")[0]
    mm = hhmmss.split(":")[1]
    ss = hhmmss.split(":")[2]
    seconds = timedelta(
        hours=int(hh), minutes=int(mm), seconds=int(ss), milliseconds=int(ms)
    )
    return seconds.total_seconds()


def srt_to_transcript(filepath):
    srt = open(filepath, encoding="utf-8-sig").read().replace("\n\n", "\n").splitlines()
    grouped = [srt[i : i + 3] for i in range(0, len(srt), 3)]
    transcript = [
        (
            idx,
            timeToSeconds(times.split(" --> ")[0]),
            timeToSeconds(times.split(" --> ")[1]),
            speech.split(": ")[0],
            speech.split(": ")[1],
        )
        for idx, times, speech in grouped
        if timeToSeconds(times.split(" --> ")[1])
        > timeToSeconds(times.split(" --> ")[0])
    ]
    return transcript


def split_waveform_by_timestamps(input_file, output_dir, transcript, showname, episode):
    mono_waveform, sample_rate = torchaudio.load(input_file)
    episode_output_dir = os.path.join(output_dir, showname, episode)
    os.makedirs(episode_output_dir, exist_ok=True)

    for idx, start, end, speaker, speech in transcript:
        start_frame = int(start * sample_rate)
        end_frame = int(end * sample_rate)
        segment = mono_waveform[0:, start_frame:end_frame]
        output_file = os.path.join(
            episode_output_dir, f"{showname}_{episode}_{start}_{end}_{speaker}.wav"
        )

        torchaudio.save(output_file, segment, sample_rate)
