from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = os.path.join(UPLOAD_FOLDER, "data.xlsx")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, "data.xlsx")
            file.save(file_path)
            return "✅ Soubor byl nahrán! <a href='/'>Zpět</a>"

    if os.path.exists(DATA_FILE):
        df = pd.read_excel(DATA_FILE)
        table_html = df.to_html(classes="table table-striped", index=False)
    else:
        table_html = "<p>❌ Žádný soubor s daty není k dispozici. Nahrajte nový!</p>"

    return render_template("table.html", table=table_html)

# ✅ API, které vrátí data ve formátu JSON
@app.route("/data", methods=["GET"])
def get_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_excel(DATA_FILE)
        return jsonify(df.to_dict(orient="records"))
    return jsonify({"error": "Soubor data.xlsx nebyl nalezen!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
