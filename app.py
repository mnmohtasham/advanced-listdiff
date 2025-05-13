from flask import Flask, render_template, request, send_file
import csv
import io

app = Flask("listdiff")

app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB limit

def process_lists(list_a, list_b, ignore_case, trim_spaces):
    if trim_spaces:
        list_a = [item.strip() for item in list_a]
        list_b = [item.strip() for item in list_b]

    if ignore_case:
        list_a = [item.lower() for item in list_a]
        list_b = [item.lower() for item in list_b]

    set_a = set(list_a)
    set_b = set(list_b)

    return {
        "intersection": set_a & set_b,
        "unique_to_a": set_a - set_b,
        "unique_to_b": set_b - set_a,
        "symmetric_difference": set_a ^ set_b
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

    # Define how to interpret separator
    sep_map = {
        "newline": "\n",
        "comma": ",",
        "tab": "\t",
        "space": " ",
        "semicolon": ";"
    }
    sep_char = sep_map.get(separator, "\n")

    list_a = raw_list_a.split(sep_char)
    list_b = raw_list_b.split(sep_char)

    results = process_lists(list_a, list_b, ignore_case, trim_spaces)
    return render_template('results.html', results=results)


@app.route('/upload', methods=['POST'])
def upload():
    file_a = request.files['file_a']
    file_b = request.files['file_b']
    ignore_case = 'ignore_case' in request.form
    trim_spaces = 'trim_spaces' in request.form

    # Read CSV files
    list_a = file_a.read().decode('utf-8').splitlines()
    list_b = file_b.read().decode('utf-8').splitlines()

    results = process_lists(list_a, list_b, ignore_case, trim_spaces)
    return render_template('results.html', results=results)

@app.route('/download', methods=['POST'])
def download():
    results = request.form.get('results')
    results = eval(results)  # Convert the string back to a dictionary

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Intersection'])
    writer.writerows([[item] for item in results['intersection']])
    writer.writerow([])
    writer.writerow(['Unique to List A'])
    writer.writerows([[item] for item in results['unique_to_a']])
    writer.writerow([])
    writer.writerow(['Unique to List B'])
    writer.writerows([[item] for item in results['unique_to_b']])
    writer.writerow([])
    writer.writerow(['Symmetric Difference'])
    writer.writerows([[item] for item in results['symmetric_difference']])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='comparison_results.csv'
    )

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)


