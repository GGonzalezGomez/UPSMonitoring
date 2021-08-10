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
        return '{{id: {:d}, timestamp: {:%Y-%m-%d %H:%M:%S}, battCharge: {:.2f}, battVolt: {:.2f}, battVoltHigh: {:.2f}, battVoltLow: {:.2f}, battVoltNom: {:.2f}, pollInterval: {:.1f}, inputCurrNom: {:.2f}, inputFreq: {:.2f}, inputFreqNom: {:.2f}, inputVolt: {:.2f}, inputVoltNom: {:.2f}, outputVolt: {:.2f}, upsStatus: {:s} }}'.format(self.id, 
                self.timestamp, self.battCharge, self.battVolt, self.battVoltHigh, self.battVoltLow, self.battVoltNom, self.pollInterval, self.inputCurrNom, self.inputFreq, self.inputFreqNom, self.inputVolt, self.inputVoltNom, self.outputVolt, self.upsStatus)
    


class Record(Resource):
    def get(self, identifier):
        pass
    def post(self, identifier):
        pass
    def delete(self, identifier):
        pass

class RecordList(Resource):
    def get(self):
        tasks = Todo.query.order_by(Todo.timestamp).all()
        print(tasks)
        return "Hello world"
    def post(self):
        print(request.form['Input Voltage'])
        new_task = Todo(battCharge=request.form['Battery Charge'], battVolt=request.form['Battery Voltage'], battVoltHigh=request.form['Battery Voltage High'], battVoltLow=request.form['Battery Voltage Low'], 
                        battVoltNom=request.form['Battery Voltage Nominal'], pollInterval=request.form['Polling interval'], inputCurrNom=request.form['Input Current Nominal'], inputFreq=request.form['Input Frequency'], 
                        inputFreqNom=request.form['Input Frequency Nominal'], inputVolt=request.form['Input Voltage'], inputVoltNom=request.form['Input Voltage Nominal'], outputVolt=request.form['Output Voltage'], 
                        upsStatus=request.form['UPS Status'])

        try:
            db.session.add(new_task)
            db.session.commit()
            return 'Successful'
        except:
            return 'There was an issue adding your task'
        pass

@app.route('/', methods=['GET'])
def main():
    #output=subprocess.run(["ls", "-l"], capture_output=True, universal_newlines=True)
    print(re.findall("battery.charge.*", MOCKOUT))
    return render_template('index.html',keyvalues=fields)

if __name__ == "__main__":
    api.add_resource(RecordList, '/records')
    api.add_resource(Record, '/record/<string:identifier>')
    app.run(port=8080,host="localhost")



# curl --location --request POST 'http://localhost:8080/records' \
# --form 'jander="clander"' \
# --form 'Battery Charge="100"' \
# --form 'Battery Voltage="13.70"' \
# --form 'Battery Voltage High="13.00"' \
# --form 'Battery Voltage Low="10.40"' \
# --form 'Battery Voltage Nominal="12.00"' \
# --form 'Polling interval="2"' \
# --form 'Input Current Nominal="3.0"' \
# --form 'Input Frequency="50.1"' \
# --form 'Input Frequency Nominal="50"' \
# --form 'Input Voltage="243.3"' \
# --form 'Input Voltage Nominal="230"' \
# --form 'Output Voltage="243.3"' \
# --form 'UPS Status="OL"'