from flask import Blueprint, render_template, request, redirect, url_for
from database import get_db_connection, USE_POSTGRES
import sqlite3

# Import appropriate exception based on database type
if USE_POSTGRES:
    try:
        import psycopg2
        IntegrityError = psycopg2.IntegrityError
    except ImportError:
        IntegrityError = Exception
else:
    IntegrityError = sqlite3.IntegrityError

bp = Blueprint('topics', __name__, url_prefix='/topics')

@bp.route('/')
def list_topics():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, description FROM topics ORDER BY name')
    topics = c.fetchall()
    conn.close()
    # Build simple stats
    topic_stats = []
    for t in topics:
        tid = t[0]
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM notes WHERE topic_id = ?', (tid,))
        notes_count = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM flashcards WHERE topic_id = ?', (tid,))
        cards_count = c.fetchone()[0]
        conn.close()
        topic_stats.append({'id': tid, 'name': t[1], 'description': t[2], 'notes': notes_count, 'flashcards': cards_count})
    return render_template('topics.html', topics=topic_stats)

@bp.route('/create', methods=['GET', 'POST'])
def create_topic():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            return render_template('create_topic.html', error='Topic name is required')
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO topics (name, description) VALUES (?, ?)', (name, description))
            conn.commit()
            topic_id = c.lastrowid
            conn.close()
            return redirect(url_for('topics.view_topic', topic_id=topic_id))
        except IntegrityError:
            conn.close()
            return render_template('create_topic.html', error='Topic already exists')
    return render_template('create_topic.html')

@bp.route('/<int:topic_id>')
def view_topic(topic_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, description FROM topics WHERE id = ?', (topic_id,))
    t = c.fetchone()
    if not t:
        conn.close()
        return 'Topic not found', 404
    c.execute('SELECT COUNT(*) FROM notes WHERE topic_id = ?', (topic_id,))
    notes_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM flashcards WHERE topic_id = ?', (topic_id,))
    cards_count = c.fetchone()[0]
    conn.close()
    topic = {'id': t[0], 'name': t[1], 'description': t[2]}
    return render_template('topic_view.html', topic=topic, notes=notes_count, flashcards=cards_count)

@bp.route('/<int:topic_id>/edit', methods=['GET', 'POST'])
def edit_topic(topic_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, description FROM topics WHERE id = ?', (topic_id,))
    t = c.fetchone()
    if not t:
        conn.close()
        return 'Topic not found', 404
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            conn.close()
            return render_template('edit_topic.html', topic={'id': t[0], 'name': t[1], 'description': t[2]}, error='Name required')
        try:
            c.execute('UPDATE topics SET name = ?, description = ? WHERE id = ?', (name, description, topic_id))
            conn.commit()
            conn.close()
            return redirect(url_for('topics.view_topic', topic_id=topic_id))
        except IntegrityError:
            conn.close()
            return render_template('edit_topic.html', topic={'id': t[0], 'name': t[1], 'description': t[2]}, error='Topic name exists')
    conn.close()
    return render_template('edit_topic.html', topic={'id': t[0], 'name': t[1], 'description': t[2]})

@bp.route('/<int:topic_id>/delete', methods=['POST'])
def delete_topic(topic_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM topics WHERE id = ?', (topic_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('topics.list_topics'))
