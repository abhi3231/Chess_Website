from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)

SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
          
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'my_creds.json', SCOPES)

client = gspread.authorize(creds)
spreadsheet = client.open_by_key('1_wQt-dMDQn9Rh6CmIf022xnPdivFsV4girsynwJfaRU')
worksheet = spreadsheet.worksheet("Player_Base") 
data = worksheet.get_all_values()
header = data[0]
body = data[1:]
df = pd.DataFrame(body, columns=header)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_value = request.form['search-input'].lower()
    filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_value).any(), axis=1)]
    if filtered_df.empty:
        error_message = "No results found"
        return render_template('index.html', error_message=error_message)
    else:
        return render_template('index.html', filtered_df=filtered_df.to_html(classes='table table-striped'))

if __name__ == '__main__':
    app.run()
