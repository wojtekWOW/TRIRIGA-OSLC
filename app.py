from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Endpoint and resource
endpoint = 'http://10.173.10.70:9080'
resource = '/oslc/so/PropIntegrationRecordCF'

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    spi_action = "Create"
    spi_wstPropertyID = request.form['spi_wstPropertyID']
    spi_wstPropertyNameTX = request.form['spi_wstPropertyNameTX']
    spi_triCountryCodeTX = request.form['spi_triCountryCodeTX']
    spi_triCountryTX = request.form['spi_triCountryTX']
    spi_triName = request.form['spi_triName']
    spi_triIdTX = request.form['spi_triIdTX']

    # Retrieve credentials from environment variables
    username = os.getenv('TRIRIGA_API_USERNAME')
    password = os.getenv('TRIRIGA_API_PASSWORD')

    if username is None or password is None:
        flash("API credentials are not set in environment variables")
        return redirect(url_for('index'))

    # Create payload
    payload = f"""{{
        "spi:Property": [
            {{
                "spi:action": "{spi_action}",
                "spi:wstPropertyID": "{spi_wstPropertyID}",
                "spi:wstPropertyNameTX": "{spi_wstPropertyNameTX}",
                "spi:triCountryCodeTX": "{spi_triCountryCodeTX}",
                "spi:triCountryTX": "{spi_triCountryTX}",
                "spi:triName": "{spi_triName}",
                "spi:triIdTX": "{spi_triIdTX}"
            }}
        ]
    }}"""

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Create REST request with POST method, endpoint, resource, headers, and payload
    response = requests.post(f"{endpoint}{resource}", headers=headers, data=payload, auth=(username, password))

    # Check response status
    if response.status_code == 201:
        flash("Request was successful")
    else:
        flash(f"Request failed with status code {response.status_code}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)