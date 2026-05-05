from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import os
from intervention_engine import send_department_email, trigger_whatsapp_blast
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'district_risk_classifier.pkl')
model = joblib.load(MODEL_PATH)
AUDIT_LOG = os.path.join(BASE_DIR, 'outputs', 'logs', 'intervention_audit.log')
def log_audit(msg):
    with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{msg}\n")
@app.route('/')
def home():
    """Serves the UI Dashboard"""
    return render_template('dashboard.html')
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    bcg = data['BCG']
    t_fi = data['T_FI_9_11']
    pop = data['POPULATION']
    asha = data['IS_ASHA']
    dropout_gap_percent = max(0, ((bcg - t_fi) / bcg) * 100) if bcg > 0 else 0
    asha_efficiency_ratio = (asha / pop) * 1000 if pop > 0 else 0
    features = pd.DataFrame([{
        'POPULATION': pop,
        'BCG': bcg,
        'IS_ASHA': asha,
        'dropout_gap_percent': dropout_gap_percent,
        'asha_efficiency_ratio': asha_efficiency_ratio
    }])
    prob = model.predict_proba(features)[0][1] # Probability of Class 1 (HIGH)
    ai_triggered = prob >= 0.45
    rule_triggered = dropout_gap_percent >= 50.0
    is_high_risk = ai_triggered or rule_triggered 
    district_name = data['district_name']
    actions = "None"
    if is_high_risk:
        stats = {
            'POPULATION': pop, 
            'BCG': bcg, 
            'IS_ASHA': asha, 
            'dropout_gap_percent': dropout_gap_percent
        }
        email_sent = send_department_email(district_name, stats, data['official_email'], prob)
        whatsapp_status = trigger_whatsapp_blast(district_name, data['phone_numbers'])
        trigger_source = "AI" if ai_triggered else "SAFETY RULE"
        actions = f"Email Alert {'Sent' if email_sent else 'Skipped'}, WhatsApp Blast ({whatsapp_status}) [{trigger_source}]"
        log_audit(f"TRIGGERED ({trigger_source}) | District: {district_name} | Prob: {prob:.2f} | Gap: {dropout_gap_percent:.1f}%")
    else:
        log_audit(f"SKIPPED | District: {district_name} | Prob: {prob:.2f} | Gap: {dropout_gap_percent:.1f}%")
    return jsonify({
        'risk_level': 'HIGH' if is_high_risk else 'LOW',
        'probability': float(prob),
        'actions_taken': actions
    })
if __name__ == '__main__':
    app.run(debug=True, port=5000)