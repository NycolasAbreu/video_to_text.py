
# Video Transcriber with Whisper and MoviePy

This Python script recursively scans a directory for video files, extracts their audio, and transcribes the content using OpenAI's [Whisper](https://github.com/openai/whisper) model. Transcriptions are saved as `.txt` files in a specified output folder. It supports custom input/output paths, video file extensions, and Whisper model selection.

## Features

- Recursive video search in folders  
- Converts video audio to `.mp3` using MoviePy  
- Transcribes audio with OpenAI Whisper (models from `tiny` to `turbo`)  
- Saves `.txt` files in an organized output directory  
- Automatically skips already transcribed files  
- Fully configurable via command-line arguments

## Requirements

- Python 3.7+
- ffmpeg (required by MoviePy and Whisper)

To install ffmpeg:
```bash
sudo apt install ffmpeg
```

**Install the required python dependencies**:
   ```bash
   pip install moviepy openai-whisper
   ```

## Usage

```bash
python transcriber.py [OPTIONS]
```

### Options

| Option        | Description                                  | Default        |
|---------------|----------------------------------------------|----------------|
| `--input, -i` | Base directory to search for video files     | `.` (current)  |
| `--output, -o`| Output directory for `.txt` transcriptions   | `./output`     |
| `--ext, -e`   | Video file extension to process              | `.mp4`         |
| `--model, -m` | Whisper model to use                         | `turbo`        |

## 💡 Examples

- Transcribe all `.mp4` videos in the current folder:
  ```bash
  python transcriber.py
  ```

- Transcribe `.mov` videos in a custom input folder:
  ```bash
  python transcriber.py -i ./videos -e .mov
  ```

- Use the `small` model and save transcriptions in a custom output folder:
  ```bash
  python transcriber.py -i ./lectures -o ./transcripts -m small
  ```

## 📄 Output

All transcriptions are saved as `.txt` files in the output directory, using the video’s relative path converted to a flattened filename (e.g., `subfolder_video1.mp4` → `subfolder_video1.txt`).
