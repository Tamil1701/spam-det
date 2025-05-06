from flask import Flask, render_template, request, redirect, url_for, flash
import joblib
import os
import email
from email.header import decode_header
import imaplib
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '123989'
CORS(app, supports_credentials=True)

# Pretrained model and vectorizer paths
MODEL_PATH = "spam_model.pkl"
VECTORIZER_PATH = "count_vectorizer.pkl"

clf = joblib.load(MODEL_PATH)
cv = joblib.load(VECTORIZER_PATH)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Gmail credentials
EMAIL = "tamilarasanselvam1701@gmail.com"
APP_PASSWORD = "vuqp ywki rpla mmda"

@app.after_request
def add_csp(response):
    response.headers['Content-Security-Policy'] = "frame-ancestors *"
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    message = request.form.get('message', '').strip()
    if message:
        vect = cv.transform([message])
        prediction = clf.predict(vect)[0]
        label = "Spam" if prediction == 1 else "Not Spam"
        return render_template('index.html', prediction=label, message=message)
    flash('Please enter a message to classify.', 'error')
    return redirect(url_for('home'))

@app.route('/upload_eml', methods=['POST'])
def upload_eml():
    file = request.files.get('eml_file')
    if not file or file.filename == '':
        flash('No selected file.', 'error')
        return redirect(url_for('home'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filepath)

    with open(filepath, 'rb') as f:
        msg = email.message_from_binary_file(f)

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    vect = cv.transform([body])
    prediction = clf.predict(vect)[0]
    label = "Spam" if prediction == 1 else "Not Spam"
    return render_template('index.html', prediction=label, message=body.strip())

@app.route('/fetch_emails')
def fetch_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        email_ids = data[0].split()[-10:]  # Last 10 emails
        email_ids.reverse()  # Newest to oldest

        results = []
        for e_id in email_ids:
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = msg.get("Subject", "No Subject")
            decoded_subject, encoding = decode_header(subject)[0]
            if isinstance(decoded_subject, bytes):
                subject = decoded_subject.decode(encoding or "utf-8", errors="ignore")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            vect = cv.transform([body])
            prediction = clf.predict(vect)[0]
            label = "Spam" if prediction == 1 else "Not Spam"

            results.append({
                'subject': subject,
                'body': body.strip(),
                'prediction': label
            })

        return render_template("index.html", emails=results)

    except Exception as e:
        flash(f"Error fetching emails: {str(e)}", "error")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
