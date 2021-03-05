from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/seoul_art_center')
def seoul_art_center():
    return render_template('seoul_art_center.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)