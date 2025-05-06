from mixmatch.core.utils import round_bpm, MUSIC_KEYS_CAMELOT
from pydantic import FilePath

import essentia
essentia.log.infoActive = False
essentia.log.warningActive = False
import essentia.standard as es


def calculate_bpm_key(path: FilePath) -> (str, int):
    features, features_frames = es.MusicExtractor(rhythmStats=['mean'], tonalStats=['mean'])(str(path))
    bpm = round_bpm(features['rhythm.bpm'])
    key = MUSIC_KEYS_CAMELOT.get(str(f'{features["tonal.key_edma.key"]} {features["tonal.key_edma.scale"]}'))
    return bpm, key
