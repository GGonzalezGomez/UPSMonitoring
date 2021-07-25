from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import subprocess, re
from flask_restful import Resource, Api, reqparse

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
api = Api(app)

fields = ["Battery Charge","Battery Voltage","Battery Voltage High","Battery Voltage Low", \
          "Battery Voltage Nominal","Polling interval","Input Current Nominal", \
          "Input Frequency","Input Frequency Nominal","Input Voltage","Input Voltage Nominal", \
          "Output Voltage","UPS Status","Input Voltage Fault","UPS load"]

class Record(db.Model):
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
    inputVoltFault = db.Column(db.Float)
    inputVoltNom = db.Column(db.Float)
    outputVolt = db.Column(db.Float)
    upsLoad = db.Column(db.Float)
    upsStatus = db.Column(db.String(25))

    def __repr__(self):
        return 'Value added for ' % self.timestamp
    


class Record(Resource):
    def get(self, identifier):
        pass
    def post(self, identifier):
        pass
    def delete(self, identifier):
        pass

class RecordList(Resource):
    def get(self):
        return "Hello world"
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('battery.charge', type=float)
        parser.add_argument('battery.voltage', type=float)
        parser.add_argument('battery.voltage.high', type=float)
        parser.add_argument('battery.voltage.low', type=float)
        parser.add_argument('battery.voltage.nominal', type=float)
        parser.add_argument('driver.parameter.pollinterval', type=float)
        parser.add_argument('input.current.nominal', type=float)
        parser.add_argument('input.frequency', type=float)
        parser.add_argument('input.frequency.nominal', type=float)
        parser.add_argument('input.voltage', type=float)
        parser.add_argument('input.voltage.fault', type=float)
        parser.add_argument('input.voltage.nominal', type=float)
        parser.add_argument('output.voltage', type=float)
        parser.add_argument('ups.load', type=float)
        parser.add_argument('ups.status', type=str)
        args = parser.parse_args()

        new_record = Record(battCharge=args['battery.charge'],
            battVolt=args['battery.voltage'],
            battVoltHigh=args['battery.voltage.high'],
            battVoltLow=args['battery.voltage.low'],
            battVoltNom=args['battery.voltage.nominal'],
            pollInterval=args['driver.parameter.pollinterval'],
            inputCurrNom=args['input.current.nominal'],
            inputFreq=args['input.frequency'],
            inputFreqNom=args['input.frequency.nominal'],
            inputVolt=args['input.voltage'],
            inputVoltFault=args['input.voltage.fault'],
            inputVoltNom=args['input.voltage.nominal'],
            outputVolt=args['output.voltage'],
            upsLoad=args['ups.load'],
            upsStatus=args['ups.status'])

        #try:
            #db.session.add()
        return {'status': 'success'}, 201

@app.route('/', methods=['GET'])
def main():
    #output=subprocess.run(["ls", "-l"], capture_output=True, universal_newlines=True)
    print(re.findall("battery.charge.*", MOCKOUT))
    return render_template('index.html',keyvalues=fields)

if __name__ == "__main__":
    api.add_resource(RecordList, '/records')
    api.add_resource(Record, '/record/<string:identifier>')
    app.run(port=8080,host="localhost")



# curl -X POST \
#   http://localhost:8080/records \
#   -H 'Content-Type: application/json' \
#   -H 'Postman-Token: 361994f4-8430-444f-9d60-ed5376d4b7cd' \
#   -H 'cache-control: no-cache' \
#   -d '{ "this": 2,
#   "that": 4
# }'