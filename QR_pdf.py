import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

st.title("DFX QR Code Generator")
st.subheader("High-Resolution PDF Output for Print")

# User Input
url = st.text_input("Enter the URL or text for the Mailer:", "https://example.com")
fill = st.color_picker("Pick a QR Color", "#000000")
back = st.color_picker("Pick a Background Color", "#FFFFFF")

def generate_qr_pdf(data, fg_color, bg_color):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    
    # 1. Setup Colors
    fill_color = colors.HexColor(fg_color)
    back_color = colors.HexColor(bg_color)
    
    # 2. Create the QR Widget
    qr_code = qr.QrCodeWidget(data)
    qr_code.barFillColor = fill_color  # This attribute is standard
    
    # 3. Handle Scaling
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    size = 200 
    
    # 4. Draw Background Rectangle on the Canvas
    # Position: x=200, y=400 (matches where we draw the QR)
    c.setFillColor(back_color)
    c.rect(200, 400, size, size, fill=1, stroke=0)
    
    # 5. Draw the QR Code on top
    d = Drawing(size, size, transform=[size/width, 0, 0, size/height, 0, 0])
    d.add(qr_code)
    renderPDF.draw(d, c, 200, 400) 
    
    c.showPage()
    c.save()
    return buf.getvalue()

if st.button("Generate Print-Ready PDF"):
    pdf_data = generate_qr_pdf(url, fill, back)
    
    st.success("QR Code rendered as a Vector PDF!")
    
    # Download button for the PDF
    st.download_button(
        label="Download High-Res PDF",
        data=pdf_data,
        file_name="mailer_qr_code.pdf",
        mime="application/pdf"
    )