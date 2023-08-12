import json

def validate_json(json_data):
    try:
        data = json.loads(json_data)
        validated_data = []

        for item in data:
            if "name" in item and item["name"].startswith("a"):
                validated_data.append({"name": item["name"]})

        return {"validated_data": validated_data}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

# Example JSON data
json_data = '[{"abc":"1","name":"ascf"},{"abc":"6","name":"65"}]'

result = validate_json(json_data)
print(result)
