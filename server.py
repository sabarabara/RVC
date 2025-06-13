from flask import Flask, request, jsonify, send_file
import subprocess
from io import BytesIO
from pathlib import Path
import traceback

app = Flask(__name__)

# 保存パス
INPUT_PATH = Path("assets/modeldata/2025052011084814960KAm_001.wav/2025052011084814960KAm_001.wav")
OUTPUT_PATH = Path("output.wav")

@app.route('/createAndInfer', methods=['POST'])
def handle_create_and_infer():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Missing audio file"}), 400

        # ファイル受け取り
        wav_file = request.files['file']
        INPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        wav_file.save(INPUT_PATH)

        # 推論実行
        result = subprocess.run(
            ["poetry", "run", "python", "run_infer.py"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "error": "Inference failed",
                "stderr": result.stderr,
                "stdout": result.stdout
            }), 500

        return send_file(
            OUTPUT_PATH,
            mimetype='audio/wav',
            as_attachment=True,
            download_name="output.wav"
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)

