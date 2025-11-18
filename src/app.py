from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from database import get_db_connection, init_database, get_placeholder, USE_POSTGRES

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Register topics blueprint
try:
    from topics_manager import bp as topics_bp
    app.register_blueprint(topics_bp)
except Exception:
    # If import fails (during early init), continue; blueprint can be registered later
    pass

# Configure app for subdirectory deployment
class SubdirectoryMiddleware:
    def __init__(self, app, subdirectory='/study'):
        self.app = app
        self.subdirectory = subdirectory

    def __call__(self, environ, start_response):
        script_name = self.subdirectory
        path_info = environ['PATH_INFO']
        if path_info.startswith(script_name):
            environ['PATH_INFO'] = path_info[len(script_name):]
            environ['SCRIPT_NAME'] = script_name
            return self.app(environ, start_response)
        else:
            environ['SCRIPT_NAME'] = script_name
            return self.app(environ, start_response)

# Only apply middleware in production
if os.getenv('FLASK_ENV') != 'development':
    app.wsgi_app = SubdirectoryMiddleware(app.wsgi_app)

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key:
    client = Anthropic(api_key=api_key)
else:
    client = None
    print("Warning: ANTHROPIC_API_KEY not found in environment variables. AI features will be disabled.")

# Initialize database when app starts
init_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Get default topic
    c.execute('SELECT id FROM topics WHERE name = ?', ('General',))
    topic = c.fetchone()
    if not topic:
        # Create default topic if it doesn't exist
        c.execute('INSERT INTO topics (name, description) VALUES (?, ?)', 
                  ('General', 'Default study topic'))
        conn.commit()
        topic_id = c.lastrowid
    else:
        topic_id = topic[0]
    
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            c.execute('INSERT INTO notes (topic_id, content) VALUES (?, ?)', (topic_id, content))
            conn.commit()
        return redirect(url_for('notes'))
    
    c.execute('SELECT * FROM notes WHERE topic_id = ? ORDER BY id DESC', (topic_id,))
    notes_list = c.fetchall()
    # pass topic tuple to template for display
    c.execute('SELECT id, name FROM topics WHERE id = ?', (topic_id,))
    topic_tuple = c.fetchone()
    conn.close()
    return render_template('notes.html', notes=notes_list, topic=topic_tuple)

@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # Get default topic id
    c.execute('SELECT id FROM topics WHERE name = ?', ('General',))
    topic = c.fetchone()
    topic_id = topic[0] if topic else 1
    
    c.execute('DELETE FROM notes WHERE id = ? AND topic_id = ?', (note_id, topic_id))
    conn.commit()
    conn.close()
    return redirect(url_for('notes'))

@app.route('/generate', methods=['POST'])
def generate_summary():
    if not client:
        return jsonify({"error": "AI features are disabled. Please set ANTHROPIC_API_KEY in your .env file."}), 400
    
    try:
        # Get default topic
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('SELECT id FROM topics WHERE name = ?', ('General',))
        topic = c.fetchone()
        topic_id = topic[0] if topic else 1
        conn.close()
        
        raw_text = request.form['raw_text']
        prompt = f"Summarize this training content into clear, organized, well-structured study notes:\n\n{raw_text}"
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.content[0].text.strip()

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('INSERT INTO notes (topic_id, content) VALUES (?, ?)', (topic_id, summary))
        conn.commit()
        conn.close()

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": f"Error generating summary: {str(e)}"}), 500

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Get default topic
    c.execute('SELECT id FROM topics WHERE name = ?', ('General',))
    topic = c.fetchone()
    if not topic:
        c.execute('INSERT INTO topics (name, description) VALUES (?, ?)', 
                  ('General', 'Default study topic'))
        conn.commit()
        topic_id = c.lastrowid
    else:
        topic_id = topic[0]
    
    if request.method == 'POST':
        if 'raw_text' in request.form:
            # AI-generated flashcards
            if not client:
                return jsonify({"error": "AI features are disabled. Please set ANTHROPIC_API_KEY in your .env file."}), 400
            
            try:
                raw_text = request.form['raw_text']
                prompt = f"Generate 5 concise flashcards based on the following study content. Format as 'Term: Definition' pairs, one per line:\n\n{raw_text}"
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
                            c.execute('INSERT INTO flashcards (topic_id, term, definition) VALUES (?, ?, ?)', 
                                      (topic_id, term, definition))
                
                conn.commit()
                return jsonify({"flashcards": flashcards_text})
            except Exception as e:
                return jsonify({"error": f"Error generating flashcards: {str(e)}"}), 500
        else:
            # Manual flashcard creation
            term = request.form['term'].strip()
            definition = request.form['definition'].strip()
            if term and definition:
                c.execute('INSERT INTO flashcards (topic_id, term, definition) VALUES (?, ?, ?)', 
                          (topic_id, term, definition))
                conn.commit()
            conn.close()
            return redirect(url_for('flashcards'))
    
    # GET request - display flashcards
    c.execute('SELECT * FROM flashcards WHERE topic_id = ? ORDER BY id DESC', (topic_id,))
    fc_list = c.fetchall()
    # pass topic info to template
    c.execute('SELECT id, name FROM topics WHERE id = ?', (topic_id,))
    topic_tuple = c.fetchone()
    conn.close()
    return render_template('flashcards.html', flashcards=fc_list, topic=topic_tuple)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Get default topic
    c.execute('SELECT id FROM topics WHERE name = ?', ('General',))
    topic = c.fetchone()
    topic_id = topic[0] if topic else 1
    
    if request.method == 'POST':
        # Process quiz answers
        c.execute('SELECT id, topic_id, term, definition FROM flashcards WHERE topic_id = ?', (topic_id,))
        cards = c.fetchall()
        
        score = 0
        for card in cards:
            card_id = str(card[0])
            if card_id in request.form:
                user_answer = request.form[card_id].strip().lower()
                correct_answer = card[3].strip().lower()  # definition is at index 3
                if user_answer in correct_answer or correct_answer in user_answer:
                    score += 1
        
        conn.close()
        return render_template('quiz.html', submitted=True, score=score, cards=cards)
    
    # GET request - show quiz
    c.execute('SELECT id, topic_id, term, definition FROM flashcards WHERE topic_id = ? ORDER BY RANDOM() LIMIT 10', (topic_id,))
    cards = c.fetchall()
    # get topic info for display
    c.execute('SELECT id, name FROM topics WHERE id = ?', (topic_id,))
    topic_tuple = c.fetchone()
    conn.close()
    
    if not cards:
        return redirect(url_for('flashcards'))
    
    return render_template('quiz.html', submitted=False, cards=cards, topic=topic_tuple)


