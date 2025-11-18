# web_app.py
from flask import Flask, request, jsonify, render_template_string
from modules.checkin import process_checkin

app = Flask(__name__)

@app.post("/checkin-api")
def checkin_api():
    data = request.get_json() or {}
    qr_string = data.get("qr_string", "").strip()
    if not qr_string:
        return jsonify({"ok": False, "message": "Falta qr_string"}), 400

    result = process_checkin(qr_string)
    return jsonify({"ok": True, "message": result})


@app.get("/scanner")
def scanner():
    # Página super simple de ejemplo
    html = """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Scanner de Check-in</title>
      <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
    </head>
    <body>
      <h1>Scanner de Check-in</h1>
      <div id="reader" style="width:300px;"></div>
      <pre id="result"></pre>

      <script>
        function onScanSuccess(decodedText, decodedResult) {
          // decodedText = "EVENT:...|LEAD:...|TS:...|HASH:..."
          fetch("/checkin-api", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ qr_string: decodedText })
          })
          .then(r => r.json())
          .then(data => {
            document.getElementById("result").textContent = data.message;
          })
          .catch(err => {
            document.getElementById("result").textContent = "Error: " + err;
          });
        }

        var html5QrcodeScanner = new Html5QrcodeScanner(
          "reader", { fps: 10, qrbox: 250 }
        );
        html5QrcodeScanner.render(onScanSuccess);
      </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
