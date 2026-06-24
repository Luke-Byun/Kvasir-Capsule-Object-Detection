# Training notebook guide

`yolo11m_training.ipynb` is a Google Colab-oriented experiment notebook for
training an Ultralytics YOLO11m detector.

## Expected dataset layout

The extracted dataset should use YOLO annotations and provide a `data.yaml`
file similar to the following structure:

```text
kvasir/
|-- data.yaml
|-- train/
|   |-- images/
|   `-- labels/
|-- valid/
|   |-- images/
|   `-- labels/
`-- test/
    |-- images/
    `-- labels/
```

Class names and the number of classes come from `data.yaml`; they are not
hard-coded by this repository.

## Before running

1. Select a GPU runtime in Colab.
2. Review `BASE_PATH` and all dataset paths.
3. Supply a private dataset URL only when prompted at runtime.
4. Review the augmentation and training hyperparameters for your dataset.
5. Save the resulting configuration, metrics, and checkpoint outside Git.

## Credential safety

Do not paste private download links into a notebook cell and save the notebook.
The download cell uses `getpass` so the value is not written into notebook
source or normal cell output. If a key has ever been committed, revoke it at
the provider; deleting it from the latest file does not remove Git history.
