# Contributing

Thank you for helping improve this research repository.

## Before opening a change

- Never commit medical images, annotations, videos, model weights, or credentials.
- Do not claim performance without including the evaluation protocol and evidence.
- Explain changes to classes, splits, preprocessing, augmentation, or metrics.
- Keep clinical language appropriately limited: detections are not diagnoses.

## Workflow

1. Fork the repository and create a focused branch.
2. Create a Python virtual environment and install `requirements.txt`.
3. Make a small, coherent change and update the documentation.
4. Run Python syntax checks and confirm edited notebooks contain valid JSON.
5. Open a pull request describing the change, validation, and limitations.

Useful commit message examples:

```text
fix: validate output video metadata
docs: document evaluation split requirements
```

## Bug reports

Include the operating system, Python version, command, model type, sanitized
configuration, and full error message. Do not attach private data or secrets.
