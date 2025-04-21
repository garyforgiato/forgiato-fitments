from flask import Flask, render_template_string, request
from formatter import format_wheel_order
import os

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Forgiato Fitments</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; padding: 40px 20px; max-width: 700px; margin: auto; }
        h1 { font-size: 2.4em; font-weight: 800; text-align: center; margin-bottom: 30px; }
        label { font-weight: 600; display: block; margin-top: 20px; margin-bottom: 8px; }
        textarea {
            width: 100%; padding: 12px; font-size: 1em;
            border: 1px solid #000; border-radius: 8px;
        }
        input[type=submit] {
            width: 100%; background: #000; color: #fff;
            padding: 14px; border: none; font-weight: 600;
            font-size: 1.1em; border-radius: 8px; cursor: pointer;
            margin-top: 20px;
        }
        input[type=submit]:hover {
            background: #333;
        }
        pre {
            background: #f4f4f4;
            padding: 20px;
            margin-top: 30px;
            border-radius: 8px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>FORGIATO FITMENTS</h1>
    <form method="post">
        <label>Fitment Input</label>
        <textarea name="fitment" rows="3" required>{{ fitment or '' }}</textarea>

        <label>Summary Input</label>
        <textarea name="summary" rows="3" required>{{ summary or '' }}</textarea>

        <input type="submit" value="FORMAT">
    </form>

    {% if output %}
    <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    fitment = summary = ""

    if request.method == "POST":
        fitment = request.form["fitment"]
        summary = request.form["summary"]

        try:
            output = format_wheel_order(fitment, summary)
        except Exception as e:
            output = f"❌ Error: {e}"

    return render_template_string(
        HTML_FORM,
        output=output,
        fitment=fitment,
        summary=summary
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
