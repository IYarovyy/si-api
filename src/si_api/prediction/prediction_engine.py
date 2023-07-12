import joblib
import librosa
import torch
import pandas as pd
import numpy as np
from quart.datastructures import FileStorage


class PredictionEngine:
    def __init__(self, models_path: str, scaler_path: str):
        self.scaler = joblib.load(scaler_path)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.best_model = torch.load(models_path)

    @classmethod
    async def __adjust_signal_length(cls, signal, target_length):
        current_length = len(signal)
        if current_length < target_length:
            pad_length = target_length - current_length
            padded_signal = np.pad(signal, (0, pad_length), mode='constant')
            return padded_signal
        elif current_length > target_length:
            trimmed_signal = signal[:target_length]
            return trimmed_signal
        else:
            return signal

    @classmethod
    async def __load_audio_file(cls, file: FileStorage, duration=6):
        # audio_format = file_path.split('.')[-1]
        # if audio_format == 'wav':
        #     signal, sr = librosa.load(file_path, sr=44100, duration=duration)#, offset=0.6)
        # else:
        #     audio_path = 'audio.mp3'
        #     with audioread.audio_open(audio_path) as input_file:
        #         sr = input_file.samplerate
        #         signal = input_file.read_channels()[0]
        #
        #     # применение необходимых преобразований
        #     signal = librosa.resample(signal, sr, 44100)
        #     sr = 44100
        return librosa.load(file, sr=44100, duration=duration)

    @classmethod
    async def __extract_features(cls, signal, sr):

        # Задаем размер окна в сэмплах
        win_size = 1024  # 256#512#2048
        # Задаем размер окна в секундах
        win_duration = 0.025
        # Получаем размер перекрытия в сэмплах
        hop_length = int(win_size / 4)
        # применение оконной функции Ханна
        window = np.hanning(win_size)

        # вычисление степенного спектра
        spec = librosa.stft(signal, n_fft=win_size, hop_length=hop_length, window=window)
        spec = np.mean((np.abs(spec) ** 2).T, axis=0)
        # вычисление мел-кепстральных коэффициентов
        n_mfcc = 120  # 40
        mfcc = np.mean(
            librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc, n_fft=2 * win_size, hop_length=hop_length).T,
            axis=0)
        # вычисление спектральных фичей
        spectral_flatness = librosa.feature.spectral_flatness(y=signal).mean(axis=1)
        spectral_centroid = librosa.feature.spectral_centroid(y=signal, sr=sr).mean(axis=1)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=signal, sr=sr).mean(axis=1)
        spectral_contrast = librosa.feature.spectral_contrast(y=signal, sr=sr).mean(axis=1)
        spectral_flux = librosa.onset.onset_strength(y=signal, sr=sr).reshape(1, -1).mean(axis=1)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=signal, sr=sr).mean(axis=1)

        # root-mean-square (RMS) value
        rmss = np.mean(librosa.feature.rms(y=signal, frame_length=win_size, hop_length=hop_length).T, axis=0)
        # Zero Crossing Rate
        zcrs = np.mean(librosa.feature.zero_crossing_rate(y=signal).T, axis=0)

        # объединение фичей в один массив
        features = np.concatenate((spec, mfcc,
                                   spectral_flatness, spectral_centroid, spectral_bandwidth,
                                   spectral_flux, spectral_rolloff, spectral_contrast, rmss, zcrs), axis=0)  #
        features = torch.tensor(features)  # torch.flatten(torch.tensor(features), 1)
        return features.detach().numpy()  # [0]

    async def __process_signals(self, file: FileStorage):
        duration = 6
        signal_duration = 9
        sr = 44100
        signal_length = sr * signal_duration

        signal, sr = await self.__load_audio_file(file, duration)
        signal = await self.__adjust_signal_length(signal, signal_length)
        speach_tensor = await self.__extract_features(signal, sr)
        features = speach_tensor
        return features

    async def analize(self, file: FileStorage):
        features = await  self.__process_signals(file)
        columns = [f'feature_{i}' for i in range(len(features))]
        # df = pd.DataFrame(features)
        df = pd.DataFrame(features, columns=columns)
        test_df = pd.DataFrame(self.scaler.transform(df))

        test_features = torch.tensor(test_df.values, dtype=torch.float32).to(self.device)
        # test_labels = torch.tensor(test_y.values, dtype=torch.long).to(self.device)

        with torch.no_grad():
            outputs = self.best_model(test_features)
            predictions = torch.argmax(outputs, 1).detach().numpy()
            for it in range(outputs.shape[0]):
                prob = outputs[it, :]
                sorted_classes = torch.argsort(prob, descending=True)
                top_classes = sorted_classes[:3].tolist()
                return top_classes
