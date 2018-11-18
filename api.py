import pickle
from sklearn.externals import joblib
# from boto.s3.key import Key
# from boto.s3.connection import S3Connection
from flask import Flask
from flask import request
from flask import json

BUCKET_NAME = 'heavywaterinc'
MODEL_FILE_NAME = 'model.pkl'
tfidf_words = 'tfidf.pkl'
MODEL_LOCAL_PATH = MODEL_FILE_NAME

app = Flask(__name__)

@app.route('/')
def indextest():
    print("Test Successful")
    return("Test Successful")
@app.route('/ml-api/')
def index():
    # payload = json.loads(request.get_data().decode('utf-8'))
    # Get request for the name words
    test = request.args.get('words')
    print (test)
    payload_2 = [test]

    result = {}
    prediction, probability, classes = predict(payload_2)
    max_prob = 0
    for i, j in zip(classes, probability[0]):
        max_prob = max(max_prob, j)
        if j == max_prob:
            result['class'] = i
        result[i] = j * 100
    data = {'Prediction': prediction, 'Confidence': result}
    return json.dumps(data)


def load_ml_model():
    # Connect with the AWS s3 and save the model in the model path
    # conn = S3Connection()
    # bucket = conn.create_bucket(BUCKET_NAME)
    # key_obj = Key(bucket)
    # key_obj.key = MODEL_FILE_NAME

    # contents = key_obj.get_contents_to_filename(MODEL_LOCAL_PATH)
    ml_model = joblib.load(MODEL_LOCAL_PATH)
    return ml_model


def predict(data):
    # Predictions the trained ml model
    f=open(tfidf_words, "rb")
    tfidf_vec = pickle.load(f)
    #tfidf_vec.fit(data)
    processed_data = tfidf_vec.transform(data)
    ml_model = load_ml_model()
    classes = ml_model.classes_
    prediction = ml_model.predict(processed_data)
    return prediction[0], ml_model.predict_proba(processed_data), classes
