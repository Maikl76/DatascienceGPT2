from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# 📁 Složka pro nahrávání souborů
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Cesta k souboru s daty (pokud není, zobrazí se výchozí zpráva)
DATA_FILE = os.path.join(UPLOAD_FOLDER, "data.xlsx")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, "data.xlsx")
            file.save(file_path)
            return "✅ Soubor byl nahrán! <a href='/'>Zpět</a>"

    # 🔹 Načítání dat z Excelu
    if os.path.exists(DATA_FILE):
        df = pd.read_excel(DATA_FILE)
        table_html = df.to_html(classes="table table-striped", index=False)
    else:
        table_html = "<p>❌ Žádný soubor s daty není k dispozici. Nahrajte nový!</p>"

    return render_template("table.html", table=table_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
