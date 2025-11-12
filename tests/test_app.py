import pytest


class TestHomePage:
    """Test the home page endpoint"""
    
    def test_index_page_loads(self, client):
        """Test that the index page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Study Buddy' in response.data or b'study' in response.data.lower()


class TestNotesFeature:
    """Test notes management"""
    
    def test_notes_page_loads(self, client):
        """Test that notes page loads"""
        response = client.get('/notes')
        assert response.status_code == 200
    
    def test_can_create_note(self, client):
        """Test creating a note"""
        response = client.post('/notes', data={
            'content': 'Test note content'
        }, follow_redirects=True)
        assert response.status_code == 200


class TestFlashcardsFeature:
    """Test flashcards management"""
    
    def test_flashcards_page_loads(self, client):
        """Test that flashcards page loads"""
        response = client.get('/flashcards')
        assert response.status_code == 200
    
    def test_can_create_flashcard(self, client):
        """Test creating a flashcard"""
        response = client.post('/flashcards', data={
            'term': 'Test Term',
            'definition': 'Test Definition'
        }, follow_redirects=True)
        assert response.status_code == 200


class TestQuizFeature:
    """Test quiz feature"""
    
    def test_quiz_page_loads(self, client):
        """Test that quiz page loads"""
        response = client.get('/quiz')
        # May redirect if no flashcards
        assert response.status_code in [200, 302]


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_404_for_nonexistent_route(self, client):
        """Test that nonexistent routes return 404"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
    
    def test_404_for_invalid_topic_id(self, client):
        """Test that invalid topic IDs return 404"""
        response = client.get('/topics/9999/notes')
        assert response.status_code == 404


class TestTopicManagement:
    """Test topic CRUD operations"""
    
    def test_list_topics_page(self, client):
        """Test that topics list page loads"""
        response = client.get('/topics/')
        assert response.status_code == 200
    
    def test_create_topic_form(self, client):
        """Test that topic creation form loads"""
        response = client.get('/topics/create')
        assert response.status_code == 200
