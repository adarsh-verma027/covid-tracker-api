'''

REST API's to get latest coronavirus cases summary for one or more countries.

Method: GET
Endpoint: /coronavirus?country=India (for single country)
         /coronavirus?country=India,China (for multiple countries,  Note: country values are NOT case sensitive)
Response: {"data": [{
            "Active Cases": "462","Country": "China","New Cases": "+14","Total Cases": "91,732","Total Deaths": "4,636 ","Total Tests": "160,000,000"}
            ]}
'''


import requests
from bs4 import BeautifulSoup
from flask import Flask, request,jsonify

app = Flask(__name__)


@app.route('/coronavirus', methods=['GET'])
def get_covid_status():

    try:
        all_countries = [x.lower() for x in request.args.get('country').split(',')]

        res = requests.request("GET", "https://www.worldometers.info/coronavirus/")
        print(res.status_code)

        res_data = res.text
        soup = BeautifulSoup(res_data, "lxml")

        table_data = soup.find('table', id='main_table_countries_today')
        get_table_data = table_data.tbody.find_all('tr')


        response = list()

        for i in range(len(get_table_data)):
            dict_data = dict()
            try:
                key = get_table_data[i].find_all('a', href=True)[0].string
            except:
                key = get_table_data[i].find_all("td")[0].string

            if key and key.lower() in all_countries:
                values = [j.string for j in get_table_data[i].find_all('td')]
                dict_data['Country'] = key
                dict_data['Total Cases'] = values[2]
                dict_data['Active Cases'] = values[8]
                dict_data['New Cases'] = values[3]
                dict_data['Total Deaths'] = values[4]
                dict_data['Total Tests'] = values[12]

                response.append(dict_data)
        # print(response)
        if len(response) > 0:
            return jsonify({"data": response}),200
        return jsonify({'message': "No data found for requested country."})
    except Exception as e:
        return jsonify({'message': "Something went wrong."}), 500


if __name__ == '__main__':
    app.run()
