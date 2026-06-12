import torch
import torch.nn as nn
from torchvision import models

import librosa
import numpy as np
import sounddevice as sd


# =====================================
# CONFIG
# =====================================

SAMPLE_RATE = 22050
DURATION = 10

MODEL_PATH = "best_siren_model.pth"


# =====================================
# RECORD AUDIO
# =====================================

def record_audio():

    print("\nRecording...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    print("Recording Complete")

    return audio.flatten()


# =====================================
# AUDIO -> SPECTROGRAM
# =====================================

def audio_to_spectrogram(audio):

    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=SAMPLE_RATE,
        n_mels=128
    )

    mel_db = librosa.power_to_db(
        mel,
        ref=np.max
    )

    TARGET_WIDTH = 128

    if mel_db.shape[1] < TARGET_WIDTH:

        mel_db = np.pad(
            mel_db,
            (
                (0, 0),
                (0, TARGET_WIDTH - mel_db.shape[1])
            ),
            mode="constant"
        )

    else:

        mel_db = mel_db[:, :TARGET_WIDTH]

    mel_db = (
        mel_db - mel_db.mean()
    ) / (mel_db.std() + 1e-8)

    mel_db = np.expand_dims(
        mel_db,
        axis=0
    )

    return mel_db


# =====================================
# BUILD MODEL
# =====================================

model = models.resnet18(
    weights=None
)

model.conv1 = nn.Conv2d(
    in_channels=1,
    out_channels=64,
    kernel_size=7,
    stride=2,
    padding=3,
    bias=False
)

model.fc = nn.Linear(
    model.fc.in_features,
    2
)

# =====================================
# LOAD WEIGHTS
# =====================================

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location="cpu"
    )
)

model.eval()

print("Model Loaded Successfully")

def detect_siren():

    audio = record_audio()

    spectrogram = audio_to_spectrogram(
        audio
    )

    spectrogram = torch.tensor(
        spectrogram,
        dtype=torch.float32
    ).unsqueeze(0)

    with torch.no_grad():

        output = model(
            spectrogram
        )

        probs = torch.softmax(
            output,
            dim=1
        )

        pred = output.argmax(1).item()

        confidence = (
            probs[0][pred]
            .item()
        )

    return (
        pred == 1,
        confidence
    )

