from gemini import Gemini
from flask import Flask, render_template, request, jsonify
import creds

app = Flask(__name__)
client = Gemini(cookies=creds.api_key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    prompt = request.form.get("prompt")
    selected_mode = request.form.get("mode")
    selected_num = int(request.form.get("num"))
    selected_anspref = request.form.get("ans")

    if selected_num >= 16:
        return jsonify({"answer": "Error: Maximum number of questions is 15"})

    try:
        if selected_mode == "Multiple":
            if selected_anspref == "Yes":
                response = client.generate_content(f"{creds.multiple_choice} containing {selected_num} questions based on this notes: {prompt} please include answer key")
            elif selected_anspref == "No":
                response = client.generate_content(f"{creds.multiple_choice} containing {selected_num} questions based on this notes: {prompt} Do not include any answer key")
        elif selected_mode == "Open":
            if selected_anspref == "Yes":
                response = client.generate_content(f"{creds.open_ended} containing {selected_num} questions based on this notes: {prompt} please include answer key")
            elif selected_anspref == "No":
                response = client.generate_content(f"{creds.open_ended} containing {selected_num} questions based on this notes: {prompt} Do not include any answer key")
        else:
            return jsonify({"answer": "Please Select Preferences"})

        if response and 'candidates' in response and 'text' in response['candidates']:
            extracted_text = response['candidates']['text']
            # Formatta la risposta prima di restituirla
            formatted_answer = extracted_text.replace('\n', '<br>').replace('*', '')
            return jsonify({"answer": formatted_answer})
        else:
            return jsonify({"answer": "Failed to get a valid response from Gemini API"})

    except Exception as e:
        return jsonify({"answer": f"Error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
