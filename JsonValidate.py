from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def validate_json(json_data):
    try:
        data = json.loads(json_data)
        validated_data = []

        for item in data:
            phone_key = next((key for key in item.keys() if key.lower() == 'phone'), None)
            if phone_key:
                if "phone" in item:
                    phone = item[phone_key]
                    phone = phone.replace(' ', '')  # Remove spaces

                    if phone.startswith('91') and len(phone) == 12:
                        phone = '+' + phone
                    elif not phone.startswith('+91') and len(phone) == 10:    #For start with +91
                        phone = '+91' + phone
                    
                    if len(phone) == 13:                #check length
                        validated_data.append({"phone": phone})
            
        return {"validated_data": validated_data}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

# Example JSON data
json_data = '[{"abc":"1","name":"ascf"},{"abc":"6","name":"65"}]'

result = validate_json(json_data)
print(result)

@app.route('/')
def home():
    return ("Welcome")

@app.route('/validate', methods=['POST'])
def validate_endpoint():
    json_data = request.data.decode('utf-8')
    result = validate_json(json_data)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)