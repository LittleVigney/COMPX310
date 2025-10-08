import gradio as gr
import joblib
import pandas as pd

# Load trained pipeline
model = joblib.load("pipeline_model.joblib")

# Prediction function
def predict_income(age, workclass, fnlwgt, education, educational_num, marital_status,
                   occupation, relationship, race, gender, capital_gain, capital_loss,
                   hours_per_week, native_country):
    # Build input DataFrame (must match training column names exactly)
    X_new = pd.DataFrame([{
        "age": age,
        "workclass": workclass,
        "fnlwgt": fnlwgt,
        "education": education,
        "educational-num": educational_num,   # ✅ fixed
        "marital-status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "gender": gender,                     # ✅ fixed
        "capital-gain": capital_gain,
        "capital-loss": capital_loss,
        "hours-per-week": hours_per_week,
        "native-country": native_country
    }])
    
    prediction = model.predict(X_new)[0]
    return f"💰 Predicted Income: {prediction}"

# ================== UI ==================

# Header (same as the first version you liked)
header_html = """
<div style='background: linear-gradient(90deg, #1abc9c, #3498db); 
            padding: 20px; text-align: center; 
            color: white; border-radius: 8px;'>
  <h1 style='margin: 0; font-size: 2.2em;'>📊 Adult Income Prediction</h1>
  <p style='font-size: 1.1em;'>Fill in your details to predict whether annual income is >50K or <=50K</p>
</div>
"""

# Footer (same as the first version you liked)
footer_html = """
<div style='text-align:center; color:#7f8c8d; font-size: 0.9em; margin-top: 20px;'>
  Made with ❤️ using <b>Machine Learning</b> & <b>Gradio</b>
</div>
"""

# Custom button style
custom_css = """
#predict-btn {
    background: linear-gradient(90deg, #3498db, #1abc9c) !important;
    color: white !important;
    font-weight: bold;
    border-radius: 10px;
    transition: 0.3s ease-in-out;
}
#predict-btn:hover {
    background: linear-gradient(90deg, #1abc9c, #3498db) !important;
    transform: scale(1.05);
}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.HTML(header_html)

    with gr.Row():
        with gr.Column():
            age = gr.Number(label="🎂 Age", value=30)
            workclass = gr.Dropdown(
                ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", 
                 "Local-gov", "State-gov", "Without-pay", "Never-worked"],
                label="💼 Workclass"
            )
            fnlwgt = gr.Number(label="📊 Final Weight (fnlwgt)", value=100000)
            education = gr.Dropdown(
                ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", 
                 "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "1st-4th", 
                 "10th", "Doctorate", "5th-6th", "Preschool"],
                label="🎓 Education"
            )
            educational_num = gr.Number(label="🎓 Education (numeric)", value=10)

        with gr.Column():
            marital_status = gr.Dropdown(
                ["Married-civ-spouse", "Divorced", "Never-married", "Separated", 
                 "Widowed", "Married-spouse-absent", "Married-AF-spouse"],
                label="💍 Marital Status"
            )
            occupation = gr.Dropdown(
                ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", 
                 "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", 
                 "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"],
                label="🛠️ Occupation"
            )
            relationship = gr.Dropdown(
                ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"],
                label="👪 Relationship"
            )
            race = gr.Dropdown(
                ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"],
                label="🌎 Race"
            )
            gender = gr.Dropdown(["Male", "Female"], label="⚧ Gender")   # ✅ fixed

        with gr.Column():
            capital_gain = gr.Number(label="📈 Capital Gain", value=0)
            capital_loss = gr.Number(label="📉 Capital Loss", value=0)
            hours_per_week = gr.Number(label="⏰ Hours per Week", value=40)
            native_country = gr.Dropdown(
                ["United-States", "Mexico", "Philippines", "Germany", "Canada", 
                 "India", "England", "China", "Puerto-Rico", "Other"],
                label="🌍 Native Country"
            )
            predict_btn = gr.Button("🚀 Predict Income", elem_id="predict-btn")

    output = gr.Textbox(label="✨ Prediction", placeholder="Prediction will appear here", interactive=False)

    gr.HTML(footer_html)

    predict_btn.click(
        fn=predict_income,
        inputs=[age, workclass, fnlwgt, education, educational_num, marital_status,
                occupation, relationship, race, gender, capital_gain, capital_loss,
                hours_per_week, native_country],
        outputs=output
    )

demo.launch()
