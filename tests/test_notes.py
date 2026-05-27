import pytest
from fastapi import status


class TestNoteCreation:
    """Tests for note creation endpoint."""
    
    def test_create_note_success(self, client, test_user_token):
        """Test successful note creation."""
        response = client.post(
            "/api/notes",
            json={
                "title": "My First Note",
                "description": "This is a test note",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "My First Note"
        assert data["description"] == "This is a test note"
        assert data["status"] == "active"
        assert "id" in data
        assert "user_id" in data
        assert "created_at" in data
    
    def test_create_note_without_description(self, client, test_user_token):
        """Test creating note without description."""
        response = client.post(
            "/api/notes",
            json={
                "title": "Note Without Desc",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Note Without Desc"
        assert data["description"] is None
    
    def test_create_note_no_auth(self, client):
        """Test creating note without authentication."""
        response = client.post(
            "/api/notes",
            json={
                "title": "Unauthorized Note",
                "status": "active",
            },
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_note_empty_title(self, client, test_user_token):
        """Test creating note with empty title."""
        response = client.post(
            "/api/notes",
            json={
                "title": "",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestNoteList:
    """Tests for note listing endpoint."""
    
    def test_list_notes_empty(self, client, test_user_token):
        """Test listing notes when no notes exist."""
        response = client.get(
            "/api/notes",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
    
    def test_list_notes_multiple(self, client, test_user_token):
        """Test listing multiple notes."""
        # Create notes
        for i in range(3):
            client.post(
                "/api/notes",
                json={
                    "title": f"Note {i+1}",
                    "description": f"Description {i+1}",
                    "status": "active",
                },
                headers={"Authorization": f"Bearer {test_user_token}"},
            )
        
        # List notes
        response = client.get(
            "/api/notes",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3
    
    def test_list_notes_pagination(self, client, test_user_token):
        """Test note pagination."""
        # Create 15 notes
        for i in range(15):
            client.post(
                "/api/notes",
                json={
                    "title": f"Note {i+1}",
                    "status": "active",
                },
                headers={"Authorization": f"Bearer {test_user_token}"},
            )
        
        # Get first page
        response = client.get(
            "/api/notes?skip=0&limit=10",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["skip"] == 0
        assert data["limit"] == 10
        
        # Get second page
        response = client.get(
            "/api/notes?skip=10&limit=10",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 5
    
    def test_list_notes_filter_by_status(self, client, test_user_token):
        """Test filtering notes by status."""
        # Create notes with different statuses
        client.post(
            "/api/notes",
            json={
                "title": "Active Note 1",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        client.post(
            "/api/notes",
            json={
                "title": "Active Note 2",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        client.post(
            "/api/notes",
            json={
                "title": "Archived Note",
                "status": "archived",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        # Filter by active status
        response = client.get(
            "/api/notes?status=active",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2
        assert all(note["status"] == "active" for note in data["items"])
        
        # Filter by archived status
        response = client.get(
            "/api/notes?status=archived",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["status"] == "archived"


class TestNoteDetail:
    """Tests for getting single note detail."""
    
    def test_get_note_success(self, client, test_user_token):
        """Test getting note details."""
        # Create a note
        create_response = client.post(
            "/api/notes",
            json={
                "title": "Detail Test",
                "description": "Test description",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        note_id = create_response.json()["id"]
        
        # Get note
        response = client.get(
            f"/api/notes/{note_id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == note_id
        assert data["title"] == "Detail Test"
    
    def test_get_note_not_found(self, client, test_user_token):
        """Test getting non-existent note."""
        response = client.get(
            "/api/notes/99999",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestNoteUpdate:
    """Tests for note update endpoint."""
    
    def test_update_note_title(self, client, test_user_token):
        """Test updating note title."""
        # Create a note
        create_response = client.post(
            "/api/notes",
            json={
                "title": "Original Title",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        note_id = create_response.json()["id"]
        
        # Update note
        response = client.put(
            f"/api/notes/{note_id}",
            json={
                "title": "Updated Title",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
    
    def test_update_note_status(self, client, test_user_token):
        """Test updating note status."""
        # Create a note
        create_response = client.post(
            "/api/notes",
            json={
                "title": "Status Test",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        note_id = create_response.json()["id"]
        
        # Update status
        response = client.put(
            f"/api/notes/{note_id}",
            json={
                "status": "archived",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "archived"
    
    def test_update_note_all_fields(self, client, test_user_token):
        """Test updating all note fields."""
        # Create a note
        create_response = client.post(
            "/api/notes",
            json={
                "title": "Original",
                "description": "Original desc",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        note_id = create_response.json()["id"]
        
        # Update all fields
        response = client.put(
            f"/api/notes/{note_id}",
            json={
                "title": "Updated",
                "description": "Updated description",
                "status": "archived",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated"
        assert data["description"] == "Updated description"
        assert data["status"] == "archived"
    
    def test_update_note_not_found(self, client, test_user_token):
        """Test updating non-existent note."""
        response = client.put(
            "/api/notes/99999",
            json={
                "title": "Updated",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestNoteDelete:
    """Tests for note delete endpoint."""
    
    def test_delete_note_success(self, client, test_user_token):
        """Test successful note deletion."""
        # Create a note
        create_response = client.post(
            "/api/notes",
            json={
                "title": "To Delete",
                "status": "active",
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        note_id = create_response.json()["id"]
        
        # Delete note
        response = client.delete(
            f"/api/notes/{note_id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        get_response = client.get(
            f"/api/notes/{note_id}",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_note_not_found(self, client, test_user_token):
        """Test deleting non-existent note."""
        response = client.delete(
            "/api/notes/99999",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
