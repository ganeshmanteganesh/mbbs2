from flask import Flask, render_template, request, jsonify
import os, re

app = Flask(__name__)

# ================= CONFIG =================
# This is your main folder path (commit this folder to GitHub)
MAIN_FOLDER = "sample"  # e.g., 'sample' folder inside your project root
# ==========================================

def get_subfolders():
    """Return all subfolders inside MAIN_FOLDER"""
    subfolders = [d for d in os.listdir(MAIN_FOLDER) 
                  if os.path.isdir(os.path.join(MAIN_FOLDER, d))]
    return subfolders

def get_topics(subfolder=None):
    """Return all txt files from a subfolder (or MAIN_FOLDER) with topic name"""
    folder_path = os.path.join(MAIN_FOLDER, subfolder) if subfolder else MAIN_FOLDER
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".txt")]
    files.sort(key=lambda f: os.path.getmtime(f))  # sort by modified time

    topics = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                # Topic name enclosed in #### topic ####
                match = re.search(r"#+\s*(.*?)\s*#+", first_line)
                topic = match.group(1) if match else os.path.basename(path)
                topics.append({"topic": topic, "path": path})
        except:
            continue
    return topics

@app.route("/")
def home():
    subfolders = get_subfolders()
    return render_template("index.html", subfolders=subfolders)

@app.route("/topics")
def topics():
    subfolder = request.args.get("folder")
    data = get_topics(subfolder)
    return jsonify(data)

@app.route("/read")
def read_file():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "File not found"})
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return jsonify({"content": content})

# No app.run() needed for Vercel
