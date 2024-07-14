from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, sentence TEXT)''')
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/teach', methods=['POST'])
def teach():
    sentence = request.form['sentence']
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO knowledge (sentence) VALUES (?)", (sentence,))
        conn.commit()
    return jsonify({"status": "Sentence added successfully!"})

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    # Simple logic to find the answer in stored sentences
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("SELECT sentence FROM knowledge")
        sentences = c.fetchall()
        for sentence in sentences:
            if question.lower() in sentence[0].lower():
                return jsonify({"answer": sentence[0]})
    return jsonify({"answer": "I don't know the answer to that question."})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