# Topic-scoped routes (Phase 2)
@app.route('/topics/<int:topic_id>/notes', methods=['GET', 'POST'])
def notes_for_topic(topic_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # verify topic
    c.execute('SELECT id, name FROM topics WHERE id = ?', (topic_id,))
    t = c.fetchone()
    if not t:
        conn.close()
        return 'Topic not found', 404

    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if content:
            c.execute('INSERT INTO notes (topic_id, content) VALUES (?, ?)', (topic_id, content))
            conn.commit()
        return redirect(url_for('notes_for_topic', topic_id=topic_id))

    c.execute('SELECT * FROM notes WHERE topic_id = ? ORDER BY id DESC', (topic_id,))
    notes_list = c.fetchall()
    conn.close()
    return render_template('notes.html', notes=notes_list, topic=t)


@app.route('/topics/<int:topic_id>/delete_note/<int:note_id>', methods=['POST'])
def delete_note_for_topic(topic_id, note_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM notes WHERE id = ? AND topic_id = ?', (note_id, topic_id))
    conn.commit()
    conn.close()
    return redirect(url_for('notes_for_topic', topic_id=topic_id))


@app.route('/topics/<int:topic_id>/flashcards', methods=['GET', 'POST'])
def flashcards_for_topic(topic_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT id, name FROM topics WHERE id = ?', (topic_id,))
    t = c.fetchone()
    if not t:
        conn.close()
        return 'Topic not found', 404

    if request.method == 'POST':
        # manual or AI-generated handled via same field names
        if 'raw_text' in request.form and request.form.get('raw_text').strip():
            if not client:
                conn.close()
                return jsonify({"error": "AI features are disabled."}), 400
            try:
                raw_text = request.form['raw_text']
                prompt = f"Generate 5 concise flashcards based on the following study content. Format as 'Term: Definition' pairs, one per line:\n\n{raw_text}"
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                flashcards_text = response.content[0].text.strip()
                lines = flashcards_text.split('\n')
                for line in lines:
                    if ':' in line:
                        term, definition = line.split(':', 1)
                        term = term.strip()
                        definition = definition.strip()
                        if term and definition:
                            c.execute('INSERT INTO flashcards (topic_id, term, definition) VALUES (?, ?, ?)', (topic_id, term, definition))
                conn.commit()
                conn.close()
                return jsonify({"flashcards": flashcards_text})
            except Exception as e:
                conn.close()
                return jsonify({"error": f"Error generating flashcards: {str(e)}"}), 500
        else:
            term = request.form.get('term', '').strip()
            definition = request.form.get('definition', '').strip()
            if term and definition:
                c.execute('INSERT INTO flashcards (topic_id, term, definition) VALUES (?, ?, ?)', (topic_id, term, definition))
                conn.commit()
            conn.close()
            return redirect(url_for('flashcards_for_topic', topic_id=topic_id))

    c.execute('SELECT * FROM flashcards WHERE topic_id = ? ORDER BY id DESC', (topic_id,))
    fc_list = c.fetchall()
    conn.close()
    return render_template('flashcards.html', flashcards=fc_list, topic=t)


@app.route('/topics/<int:topic_id>/quiz', methods=['GET', 'POST'])
def quiz_for_topic(topic_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT id, name FROM topics WHERE id = ?', (topic_id,))
    t = c.fetchone()
    if not t:
        conn.close()
        return 'Topic not found', 404

    if request.method == 'POST':
        c.execute('SELECT id, topic_id, term, definition FROM flashcards WHERE topic_id = ?', (topic_id,))
        cards = c.fetchall()
        score = 0
        for card in cards:
            card_id = str(card[0])
            if card_id in request.form:
                user_answer = request.form[card_id].strip().lower()
                correct_answer = card[3].strip().lower()
                if user_answer in correct_answer or correct_answer in user_answer:
                    score += 1
        conn.close()
        return render_template('quiz.html', submitted=True, score=score, cards=cards, topic=t)

    c.execute('SELECT id, topic_id, term, definition FROM flashcards WHERE topic_id = ? ORDER BY RANDOM() LIMIT 10', (topic_id,))
    cards = c.fetchall()
    conn.close()
    if not cards:
        return redirect(url_for('flashcards_for_topic', topic_id=topic_id))
    return render_template('quiz.html', submitted=False, cards=cards, topic=t)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
