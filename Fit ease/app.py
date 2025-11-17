from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    # Get height and weight safely
    try:
        height = float(request.form.get('height', 0))
        weight = float(request.form.get('weight', 0))
    except ValueError:
        return "Invalid input. Please enter numeric values.", 400

    if height <= 0 or weight <= 0:
        return "Height and weight must be positive numbers.", 400

    bmi = weight / (height * height)
    bmi_value = round(bmi, 2)

    # Determine category
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # Render diet selection page
    return render_template("diet_choice.html",
                           bmi=bmi_value,
                           category=category)


@app.route('/diet_chart', methods=['POST'])
def diet_chart():
    # Get form data
    diet_type = request.form.get('diet_type')
    category = request.form.get('category')
    bmi = request.form.get('bmi')

    # Ensure all data is present
    if not all([diet_type, category, bmi]):
        return "Missing form data. Please go back and select a diet.", 400

    # Render the diet chart template
    return render_template("diet_chart.html",
                           diet_type=diet_type,
                           category=category,
                           bmi=bmi)


if __name__ == '__main__':
    app.run(debug=True)
