from flask import Flask, request, jsonify
from .math_utils import add_numbers, divide

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/sum")
    def sum_endpoint():
        data = request.get_json(silent=True) or {}
        nums = data.get("numbers", [])
        if not isinstance(nums, list):
            return jsonify(error="`numbers` must be a list"), 400
        try:
            result = add_numbers(nums)
        except (TypeError, ValueError):
            return jsonify(error="Invalid number in list"), 400
        return jsonify(result=result)

    @app.get("/divide")
    def divide_endpoint():
        a = request.args.get("a", None)
        b = request.args.get("b", None)
        if a is None or b is None:
            return jsonify(error="a and b are required"), 400
        try:
            a = float(a); b = float(b)
            result = divide(a, b)
        except ZeroDivisionError:
            return jsonify(error="division by zero"), 400
        except ValueError:
            return jsonify(error="invalid number"), 400
        return jsonify(result=result)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
