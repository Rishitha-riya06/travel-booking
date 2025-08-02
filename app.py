from flask import Flask, render_template, request, send_file
import psycopg2
import urllib.parse as up
import os
from fpdf import FPDF

app = Flask(__name__)

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    destination = request.form["destination"]
    date = request.form["date"]
    gender = request.form["gender"]

    cur.execute("INSERT INTO tickets (name, destination, date, gender) VALUES (%s, %s, %s, %s)",
                (name, destination, date, gender))
    conn.commit()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Travel Ticket", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Destination: {destination}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
    pdf.output("ticket.pdf")

    return send_file("ticket.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
