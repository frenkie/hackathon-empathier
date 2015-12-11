# hackathon-empathier
Story audioliser and visualiser

## install

Do an `npm install` for installing all prerequisites.

Adjust the OSC clients in `python-tracker/PythonTracker.py`.

## running

### server + speech recognizer
`npm start`

Navigate to [localhost:8080/speech-analyser/](http://localhost:8080/speech-analyser/)
to start recording (Dutch) speech. Adjust the recognition.lang variable
in the code if you want to translate different speech.

### FaceReader
Run the `python-tracker/PythonTracker.py` script on the FaceReader machine.

