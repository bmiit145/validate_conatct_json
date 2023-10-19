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

            df['phone'].drop_duplicates(inplace=True)
            
            # Apply validation rules to the 'phone' column
            mask = (
                ((df['phone'].str.startswith('91') & (df['phone'].str.len() == 12)) |
                (df['phone'].str.startswith('+91') & (df['phone'].str.len() == 13)))
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
