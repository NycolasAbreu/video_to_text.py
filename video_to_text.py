import os
import argparse
from moviepy import VideoFileClip
import whisper

def convert_to_mp3(video_path, mp3_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(mp3_path, logger="bar")

def concatenate_dir_names(base_dir, file_path):
    relative_path = os.path.relpath(file_path, base_dir)
    path_without_ext = os.path.splitext(relative_path)[0]
    concatenated_name = path_without_ext.replace(os.sep, "_")
    return concatenated_name

def transcribe_from_folder(base_dir, output_dir, video_ext, model_name):
    os.makedirs(output_dir, exist_ok=True)

    model = whisper.load_model(name=model_name)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(video_ext):
                video_path = os.path.join(root, file)
                base_name = concatenate_dir_names(base_dir, video_path)

                mp3_path = os.path.join(root, base_name + ".mp3")
                output_txt_path = os.path.join(output_dir, base_name + ".txt")

                if os.path.exists(output_txt_path):
                    print(f"Text file: {output_txt_path} already exists, skipping...")
                    continue

                print(f"Converting video file: {video_path}")
                convert_to_mp3(video_path, mp3_path)

                print(f"Transcribing audio file: {mp3_path}")
                result = model.transcribe(mp3_path)
                with open(output_txt_path, "w", encoding="utf-8") as f:
                    f.write(result["text"])
                print(f"Saved transcription to: {output_txt_path}")

                os.remove(mp3_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio from videos in a folder using Whisper.")
    parser.add_argument(
        "--input", "-i",
        default=".",
        help="Base directory containing videos (default: current directory)."
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output directory for transcriptions (default: 'output' inside the base directory)."
    )
    parser.add_argument(
        "--ext", "-e",
        default=".mp4",
        choices=[".mp4", ".avi", ".mov", ".mpeg", ".ogv"],
        help="Video file extension to process (default: .mp4).\n"
    )
    parser.add_argument(
        "--model", "-m",
        default="turbo",
        choices=["tiny", "base", "small", "medium", "large", "turbo"],
        help=(
            "Whisper model to use (default: turbo).\n"
            "Available models with relative speeds:\n"
            "  tiny   (~10x)\n"
            "  base   (~7x)\n"
            "  small  (~4x)\n"
            "  medium (~2x)\n"
            "  large  (~1x)\n"
            "  turbo  (~8x)"
        )
    )

    args = parser.parse_args()

    base_dir = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output) if args.output else os.path.join(base_dir, "output")

    transcribe_from_folder(base_dir, output_dir, args.ext, args.model)
