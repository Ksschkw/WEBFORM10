from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pygsheets
import pandas as pd
import csv

app = Flask(__name__)
CORS(app)

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()

    # Insert form data into SQLite database
    conn = sqlite3.connect('form_data.db')
    c = conn.cursor()

    c.execute('''INSERT INTO form_entries 
                 (first_name, last_name, email, age, dob, address, city, state, zip, phone)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                 (data['firstName'], data['lastName'], data['email'], data['age'], data['dob'], 
                 data['address'], data['city'], data['state'], data['zip'], data['phone']))
    conn.commit()
    print("Data submitted successfully")

    # Fetch all data from the users table
    c.execute('SELECT * FROM form_entries')
    rows = c.fetchall()
    # Specify the file name
    csv_file = 'users_data.csv'
    # Write the data to a CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(['id', 'firstName', 'lastName', 'email','age','dob', 'address','city','state','zip', 'phone'])
        # Write the data
        writer.writerows(rows)

    print(f"Data has been exported to {csv_file}")
    # Authorize and open the Google Sheets document
    gc = pygsheets.authorize(service_file='CIT_306_ASSIGNMENT\okaforcit306-b20877ce96db.json')
    spreadsheet = gc.open('CIT306FormData')

    # Select the first sheet in the spreadsheet
    sheet = spreadsheet[0]

    # Load your CSV data into a pandas DataFrame
    df = pd.read_csv('users_data.csv')

    # Clear the existing content in the sheet
    sheet.clear()

    # Update the sheet with the DataFrame content
    sheet.set_dataframe(df, (1, 1))  # Starting at cell (1, 1)

    print("Data has been uploaded to Google Sheets")
    # Close the database connection

    conn.close()
    return jsonify({'message': 'Data saved successfully!'})
    

if __name__ == '__main__':
    app.run(debug=True)