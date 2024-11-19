from io import BytesIO

import pandas as pd
from flask import Flask, request, render_template, send_file

from . import get_records_for_pmids

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pmids = request.form['pmids'].split(',')
        merge = request.form.get('merge') == 'on'
        records = get_records_for_pmids(pmids, merge)
        df = pd.DataFrame(records)

        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return send_file(output, as_attachment=True, download_name="coa.xlsx",
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)