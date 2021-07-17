from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import subprocess, re

MOCKOUT="Init SSL without certificate database\n\
battery.charge: 100\n\
battery.voltage: 13.70\n\
battery.voltage.high: 13.00\n\
battery.voltage.low: 10.40\n\
battery.voltage.nominal: 12.0\n\
device.type: ups\n\
driver.name: blazer_usb\n\
driver.parameter.pollinterval: 2\n\
driver.parameter.port: auto\n\
driver.parameter.synchronous: no\n\
driver.version: 2.7.4\n\
driver.version.internal: 0.12\n\
input.current.nominal: 3.0\n\
input.frequency: 50.1\n\
input.frequency.nominal: 50\n\
input.voltage: 243.3\n\
input.voltage.fault: 243.3\n\
input.voltage.nominal: 230\n\
output.voltage: 243.3\n\
ups.beeper.status: disabled\n\
ups.delay.shutdown: 30\n\
ups.delay.start: 180\n\
ups.load: 9\n\
ups.productid: 5161\n\
ups.status: OL\n\
ups.type: offline / line interactive\n\
ups.vendorid: 0665\n"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historicdata.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    battCharge = db.Column(db.Float)
    battVolt = db.Column(db.Float)
    battVoltHigh = db.Column(db.Float)
    battVoltLow = db.Column(db.Float)
    battVoltNom = db.Column(db.Float)
    pollInterval = db.Column(db.Float)
    inputCurrNom = db.Column(db.Float)
    inputFreq = db.Column(db.Float)
    inputFreqNom = db.Column(db.Float)
    inputVolt = db.Column(db.Float)
    inputVoltNom = db.Column(db.Float)
    outputVolt = db.Column(db.Float)
    upsStatus = db.Column(db.String(25))

    def __repr__(self):
        return 'Value added for ' % self.timestamp
    

@app.route('/', methods=['GET'])
def main():
    output=subprocess.run(["ls", "-l"], capture_output=True, universal_newlines=True)
    print(re.findall("battery.charge.*", MOCKOUT))
    #print(output.returncode)
    #print(output.stdout)
    #print(MOCKOUT)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8080,host="localhost")