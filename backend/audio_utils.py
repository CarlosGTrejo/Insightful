import ffmpeg
import numpy as np


def audio_to_flac(audio_bytes: bytes) -> bytes:
    '''Converts mp3 to flac with CUDA hardware acceleration'''
    process = (
        ffmpeg
        .input('pipe:', threads=0)
        .output('pipe:', format='flac')
        .run_async(cmd=['ffmpeg', '-hide_banner'], pipe_stdin=True, pipe_stdout=True)
    )

    out, _ = process.communicate(input=audio_bytes)  # process mp3_bytes
    return out


def load_audio(audio_bytes: bytes, sample_rate: int = 16_000) -> np.ndarray:
    """
    Use file's bytes and transform to mono waveform, resampling as necessary
    Parameters
    ----------
    audio_bytes: bytes
        The bytes of the audio file
    sample_rate: int
        The sample rate to resample the audio if necessary
    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input('pipe:', threads=0)  # threads=0 for optimal thread detection
            .output("pipe:", format="s16le", acodec="pcm_s16le", ac=1, ar=sample_rate)
            .run_async(cmd=['ffmpeg', '-hide_banner'], pipe_stdin=True, pipe_stdout=True)
        ).communicate(input=audio_bytes)

    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
