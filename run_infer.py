# -*- coding: utf-8 -*-
from pathlib import Path
from dotenv import load_dotenv
from scipy.io import wavfile
from rvc.modules.vc.modules import VC

def main():
    vc = VC()
    # モデルの相対パスを指定（スクリプトの実行位置が Retrieval-based-Voice-Conversion/ の場合）
    model_path = Path("assets/modeldata/20230525_v2版_CommonVoiceベースRVCモデル_クール系_/20230525_v2版_CommonVoiceベースRVCモデル「クール系」/CommonVoice02a8V2.pth")
    vc.get_vc(str(model_path))

    # 音声ファイルの相対パス
    input_wav_path = Path("assets/modeldata/2025052011084814960KAm_001.wav/2025052011084814960KAm_001.wav")


    tgt_sr, audio_opt, times, _ = vc.vc_inference(
        sid=1,
        input_audio_path=input_wav_path
    )
    wavfile.write("output.wav", tgt_sr, audio_opt)

if __name__ == "__main__":
    load_dotenv(".env")
    main()

