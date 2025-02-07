from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def is_armstrong(num):
    digits = [int(d) for d in str(num)]
    power = len(digits)
    return sum(d ** power for d in digits) == num

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num = request.args.get('number')
    
    if not num or not num.isdigit():
        return jsonify({"number": num, "error": True}), 400
    
    num = int(num)
    properties = ["odd" if num % 2 else "even"]
    
    if is_armstrong(num):
        properties.insert(0, "armstrong")

    digit_sum = sum(int(d) for d in str(num))
    
    fun_fact_url = f"http://numbersapi.com/{num}/math?json"
    fun_fact = requests.get(fun_fact_url).json().get("text", "No fact available.")
    
    response = {
        "number": num,
        "is_prime": num > 1 and all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)),
        "is_perfect": num == sum(i for i in range(1, num) if num % i == 0),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
