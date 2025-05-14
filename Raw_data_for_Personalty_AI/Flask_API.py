from flask import Flask, request, jsonify
import joblib
import numpy as np

# Load models and scaler
scaler = joblib.load('scaler.pkl')
models = {
    'Extraversion': joblib.load('Extraversion_model.pkl'),
    'Agreeableness': joblib.load('Agreeableness_model.pkl'),
    'Openness': joblib.load('Openness_model.pkl'),
    'Conscientiousness': joblib.load('Conscientiousness_model.pkl'),
    'Neuroticism': joblib.load('Neuroticism_model.pkl')
}

# Questions mapping for traits
questions_mapping = {
    "Openness": [
        "How do you typically approach new situations?",
        "When solving problems, how do you prefer to think?"
    ],
    "Conscientiousness": [
        "How do you approach deadlines and schedules?",
        "How do you maintain your personal space?"
    ],
    "Extraversion": [
        "In group settings, how do you typically behave?",
        "How do you recharge after a long day?"
    ],
    "Agreeableness": [
        "When someone disagrees with you, how do you respond?",
        "How do you handle others' emotional needs?"
    ],
    "Neuroticism": [
        "How do you handle unexpected changes?",
        "Before important events, how do you feel?"
    ]
}

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON input
    data = request.json
    user_answers = data.get('answers')  # Expecting a dictionary of trait answers

    # Validate input
    if not user_answers or len(user_answers) != len(models):
        return jsonify({'error': 'Invalid input data. Provide answers for all traits.'}), 400

    # Convert answers to numerical values
    responses = []
    for trait, questions in questions_mapping.items():
        trait_scores = [user_answers.get(question, 0) for question in questions]
        responses.append(np.mean(trait_scores))  # Average scores for each trait

    # Scale responses
    responses_scaled = scaler.transform([responses])

    # Predict OCEAN traits
    predictions = {trait: model.predict(responses_scaled)[0] for trait, model in models.items()}

    # Normalize predictions to sum to 100
    total_score = sum(predictions.values())
    normalized_scores = {trait: round((score / total_score) * 100, 2) for trait, score in predictions.items()}

    # Identify dominant trait
    dominant_trait = max(normalized_scores, key=normalized_scores.get)

    return jsonify({
        'scores': normalized_scores,
        'dominant_trait': dominant_trait
    })

if __name__ == '__main__':
    app.run(debug=True)
