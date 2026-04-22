"""
Test suite for Partidas filters feature
Tests: year filter, month filter, result filter, and combinations
Expected data: 30 partidas (11 in 2024, 12 in 2025, 4 in 2026 + 3 pre-existing in 2024)
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestAuth:
    """Authentication test to get token for subsequent tests"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "diretoria@ecp.com.br",
            "senha": "ecp2024"
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        return data["access_token"]
    
    def test_login_success(self, auth_token):
        """Verify login works and returns token"""
        assert auth_token is not None
        assert len(auth_token) > 0
        print(f"Login successful, token obtained")


class TestPartidasFilters:
    """Test Partidas endpoint with various filter combinations"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "diretoria@ecp.com.br",
            "senha": "ecp2024"
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Authentication failed")
    
    @pytest.fixture(scope="class")
    def auth_headers(self, auth_token):
        """Return headers with auth token"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    def test_partidas_without_filters(self, auth_headers):
        """GET /api/partidas without filters should return all partidas (30)"""
        response = requests.get(f"{BASE_URL}/api/partidas", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should have 30 partidas total
        print(f"Total partidas without filter: {len(data)}")
        assert len(data) == 30, f"Expected 30 partidas, got {len(data)}"
        # Verify each partida has required fields
        for partida in data:
            assert "id" in partida
            assert "data" in partida
            assert "adversario" in partida
            assert "resultado" in partida
            assert partida["resultado"] in ["Vitória", "Empate", "Derrota"]
    
    def test_partidas_filter_by_year_2025(self, auth_headers):
        """GET /api/partidas?ano=2025 should return 12 partidas"""
        response = requests.get(f"{BASE_URL}/api/partidas?ano=2025", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas in 2025: {len(data)}")
        assert len(data) == 12, f"Expected 12 partidas in 2025, got {len(data)}"
        # Verify all partidas are from 2025
        for partida in data:
            assert partida["data"].startswith("2025"), f"Partida date {partida['data']} is not from 2025"
    
    def test_partidas_filter_by_year_2024(self, auth_headers):
        """GET /api/partidas?ano=2024 should return 14 partidas (11 seeded + 3 pre-existing)"""
        response = requests.get(f"{BASE_URL}/api/partidas?ano=2024", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas in 2024: {len(data)}")
        # 11 seeded + 3 pre-existing = 14
        assert len(data) == 14, f"Expected 14 partidas in 2024, got {len(data)}"
        for partida in data:
            assert partida["data"].startswith("2024")
    
    def test_partidas_filter_by_year_2026(self, auth_headers):
        """GET /api/partidas?ano=2026 should return 4 partidas"""
        response = requests.get(f"{BASE_URL}/api/partidas?ano=2026", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas in 2026: {len(data)}")
        assert len(data) == 4, f"Expected 4 partidas in 2026, got {len(data)}"
        for partida in data:
            assert partida["data"].startswith("2026")
    
    def test_partidas_filter_by_resultado_vitoria(self, auth_headers):
        """GET /api/partidas?resultado=Vitória should return only victories"""
        # URL encode Vitória
        response = requests.get(f"{BASE_URL}/api/partidas?resultado=Vit%C3%B3ria", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas with Vitória: {len(data)}")
        assert len(data) > 0, "Expected at least one victory"
        for partida in data:
            assert partida["resultado"] == "Vitória", f"Expected Vitória, got {partida['resultado']}"
    
    def test_partidas_filter_by_resultado_empate(self, auth_headers):
        """GET /api/partidas?resultado=Empate should return only draws"""
        response = requests.get(f"{BASE_URL}/api/partidas?resultado=Empate", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas with Empate: {len(data)}")
        for partida in data:
            assert partida["resultado"] == "Empate", f"Expected Empate, got {partida['resultado']}"
    
    def test_partidas_filter_by_resultado_derrota(self, auth_headers):
        """GET /api/partidas?resultado=Derrota should return only defeats"""
        response = requests.get(f"{BASE_URL}/api/partidas?resultado=Derrota", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas with Derrota: {len(data)}")
        for partida in data:
            assert partida["resultado"] == "Derrota", f"Expected Derrota, got {partida['resultado']}"
    
    def test_partidas_filter_year_and_resultado(self, auth_headers):
        """GET /api/partidas?ano=2024&resultado=Derrota should return 2 partidas"""
        response = requests.get(f"{BASE_URL}/api/partidas?ano=2024&resultado=Derrota", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas in 2024 with Derrota: {len(data)}")
        assert len(data) == 2, f"Expected 2 partidas in 2024 with Derrota, got {len(data)}"
        for partida in data:
            assert partida["data"].startswith("2024")
            assert partida["resultado"] == "Derrota"
    
    def test_partidas_filter_year_and_month(self, auth_headers):
        """GET /api/partidas?ano=2024&mes=3 should return 1 partida"""
        response = requests.get(f"{BASE_URL}/api/partidas?ano=2024&mes=3", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas in March 2024: {len(data)}")
        assert len(data) == 1, f"Expected 1 partida in March 2024, got {len(data)}"
        for partida in data:
            assert partida["data"].startswith("2024-03")
    
    def test_partidas_filter_year_month_resultado(self, auth_headers):
        """GET /api/partidas?ano=2025&mes=6&resultado=Vitória should filter by all three"""
        response = requests.get(f"{BASE_URL}/api/partidas?ano=2025&mes=6&resultado=Vit%C3%B3ria", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Partidas in June 2025 with Vitória: {len(data)}")
        for partida in data:
            assert partida["data"].startswith("2025-06")
            assert partida["resultado"] == "Vitória"
    
    def test_partidas_resultado_calculation(self, auth_headers):
        """Verify resultado is correctly calculated based on goals"""
        response = requests.get(f"{BASE_URL}/api/partidas", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        for partida in data:
            gols_clube = partida["gols_clube"]
            gols_adversario = partida["gols_adversario"]
            expected_resultado = (
                "Vitória" if gols_clube > gols_adversario else
                "Derrota" if gols_clube < gols_adversario else
                "Empate"
            )
            assert partida["resultado"] == expected_resultado, \
                f"Partida {partida['id']}: {gols_clube}x{gols_adversario} should be {expected_resultado}, got {partida['resultado']}"
        print("All resultado calculations are correct")


class TestPartidasCRUD:
    """Test that CRUD operations still work after filter implementation"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "diretoria@ecp.com.br",
            "senha": "ecp2024"
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Authentication failed")
    
    @pytest.fixture(scope="class")
    def auth_headers(self, auth_token):
        """Return headers with auth token"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    def test_create_partida(self, auth_headers):
        """POST /api/partidas should create a new partida"""
        new_partida = {
            "data": "2026-12-25",
            "adversario": "TEST_Time Teste",
            "local": "Estádio Teste",
            "gols_clube": 3,
            "gols_adversario": 1
        }
        response = requests.post(f"{BASE_URL}/api/partidas", json=new_partida, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["adversario"] == "TEST_Time Teste"
        assert data["resultado"] == "Vitória"
        assert "id" in data
        # Store ID for cleanup
        TestPartidasCRUD.created_partida_id = data["id"]
        print(f"Created partida with ID: {data['id']}")
    
    def test_get_created_partida(self, auth_headers):
        """GET /api/partidas/{id} should return the created partida"""
        partida_id = getattr(TestPartidasCRUD, 'created_partida_id', None)
        if not partida_id:
            pytest.skip("No partida was created")
        
        response = requests.get(f"{BASE_URL}/api/partidas/{partida_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["adversario"] == "TEST_Time Teste"
        assert data["resultado"] == "Vitória"
        print(f"Retrieved partida: {data['adversario']}")
    
    def test_update_partida(self, auth_headers):
        """PUT /api/partidas/{id} should update the partida"""
        partida_id = getattr(TestPartidasCRUD, 'created_partida_id', None)
        if not partida_id:
            pytest.skip("No partida was created")
        
        updated_data = {
            "data": "2026-12-25",
            "adversario": "TEST_Time Atualizado",
            "local": "Estádio Atualizado",
            "gols_clube": 1,
            "gols_adversario": 2
        }
        response = requests.put(f"{BASE_URL}/api/partidas/{partida_id}", json=updated_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["adversario"] == "TEST_Time Atualizado"
        assert data["resultado"] == "Derrota"  # 1x2 = Derrota
        print(f"Updated partida: {data['adversario']}, resultado: {data['resultado']}")
    
    def test_delete_partida(self, auth_headers):
        """DELETE /api/partidas/{id} should delete the partida"""
        partida_id = getattr(TestPartidasCRUD, 'created_partida_id', None)
        if not partida_id:
            pytest.skip("No partida was created")
        
        response = requests.delete(f"{BASE_URL}/api/partidas/{partida_id}", headers=auth_headers)
        assert response.status_code == 200
        
        # Verify deletion
        response = requests.get(f"{BASE_URL}/api/partidas/{partida_id}", headers=auth_headers)
        assert response.status_code == 404
        print(f"Deleted partida with ID: {partida_id}")


class TestPartidasUnauthorized:
    """Test that endpoints require authentication"""
    
    def test_partidas_unauthorized(self):
        """GET /api/partidas without token should return 403"""
        response = requests.get(f"{BASE_URL}/api/partidas")
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        print("Unauthorized access correctly rejected")
