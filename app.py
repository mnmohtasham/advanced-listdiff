from flask import Flask, render_template, request, send_file
import csv
import io
from collections import Counter
import json

app = Flask("listdiff")

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit
ALLOWED_EXTENSIONS = {'txt', 'csv'}

def process_lists(list_a, list_b, ignore_case, trim_spaces):
    if trim_spaces:
        list_a = [item.strip() for item in list_a]
        list_b = [item.strip() for item in list_b]

    if ignore_case:
        list_a = [item.lower() for item in list_a]
        list_b = [item.lower() for item in list_b]

    # Calculate duplicates on the normalized lists. This is the correct logic.
    duplicates_a = [item for item, count in Counter(list_a).items() if count > 1]
    duplicates_b = [item for item, count in Counter(list_b).items() if count > 1]
    set_a = set(list_a)
    set_b = set(list_b)
    return {
        "intersection": sorted(list(set_a & set_b)),
        "unique_to_a": sorted(list(set_a - set_b)),
        "unique_to_b": sorted(list(set_b - set_a)),
        "symmetric_difference": sorted(list(set_a ^ set_b)),
        "union": sorted(list(set_a | set_b)),
        "duplicates_a": sorted(duplicates_a),
        "duplicates_b": sorted(duplicates_b)
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    raw_list_a = request.form.get('list_a', '')
    raw_list_b = request.form.get('list_b', '')
    separator = request.form.get('separator', 'newline')
    ignore_case = 'ignore_case' in request.form
    trim_spaces = 'trim_spaces' in request.form

    sep_map = {"newline": "\n", "comma": ",", "tab": "\t", "space": " ", "semicolon": ";"}
    sep_char = sep_map.get(separator, "\n")

    list_a = [item for item in raw_list_a.split(sep_char) if item]
    list_b = [item for item in raw_list_b.split(sep_char) if item]

    results = process_lists(list_a, list_b, ignore_case, trim_spaces)
    
    return render_template(
        'results.html', 
        results=results, 
        results_json=json.dumps(results)
    )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    file_a = request.files['file_a']
    file_b = request.files['file_b']
    
    if not file_a or not allowed_file(file_a.filename) or \
       not file_b or not allowed_file(file_b.filename):
        return "Invalid file type. Please upload .txt or .csv files.", 400
    
    ignore_case = 'ignore_case' in request.form
    trim_spaces = 'trim_spaces' in request.form

    list_a = [line for line in file_a.read().decode('utf-8').splitlines() if line]
    list_b = [line for line in file_b.read().decode('utf-8').splitlines() if line]

    results = process_lists(list_a, list_b, ignore_case, trim_spaces)

    return render_template(
        'results.html', 
        results=results, 
        results_json=json.dumps(results)
    )

@app.route('/download', methods=['POST'])
def download():
    results_json_str = request.form.get('results_json')
    if not results_json_str:
        return "No results to download", 400
        
    results = json.loads(results_json_str)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['Intersection'])
    writer.writerows([[item] for item in results.get('intersection', [])])
    writer.writerow([])
    writer.writerow(['Unique to List A'])
    writer.writerows([[item] for item in results.get('unique_to_a', [])])
    writer.writerow([])
    writer.writerow(['Unique to List B'])
    writer.writerows([[item] for item in results.get('unique_to_b', [])])
    writer.writerow([])
    writer.writerow(['Symmetric Difference'])
    writer.writerows([[item] for item in results.get('symmetric_difference', [])])
    writer.writerow([])
    writer.writerow(['All Unique Items (Union)'])
    writer.writerows([[item] for item in results.get('union', [])])
    writer.writerow([])
    writer.writerow(['Duplicates in List A'])
    writer.writerows([[item] for item in results.get('duplicates_a', [])])
    writer.writerow([])
    writer.writerow(['Duplicates in List B'])
    writer.writerows([[item] for item in results.get('duplicates_b', [])])

    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='comparison_results.csv'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


