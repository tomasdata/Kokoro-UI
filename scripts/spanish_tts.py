#!/usr/bin/env python3
"""Generación cuidada en español usando Kokoro, orientada a podcasts."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Iterable, List

import numpy as np
import soundfile as sf

from kokoro import KPipeline

BASE_DIR = Path(__file__).resolve().parents[1]
TEXT_PATH = BASE_DIR / "input" / "es_text.txt"
OUTPUT_DIR = BASE_DIR / "output"

LANG_CODE = "e"
VOICE = "ef_dora"  # Cambia aquí si prefieres em_alex o em_santa
SPEED = 0.92
SPLIT_PATTERN = r"\n{2,}"
MAX_CHARS = 320
SILENCE_MS = 320
SAMPLE_RATE = 24_000
OUTPUT_FILE = "output/kokoro-es.wav"


def read_text() -> str:
    if not TEXT_PATH.exists():
        raise FileNotFoundError(
            f"No se encuentra {TEXT_PATH}. Crea el archivo con tu texto en español."
        )
    text = TEXT_PATH.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"{TEXT_PATH} está vacío. Escribe el texto que quieres convertir.")
    return text


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip()


def chunk_text(text: str, max_chars: int) -> List[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    sentence_splitter = re.compile(r"(?<=[.!?¡¿])\s+(?=[A-ZÁÉÍÓÚÑÜ0-9])")

    for para in paragraphs:
        if len(para) <= max_chars:
            chunks.append(para)
            continue

        sentences = [s.strip() for s in sentence_splitter.split(para) if s.strip()]
        current = ""
        for sentence in sentences:
            tentative = f"{current} {sentence}".strip()
            if current and len(tentative) > max_chars:
                chunks.append(current)
                current = sentence
            else:
                current = tentative
        if current:
            chunks.append(current)

    if not chunks and text:
        chunks.append(text)
    return chunks


def synthesize_blocks(pipeline: KPipeline, blocks: Iterable[str], voice: str,
                      speed: float, split_pattern: str) -> List[np.ndarray]:
    audios: List[np.ndarray] = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        block_audio = [
            audio for _, _, audio in pipeline(
                block,
                voice=voice,
                speed=speed,
                split_pattern=split_pattern,
            )
        ]
        if not block_audio:
            raise RuntimeError(f"No se pudo generar audio para el bloque:\n{block}")
        audios.extend(block_audio)
    return audios


def add_silence_between(chunks: List[np.ndarray], silence_ms: int) -> np.ndarray:
    if not chunks:
        raise RuntimeError("No se generaron fragmentos de audio.")
    if silence_ms <= 0:
        return np.concatenate(chunks)
    silence = np.zeros(int(SAMPLE_RATE * (silence_ms / 1000)), dtype=np.float32)
    with_pauses: List[np.ndarray] = []
    for idx, chunk in enumerate(chunks):
        with_pauses.append(chunk)
        if idx < len(chunks) - 1:
            with_pauses.append(silence)
    return np.concatenate(with_pauses)


def should_enable_mps() -> bool:
    is_macos = sys.platform == "darwin"
    default_yes = is_macos
    if is_macos:
        prompt = ("Se detectó macOS. ¿Activar aceleración MPS para usar la GPU? "
                  "[Y/n]: ")
    else:
        prompt = ("Estás en Windows/Linux. Presiona Enter para continuar en CPU "
                  "o escribe 'y' si aun así quieres forzar MPS (no recomendado) [y/N]: ")
    try:
        answer = input(prompt).strip().lower()
    except EOFError:
        answer = ""
    if not answer:
        return default_yes
    return answer in {"y", "yes", "s", "si"}


def configure_acceleration():
    enable_mps = should_enable_mps()
    if enable_mps:
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        print("MPS fallback activado (Apple Silicon).")
    else:
        os.environ.pop("PYTORCH_ENABLE_MPS_FALLBACK", None)
        print("Modo CPU seleccionado.")


def main():
    text = normalize_text(read_text())
    blocks = chunk_text(text, max_chars=MAX_CHARS)

    configure_acceleration()
    print(f"Bloques a sintetizar: {len(blocks)} | Voz: {VOICE} | Velocidad: {SPEED}")
    pipeline = KPipeline(lang_code=LANG_CODE)

    audio_chunks = synthesize_blocks(
        pipeline,
        blocks,
        voice=VOICE,
        speed=SPEED,
        split_pattern=SPLIT_PATTERN,
    )
    audio = add_silence_between(audio_chunks, SILENCE_MS)

    out_path = Path(OUTPUT_FILE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(out_path, audio, SAMPLE_RATE)

    print(f"Texto leído desde: {TEXT_PATH}")
    print(f"Audio guardado en: {out_path}")
    print("Listo para tu podcast 🎙️")


if __name__ == "__main__":
    main()
