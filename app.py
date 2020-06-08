
import requests
import json
import csv
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

app = Flask(__name__)

app.debug = True

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

with open("output.csv",'w') as f:
  writer = csv.writer(f, delimiter=',')
  for item in data:
    for data_item in item['rates']:
      writer.writerow([data_item['currency'], data_item['code'], data_item['bid'], data_item['ask'] ])

@app.route('/', methods=['GET', 'POST'])
def dropdown():
    if request.method == 'GET':
      currencies = []
      for item in data:
          for data_item in item['rates']:
            currencies += [data_item['currency']] 
      for line in data:
         # print(line)
         data_source = 'This exchange rates apply on date: ' + item['effectiveDate'] + '. According to official NBP table no: '  + item['no']
         print(data)
         return render_template('index.html', currencies=currencies, data_source=data_source)
    
    elif request.method == 'POST':
      print("We received POST")
      print(request.form)
      result = request.form.get('currencies')
      resulta = request.form.get('currency_to_enter')
      # return redirect("/output.html")
      # return render_template("indexa.html")
      return redirect("/output.html")
      # print('currencies: ', currencies)    

@app.route("/output", methods = ["POST", "GET"])
def result():
    result = request.form.get('currency_to_enter')
    print("Currency to enter: ", result )
    resulta = request.form.get('currencies')
    print("Amount to enter ROW: ", resulta )
    currencies = []
    for item in data:
        for data_item in item['rates']:
          currencies += [data_item['currency']] 
        fx_chosen = currencies.index(resulta)
    print(currencies)  
    resultax = item['rates'][fx_chosen]['bid']
    output = resultax * int(result)
    return render_template("output.html", result=result, resulta=resulta, resultax=resultax, output=output)




if __name__ == "__main__":
    app.run()