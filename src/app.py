from flask import Flask, request, jsonify

app = Flask(__name__)

def trial_division(n):
    if n <= 1:
        return []
    
    factors = []
    
    # Handle 2 separately
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    p = 3
    while p * p <= n:
        while n % p == 0:
            factors.append(p)
            n //= p
        p += 2
    if n > 1:
        factors.append(n)
    
    return factors

@app.route('/')
def home():
    return jsonify({
        "message": "Flask Factoring API",
        "endpoints": {
            "/factor/<int>": "GET - Returns prime factors of the integer",
            "/factor": "POST - Send {\"number\": <int>} to get factors"
        }
    })

@app.route('/factor/<int:num>', methods=['GET'])
def factor_get(num):
    if num < 0:
        return jsonify({"error": "Please provide a non-negative integer"}), 400
    
    factors = trial_division(num)
    
    return jsonify({
        "number": num,
        "factors": factors,
        "is_prime": len(factors) == 1 and factors[0] == num if factors else False
    })

@app.route('/factor', methods=['POST'])
def factor_post():
    data = request.get_json()
    
    if not data or 'number' not in data:
        return jsonify({"error": "Please provide a 'number' field in JSON"}), 400
    
    try:
        num = int(data['number'])
        if num < 0:
            return jsonify({"error": "Please provide a non-negative integer"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid number format"}), 400
    
    factors = trial_division(num)
    
    return jsonify({
        "number": num,
        "factors": factors,
        "is_prime": len(factors) == 1 and factors[0] == num if factors else False
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)