
from flask import Flask, render_template, request, jsonify
from soccer_planner.api_handler import WeatherAPI, OpenAIAPI
from soccer_planner.data_manager import TrainingDataManager
from googletrans import Translator


app = Flask(__name__)

# Initialize API handlers
weather_api = WeatherAPI(api_key="")
gpt_api = OpenAIAPI(api_key=)
translator = Translator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        team = request.form["team"]
        focus = request.form["focus"]
        location = request.form["location"]

        # Fetch weather data
        weather = weather_api.get_weather(location)

        # Generate training plan using OpenAI GPT
        drills = gpt_api.generate_training_plan(focus)

        # Save the data
        data_manager = TrainingDataManager("training_data.csv")
        data_manager.save_training_plan(team, focus, drills)

        return render_template("results.html", team=team, focus=focus, weather=weather, drills=drills)
    except Exception as e:
        return render_template("error.html", error_message=str(e))

@app.route("/translate", methods=["POST"])
def translate_text_form():
    try:
        # Get data from form
        text_to_translate = request.form.get("text", "").strip()
        target_language = request.form.get("lang", "es").strip()

        # Validate inputs
        if not text_to_translate:
            return jsonify({"error": "No text provided"}), 400

        # Perform translation
        translated = translator.translate(text_to_translate, dest=target_language)

        # Return the translated text
        return jsonify({"translated_text": translated.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
