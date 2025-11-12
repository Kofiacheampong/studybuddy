import pytest
from flask import url_for


class TestHomePage:
    """Test the home page endpoint"""
    
    def test_index_page_loads(self, client):
        """Test that the index page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Study Buddy' in response.data
    
    def test_index_page_has_cta_buttons(self, client):
        """Test that the index page has call-to-action buttons"""
        response = client.get('/')
        assert response.status_code == 200
        # Check for key CTAs
        assert b'Get Started' in response.data or b'get started' in response.data.lower()


class TestTopicManagement:
    """Test topic CRUD operations"""
    
    def test_list_topics_page(self, client):
        """Test that topics list page loads"""
        response = client.get('/topics/')
        assert response.status_code == 200
        assert b'Topic' in response.data or b'topic' in response.data.lower()
    
    def test_create_topic_form(self, client):
        """Test that topic creation form loads"""
        response = client.get('/topics/create')
        assert response.status_code == 200
        assert b'Create' in response.data or b'create' in response.data.lower()
    
    def test_create_topic_post(self, client):
        """Test creating a topic via POST"""
        response = client.post('/topics/create', data={
            'name': 'Test Topic',
            'description': 'Test Description'
        }, follow_redirects=True)
        assert response.status_code == 200


class TestNotesFeature:
    """Test notes management"""
    
    def test_notes_page_loads(self, client):
        """Test that notes page loads"""
        # This assumes a default topic exists or is created
        response = client.get('/notes/', follow_redirects=True)
        assert response.status_code == 200


class TestFlashcardsFeature:
    """Test flashcards management"""
    
    def test_flashcards_page_loads(self, client):
        """Test that flashcards page loads"""
        response = client.get('/flashcards/', follow_redirects=True)
        assert response.status_code == 200


class TestQuizFeature:
    """Test quiz feature"""
    
    def test_quiz_page_loads(self, client):
        """Test that quiz page loads"""
        response = client.get('/quiz/', follow_redirects=True)
        assert response.status_code == 200


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
