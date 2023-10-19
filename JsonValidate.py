import re
from flask import Flask, request, jsonify
import pandas as pd
import json


app = Flask(__name__)

def validate_json(json_data):
    try:
        data = json.loads(json_data)

        # Create a Pandas DataFrame from the JSON data
        df = pd.DataFrame(data)

        # Ensure 'phone' column exists
        if 'phone' in df.columns:
            # Convert the 'phone' column to strings
            df['phone'] = df['phone'].astype(str)

            # Remove spaces from the 'phone' column
            df['phone'] = df['phone'].str.replace(' ', '')

            # give unique only
            df.drop_duplicates(subset=['phone'], keep='first', inplace=True)

            # Add country code prefix to phone numbers
            df['phone'] = df['phone'].apply(lambda phone: '+' + phone if phone.startswith('91') and len(phone) == 12 else ('+91' + phone if not phone.startswith('+91') and len(phone) == 10 else phone))
            
            # Apply validation rules to the 'phone' column
            mask = (
                df['phone'].apply(lambda phone: bool(re.match(r'^\+?91\d{10}$', phone))) |
                df['phone'].apply(lambda phone: bool(re.match(r'^\+\d{12}$', phone)))
            )

            # Create a new DataFrame with valid phone numbers
            validated_data = df[mask]

            # Convert the valid phone numbers to a list of dictionaries
            validated_data = validated_data.to_dict(orient='records')

            return {"validated_data": validated_data}
        else:
            return {"error": "No 'phone' key found in JSON data"}

    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}


json_data = '[{"phone":"1","name":"ascf"},{"phone":"6","name":"65"}]'

result = validate_json(json_data)
print(result)


@app.route('/')
def home():
    return "Welcome"

@app.route('/validate', methods=['POST'])
def validate_endpoint():
    json_data = request.data.decode('utf-8')
    result = validate_json(json_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
