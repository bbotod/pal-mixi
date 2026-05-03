from flask import Flask, render_template, request, jsonify, send_file, abort
import os
import json
from pathlib import Path
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)

TASKS_DIR = Path(__file__).parent / "tasks"
TASKS_DIR.mkdir(exist_ok=True)
(TASKS_DIR / "Megoldasok").mkdir(exist_ok=True)

ALLOWED_EXT = {".mxf"}

def get_task_list():
    tasks = []
    solutions = []
    for f in sorted(TASKS_DIR.glob("*.mxf")):
        tasks.append({"name": f.stem, "filename": f.name})
    for f in sorted((TASKS_DIR / "Megoldasok").glob("*.mxf")):
        solutions.append({"name": f.stem, "filename": f"Megoldasok/{f.name}"})
    return tasks, solutions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks")
def api_tasks():
    tasks, solutions = get_task_list()
    return jsonify({"tasks": tasks, "solutions": solutions})

@app.route("/api/task/<path:filename>")
def api_task(filename):
    path = TASKS_DIR / filename
    if not path.resolve().is_relative_to(TASKS_DIR.resolve()):
        abort(403)
    if not path.exists() or path.suffix.lower() not in ALLOWED_EXT:
        abort(404)
    return path.read_text(encoding="latin-1").strip(), 200, {"Content-Type": "text/plain"}

@app.route("/api/save", methods=["POST"])
def api_save():
    data = request.get_json()
    name = secure_filename(data.get("name", "task")).replace(" ", "_")
    content = data.get("content", "")
    folder = data.get("folder", "tasks")  # "tasks" or "Megoldasok"

    if not name or not content:
        return jsonify({"error": "Missing name or content"}), 400

    if folder == "Megoldasok":
        save_path = TASKS_DIR / "Megoldasok" / f"{name}.mxf"
    else:
        save_path = TASKS_DIR / f"{name}.mxf"

    save_path.write_text(content, encoding="latin-1")
    return jsonify({"ok": True, "filename": save_path.name})

@app.route("/api/download/<path:filename>")
def api_download(filename):
    path = TASKS_DIR / filename
    if not path.resolve().is_relative_to(TASKS_DIR.resolve()):
        abort(403)
    if not path.exists():
        abort(404)
    content = path.read_bytes()
    return send_file(
        io.BytesIO(content),
        as_attachment=True,
        download_name=path.name,
        mimetype="application/octet-stream"
    )

@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    f = request.files["file"]
    if not f.filename.endswith(".mxf"):
        return jsonify({"error": "Only .mxf files allowed"}), 400
    name = secure_filename(f.filename)
    folder = request.form.get("folder", "tasks")
    if folder == "Megoldasok":
        dest = TASKS_DIR / "Megoldasok" / name
    else:
        dest = TASKS_DIR / name
    f.save(dest)
    content = dest.read_text(encoding="latin-1").strip()
    return jsonify({"ok": True, "filename": name, "content": content})

@app.route("/api/delete/<path:filename>", methods=["DELETE"])
def api_delete(filename):
    path = TASKS_DIR / filename
    if not path.resolve().is_relative_to(TASKS_DIR.resolve()):
        abort(403)
    if path.exists():
        path.unlink()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
