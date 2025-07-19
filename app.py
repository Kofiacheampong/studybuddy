from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from dotenv import load_dotenv
from anthropic import Anthropic

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key:
    client = Anthropic(api_key=api_key)
else:
    client = None
    print("Warning: ANTHROPIC_API_KEY not found in environment variables. AI features will be disabled.")

DB = 'oci_study.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS flashcards (id INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT NOT NULL, definition TEXT NOT NULL)")
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            c.execute('INSERT INTO notes (content) VALUES (?)', (content,))
            conn.commit()
        return redirect(url_for('notes'))
    c.execute('SELECT * FROM notes ORDER BY id DESC')
    notes = c.fetchall()
    conn.close()
    return render_template('notes.html', notes=notes)

@app.route('/generate', methods=['POST'])
def generate_summary():
    if not client:
        return jsonify({"error": "AI features are disabled. Please set ANTHROPIC_API_KEY in your .env file."}), 400
    
    try:
        raw_text = request.form['raw_text']
        prompt = f"Summarize this Oracle Cloud Infrastructure training content into clear, organized notes:\n\n{raw_text}"
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.content[0].text.strip()

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('INSERT INTO notes (content) VALUES (?)', (summary,))
        conn.commit()
        conn.close()

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": f"Error generating summary: {str(e)}"}), 500

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    if request.method == 'POST':
        if 'raw_text' in request.form:
            # AI-generated flashcards
            if not client:
                return jsonify({"error": "AI features are disabled. Please set ANTHROPIC_API_KEY in your .env file."}), 400
            
            try:
                raw_text = request.form['raw_text']
                prompt = f"Generate 5 concise flashcards based on the following Oracle Cloud content. Format as 'Term: Definition' pairs, one per line:\n\n{raw_text}"
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                flashcards_text = response.content[0].text.strip()
                
                # Parse and save flashcards
                lines = flashcards_text.split('\n')
                for line in lines:
                    if ':' in line:
                        term, definition = line.split(':', 1)
                        term = term.strip()
                        definition = definition.strip()
                        if term and definition:
                            c.execute('INSERT INTO flashcards (term, definition) VALUES (?, ?)', (term, definition))
                
                conn.commit()
                return jsonify({"flashcards": flashcards_text})
            except Exception as e:
                return jsonify({"error": f"Error generating flashcards: {str(e)}"}), 500
        else:
            # Manual flashcard creation
            term = request.form['term']
            definition = request.form['definition']
            if term.strip() and definition.strip():
                c.execute('INSERT INTO flashcards (term, definition) VALUES (?, ?)', (term, definition))
                conn.commit()
            return redirect(url_for('flashcards'))
    
    # GET request - display flashcards
    c.execute('SELECT * FROM flashcards ORDER BY id DESC')
    flashcards = c.fetchall()
    conn.close()
    return render_template('flashcards.html', flashcards=flashcards)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    if request.method == 'POST':
        # Process quiz answers
        c.execute('SELECT * FROM flashcards')
        cards = c.fetchall()
        
        score = 0
        for card in cards:
            card_id = str(card[0])
            if card_id in request.form:
                user_answer = request.form[card_id].strip().lower()
                correct_answer = card[2].strip().lower()
                if user_answer in correct_answer or correct_answer in user_answer:
                    score += 1
        
        conn.close()
        return render_template('quiz.html', submitted=True, score=score, cards=cards)
    
    # GET request - show quiz
    c.execute('SELECT * FROM flashcards ORDER BY RANDOM() LIMIT 10')
    cards = c.fetchall()
    conn.close()
    
    if not cards:
        return redirect(url_for('flashcards'))
    
    return render_template('quiz.html', submitted=False, cards=cards)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
# app.py - Main application file for the OCI Study Buddy Flask app
# This file initializes the Flask app, sets up routes for notes and flashcards,
# and handles database interactions using SQLite.