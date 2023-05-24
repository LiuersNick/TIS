from flask import Flask, render_template, url_for, request
from D_search_pipeline import search

app = Flask(__name__)

@app.route('/', methods=['get', 'post'])
def main_page():
    return render_template('homepage.html')

@app.route('/search', methods=['post', 'get'])
def search_page():
    get_data = request.args.to_dict()
    paths = search(get_data['input_text'])
    labels = []
    for path in paths:
        label = path.split('/')[-2]
        labels.append(label)
    i=0
    output = []
    while i < 5:
        pair = []
        pair.append(labels[i])
        path_ = '.' + paths[i][18:]
        pair.append(path_)
        output.append(pair)
        i += 1
    print(output)
    
    inputs = get_data['input_text']
    return render_template('homepage_search.html', inputs=inputs, output=output)