from flask import Flask, request, send_file, render_template_string
import os
import tempfile

from work import redact_document

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PII Redaction Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 80px auto;
            padding: 30px;
        }

        h1 {
            margin-bottom: 10px;
        }

        p {
            color: #555;
        }

        form {
            margin-top: 30px;
        }

        input {
            margin-bottom: 20px;
        }

        button {
            padding: 10px 20px;
            cursor: pointer;
        }
    </style>
</head>

<body>

    <h1>PII Redaction Tool</h1>

    <p>
        Upload a DOCX document to detect and replace
        personally identifiable information with synthetic values.
    </p>

    <form method="POST" enctype="multipart/form-data">

        <input
            type="file"
            name="file"
            accept=".docx"
            required
        >

        <br>

        <button type="submit">
            Redact Document
        </button>

    </form>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template_string(HTML)

    file = request.files.get("file")

    if not file or not file.filename:
        return "Please upload a DOCX file.", 400

    if not file.filename.lower().endswith(".docx"):
        return "Only DOCX files are supported.", 400

    with tempfile.TemporaryDirectory() as folder:

        input_path = os.path.join(
            folder,
            "input.docx"
        )

        output_path = os.path.join(
            folder,
            "redacted.docx"
        )

        file.save(input_path)

        redact_document(
            input_path,
            output_path
        )

        return send_file(
            output_path,
            as_attachment=True,
            download_name="Redacted_Document.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )