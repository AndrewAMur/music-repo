from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Load dataset from CSV file
def load_dataset():
    dataset = []
    with open('dataset.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dataset.append(row)
    return dataset

# Search function to find songs by various criteria
def search(query, search_type, dataset):
    if search_type == 'artist':
        return [song for song in dataset if query.lower() in song['artists'].lower()]
    elif search_type == 'album':
        return [song for song in dataset if query.lower() in song['album_name'].lower()]
    elif search_type == 'genre':
        return [song for song in dataset if query.lower() in song['track_genre'].lower()]
    elif search_type == 'song':
        return [song for song in dataset if query.lower() in song['track_name'].lower()]
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    dataset = load_dataset()
    if request.method == 'POST':
        query = request.form['query'].strip()
        search_type = request.form['search_type']
        results = search(query, search_type, dataset)
        return render_template('results.html', results=results, query=query, search_type=search_type)
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
