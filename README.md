# OCI Study Buddy

A modern, minimalist Flask web application designed to help you study Oracle Cloud Infrastructure (OCI) concepts through intelligent note-taking and AI-powered content generation.

## Features

- **Quick Notes**: Simple, fast note-taking interface for capturing study thoughts
- **AI-Powered Content Processing**: Transform raw OCI content into structured summaries using Claude AI
- **Flashcard Generation**: Automatically generate study flashcards from your content
- **Modern UI**: Clean, minimalist design inspired by modern web applications
- **Dark/Light Mode**: Seamless theme switching for comfortable studying
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## Technology Stack

- **Backend**: Flask 2.3.2 (Python web framework)
- **Database**: SQLite (lightweight, file-based database)
- **AI Integration**: Anthropic Claude 3.5 Sonnet API
- **Frontend**: Bootstrap 5 with custom CSS
- **Templates**: Jinja2 template engine

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd oci_study_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the app**
   Open your browser and navigate to `http://localhost:5000`

## Usage

### Quick Notes
- Use the "Quick Notes" section to jot down important OCI concepts
- Notes are automatically saved to your local SQLite database
- All saved notes appear in the "Saved Notes" section below

### AI-Powered Content Processing
- Paste raw OCI documentation, transcripts, or study materials
- Click "Generate Summary" to get a structured summary using Claude AI
- Use "Generate Flashcards" to create study flashcards from your content

### Navigation
- **Home**: Overview and getting started
- **Notes**: Main study interface (note-taking and AI features)
- **Flashcards**: View and study your generated flashcards
- **Quiz**: Test your OCI knowledge

## File Structure

```
oci_study_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── oci_study.db          # SQLite database (auto-generated)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── notes.html        # Notes interface
│   ├── flashcards.html   # Flashcards page
│   └── quiz.html         # Quiz page
└── static/
    └── style.css         # Custom CSS styles
```

## Database Schema

The application uses a simple SQLite database with one table:

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
);
```

## API Endpoints

- `GET /` - Home page
- `GET /notes` - Notes page (display notes and forms)
- `POST /notes` - Create a new note
- `POST /generate` - Generate AI summary (returns JSON)
- `POST /flashcards` - Generate AI flashcards (returns JSON)

## Development

### Debug Mode
The application runs in debug mode by default during development:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Adding New Features
1. Update routes in `app.py`
2. Create or modify templates in `templates/`
3. Add styling to `static/style.css`
4. Update database schema if needed

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key for Claude AI integration | Yes |

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure you've installed all dependencies: `pip install -r requirements.txt`

2. **AI features not working**
   - Check your `.env` file contains a valid `ANTHROPIC_API_KEY`
   - Verify your API key has sufficient credits/usage limits

3. **Database errors**
   - The SQLite database is created automatically on first run
   - If issues persist, delete `oci_study.db` to reset the database

4. **Port already in use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

## Contributing

This is a study application. Feel free to fork and modify for your own learning needs.

## License

This project is for educational purposes. Please respect Oracle's trademarks and Anthropic's API terms of service.