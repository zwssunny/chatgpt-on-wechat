import wave
import pilk
from pydub import AudioSegment


def get_pcm_from_wav(wav_path):
    """
    从 wav 文件中读取 pcm

    :param wav_path: wav 文件路径
    :returns: pcm 数据
    """
    wav = wave.open(wav_path, "rb")
    return wav.readframes(wav.getnframes())


def mp3_to_wav(mp3_path, wav_path):
    """把mp3格式转成pcm文件
    """
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")


def pcm_to_silk(pcm_path, silk_path, tencent: bool = True):
    """
    wav 文件转成 silk
    """
    pilk.SilkEncoder().encode(pcm_path, silk_path, tencent)


def silk_to_wav(silk_path, wav_path, rate: int = 24000):
    """
    silk 文件转 wav
    """
    pilk.silk_to_wav(silk_path, wav_path, rate)
