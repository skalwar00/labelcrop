from flask import Flask, request, send_file, render_template
import PyPDF2
import io

app = Flask(__name__)

# Fixed crop coordinates
X = 187
Y = 461
W = 218
H = 358

def crop_pdf(input_pdf):
    output_pdf = io.BytesIO()
    pdf_reader = PyPDF2.PdfReader(input_pdf)
    pdf_writer = PyPDF2.PdfWriter()
    
    for page in pdf_reader.pages:
        # Set the new media box based on fixed crop coordinates
        page.mediabox.lower_left = (X, Y)
        page.mediabox.upper_right = (X + W, Y + H)
        
        pdf_writer.add_page(page)
    
    pdf_writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        cropped_pdf = crop_pdf(file)
        return send_file(cropped_pdf, as_attachment=True, download_name='cropped.pdf')

if __name__ == '__main__':
    app.run(debug=True)
