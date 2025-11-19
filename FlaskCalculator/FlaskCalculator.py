from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Standard calculator endpoint supporting basic arithmetic only."""
    try:
        data = request.get_json()
        operation = data.get('operation')

        if operation not in ['add', 'subtract', 'multiply', 'divide', 'cos']:
            return jsonify({'error': 'Invalid operation'}), 400

        # Validate required numbers
        try:
            num1 = float(data.get('num1'))
            # num2 is optional for single-argument operations like cos
            if operation in ['cos']:
                num2 = None
            else:
                num2 = float(data.get('num2'))
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid input'}), 400

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return jsonify({'error': 'Cannot divide by zero'}), 400
            result = num1 / num2
        elif operation == 'cos':
            result = math.cos(num1)
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        return jsonify({'result': result})
    except OverflowError:
        return jsonify({'error': 'Result too large'}), 400
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero error'}), 400


if __name__ == '__main__':
    app.run(debug=True)
