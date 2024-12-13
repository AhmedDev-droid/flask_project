from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_crcl(age, weight, serum_creatinine, gender):
    if gender.lower() == 'male':
        k = 1.23
    elif gender.lower() == 'female':
        k = 1.04
    else:
        raise ValueError("Gender must be 'male' or 'female'.")

    crcl = ((140 - age) * weight * k) / serum_creatinine
    return crcl

def get_apixaban_dose(crcl, age, weight, serum_creatinine):
    if crcl < 15:
        return "Avoid use"
    elif 15 <= crcl <= 30:
        return "2.5 mg twice daily"
    else:
        risk_factors = 0
        if age >= 80:
            risk_factors += 1
        if weight <= 60:
            risk_factors += 1
        if serum_creatinine >= 1.5:
            risk_factors += 1

        if risk_factors >= 2:
            return "2.5 mg twice daily"
        else:
            return "5 mg twice daily"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            age = int(request.form["age"])
            weight = float(request.form["weight"])
            serum_creatinine = float(request.form["serum_creatinine"])
            unit = request.form["unit"]
            gender = request.form["gender"]

            # Convert serum creatinine if unit is mg/dL
            if unit == "mg/dL":
                serum_creatinine *= 88.4

            crcl = calculate_crcl(age, weight, serum_creatinine, gender)
            apixaban_dose = get_apixaban_dose(crcl, age, weight, serum_creatinine / 88.4)

            return render_template("result.html", crcl=crcl, apixaban_dose=apixaban_dose)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html", error=None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
