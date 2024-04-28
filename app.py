import pickle
import numpy as np
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

options = {
    "How often do you feel sad?": ['Usually', 'Sometimes', 'Seldom', 'Most-Often'],
    "How often do you feel euphoric?": ['Seldom', 'Most-Often', 'Usually', 'Sometimes'],
    "How often do you feel exhausted?": ['Sometimes', 'Usually', 'Seldom', 'Most-Often'],
    "How often do you have difficulty in sleeping?": ['Sometimes', 'Most-Often', 'Usually', 'Seldom'],
    "Mood Swing": ['YES', 'NO'],
    "Suicidal thoughts": ['YES', 'NO'],
    "Anorexia": ['NO', 'YES'],
    "Authority Respect": ['NO', 'YES'],
    "Try-Explanation": ['YES', 'NO'],
    "Aggressive Response": ['NO', 'YES'],
    "Ignore & Move-On": ['NO', 'YES'],
    "Nervous Break-down": ['YES', 'NO'],
    "Admit Mistakes": ['YES', 'NO'],
    "Overthinking": ['YES', 'NO'],
    "Sexual Activity": ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    "Concentration": ['1', '2', '3', '4', '5', '6', '7', '8'],
    "Optimisim": ['1', '2', '3', '4', '5', '6', '7', '8', '9']
}

@app.route('/', methods=['GET'])
def home():
    return render_template('options.html', options=options)

@app.route('/output', methods=['POST'])
def output():
    if request.method == 'POST':
        form_data = {key: request.form[key] for key in request.form}

        print("form data:", form_data)
        
        form_data_values = []
        for key in form_data.keys():
            form_data_values.append(form_data[key])
        print("form data values:", form_data_values)
        
        responses = []
        for val in form_data_values:
            if val == 'Most-Often':
                responses.append(4)
            elif val == 'Usually':
                responses.append(3)
            elif val == 'Sometimes':
                responses.append(2)
            elif val == 'Seldom' or val == 'YES':
                responses.append(1)
            elif val == 'NO':
                responses.append(0)
            else:
                responses.append(int(val))
        #responses = [response.tolist() if isinstance(response, np.ndarray) else response for response in responses]
        print("responses: ",responses)
        '''
        for key in form_data_encoded.keys():
            responses.append(form_data_encoded[key])
        
        responses_hashable = []
        for response in responses:
            if isinstance(response, np.ndarray):
                responses_hashable.append(response.tolist())
            else:
                responses_hashable.append(response)
        '''
    
        #input_values = pd.DataFrame([responses_hashable], columns=list(form_data.keys()))
        input_values = np.array(responses).reshape(1,-1)

        print(input_values)

        output_mapping = {0: 'Bipolar Type-1', 1: 'Bipolar Type-2', 2: 'Depression', 3: 'Normal'}

        model = pickle.load(open('model.pkl','rb'))
        pred = model.predict(input_values)
        
        print(form_data)
        return render_template('output.html', form_data=form_data, result = output_mapping[pred[0]])

if __name__ == '__main__':
    app.run(debug=True)
