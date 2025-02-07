from flask import Flask, request, jsonify
import requests
import math

app = Flask(__name__)

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is a perfect number
def is_perfect(n):
    if n < 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    if n == 0:  # Ensure 0 is NOT classified as Armstrong
        return False
    digits = [int(d) for d in str(abs(int(n)))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(int(n))

# Function to get fun fact from Numbers API
def get_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        return response.json().get("text", "No fun fact available.")
    except:
        return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num_param = request.args.get('number')

    try:
        num = float(num_param)  # Allow floating-point numbers
        num_int = int(num)

        properties = []
        if is_armstrong(num_int):
            properties.append("armstrong")
        properties.append("even" if num_int % 2 == 0 else "odd")

        response = {
            "number": int(num) if num.is_integer() else num,  # Return integer if no decimal part
            "is_prime": is_prime(num_int),
            "is_perfect": is_perfect(num_int),
            "properties": properties,
            "digit_sum": sum(int(d) for d in str(abs(num_int))),  # Ignore negative sign
            "fun_fact": get_fun_fact(num_int)
        }
        return jsonify(response), 200

    except ValueError:
        return jsonify({"number": num_param, "error": True}), 400

if __name__ == '__main__':
    app.run(debug=True)
