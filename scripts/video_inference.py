"""Run YOLO inference on a video and overlay per-frame class counts."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="Path to a YOLO weights file")
    parser.add_argument("--input", type=Path, required=True, help="Input video path")
    parser.add_argument("--output", type=Path, required=True, help="Annotated output video path")
    parser.add_argument("--confidence", type=float, default=0.25, help="Detection confidence threshold")
    parser.add_argument("--device", default=None, help="Inference device, for example 0 or cpu")
    return parser.parse_args()


def inspect_video(path: Path) -> tuple[int, int, float]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Could not open input video: {path}")

    try:
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(capture.get(cv2.CAP_PROP_FPS))
    finally:
        capture.release()

    if width <= 0 or height <= 0 or fps <= 0:
        raise ValueError(f"Invalid video metadata: width={width}, height={height}, fps={fps}")
    return width, height, fps


def annotate_video(
    model_path: Path,
    input_path: Path,
    output_path: Path,
    confidence: float = 0.25,
    device: str | None = None,
) -> None:
    if not model_path.is_file():
        raise FileNotFoundError(f"Model weights not found: {model_path}")
    if not input_path.is_file():
        raise FileNotFoundError(f"Input video not found: {input_path}")
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("Confidence must be between 0 and 1")

    width, height, fps = inspect_video(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not writer.isOpened():
        raise RuntimeError(f"Could not create output video: {output_path}")

    model = YOLO(str(model_path))
    predict_options = {"stream": True, "conf": confidence}
    if device is not None:
        predict_options["device"] = device

    try:
        for result in model(str(input_path), **predict_options):
            frame = result.plot()
            class_counts: dict[str, int] = {}

            if result.boxes is not None and result.boxes.cls is not None:
                for class_id in result.boxes.cls.cpu().numpy().astype(int):
                    class_name = str(model.names[class_id])
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1

            for line_number, (class_name, count) in enumerate(sorted(class_counts.items())):
                cv2.putText(
                    frame,
                    f"{class_name}: {count}",
                    (20, 30 + line_number * 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2,
                )

            writer.write(frame)
    finally:
        writer.release()

    print(f"Saved annotated video to: {output_path}")


def main() -> None:
    args = parse_args()
    annotate_video(
        model_path=args.model,
        input_path=args.input,
        output_path=args.output,
        confidence=args.confidence,
        device=args.device,
    )


if __name__ == "__main__":
    main()
