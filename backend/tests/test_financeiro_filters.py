"""
Test suite for Financeiro filters feature
Tests the month/year filtering on /api/recebimentos and /api/despesas endpoints
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestAuth:
    """Authentication tests to get token for subsequent tests"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token using test credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "diretoria@ecp.com.br",
            "senha": "ecp2024"
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        return data["access_token"]
    
    def test_login_success(self, auth_token):
        """Verify login works with test credentials"""
        assert auth_token is not None
        assert len(auth_token) > 0
        print(f"Login successful, token obtained")


class TestRecebimentosFilters:
    """Tests for /api/recebimentos endpoint with mes/ano filters"""
    
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
    def headers(self, auth_token):
        """Get headers with auth token"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    def test_recebimentos_without_filters(self, headers):
        """Test GET /api/recebimentos without any filters returns all data"""
        response = requests.get(f"{BASE_URL}/api/recebimentos", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Total recebimentos without filters: {len(data)}")
    
    def test_recebimentos_filter_by_year_2024(self, headers):
        """Test GET /api/recebimentos?ano=2024 returns only 2024 data"""
        response = requests.get(f"{BASE_URL}/api/recebimentos?ano=2024", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verify all returned items are from 2024
        for item in data:
            assert item["data"].startswith("2024"), f"Expected 2024 data, got {item['data']}"
        print(f"Recebimentos for 2024: {len(data)}")
    
    def test_recebimentos_filter_by_year_2026(self, headers):
        """Test GET /api/recebimentos?ano=2026 returns only 2026 data (expected 0)"""
        response = requests.get(f"{BASE_URL}/api/recebimentos?ano=2026", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # According to test data, 2026 should have 0 recebimentos
        for item in data:
            assert item["data"].startswith("2026"), f"Expected 2026 data, got {item['data']}"
        print(f"Recebimentos for 2026: {len(data)}")
    
    def test_recebimentos_filter_by_month_and_year(self, headers):
        """Test GET /api/recebimentos?mes=6&ano=2024 returns June 2024 data"""
        response = requests.get(f"{BASE_URL}/api/recebimentos?mes=6&ano=2024", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Verify all returned items are from June 2024
        for item in data:
            assert item["data"].startswith("2024-06"), f"Expected 2024-06 data, got {item['data']}"
        print(f"Recebimentos for June 2024: {len(data)}")
    
    def test_recebimentos_filter_by_december_2024(self, headers):
        """Test GET /api/recebimentos?mes=12&ano=2024 returns December 2024 data"""
        response = requests.get(f"{BASE_URL}/api/recebimentos?mes=12&ano=2024", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for item in data:
            assert item["data"].startswith("2024-12"), f"Expected 2024-12 data, got {item['data']}"
        print(f"Recebimentos for December 2024: {len(data)}")


class TestDespesasFilters:
    """Tests for /api/despesas endpoint with mes/ano filters"""
    
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
    def headers(self, auth_token):
        """Get headers with auth token"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    def test_despesas_without_filters(self, headers):
        """Test GET /api/despesas without any filters returns all data"""
        response = requests.get(f"{BASE_URL}/api/despesas", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Total despesas without filters: {len(data)}")
    
    def test_despesas_filter_by_year_2024(self, headers):
        """Test GET /api/despesas?ano=2024 returns only 2024 data"""
        response = requests.get(f"{BASE_URL}/api/despesas?ano=2024", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for item in data:
            assert item["data"].startswith("2024"), f"Expected 2024 data, got {item['data']}"
        print(f"Despesas for 2024: {len(data)}")
    
    def test_despesas_filter_by_year_2026(self, headers):
        """Test GET /api/despesas?ano=2026 returns only 2026 data"""
        response = requests.get(f"{BASE_URL}/api/despesas?ano=2026", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # According to test data, 2026 should have 1 despesa (2026-03-31)
        for item in data:
            assert item["data"].startswith("2026"), f"Expected 2026 data, got {item['data']}"
        print(f"Despesas for 2026: {len(data)}")
    
    def test_despesas_filter_by_month_and_year(self, headers):
        """Test GET /api/despesas?mes=3&ano=2026 returns March 2026 data"""
        response = requests.get(f"{BASE_URL}/api/despesas?mes=3&ano=2026", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        for item in data:
            assert item["data"].startswith("2026-03"), f"Expected 2026-03 data, got {item['data']}"
        print(f"Despesas for March 2026: {len(data)}")


class TestPatrocinadoresNotAffected:
    """Tests to verify patrocinadores endpoint is NOT affected by date filters"""
    
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
    def headers(self, auth_token):
        """Get headers with auth token"""
        return {"Authorization": f"Bearer {auth_token}"}
    
    def test_patrocinadores_no_date_filter_params(self, headers):
        """Test GET /api/patrocinadores does not accept mes/ano params (returns same data)"""
        # Get all patrocinadores
        response_all = requests.get(f"{BASE_URL}/api/patrocinadores", headers=headers)
        assert response_all.status_code == 200
        data_all = response_all.json()
        
        # Try with date params (should be ignored or return same data)
        response_filtered = requests.get(f"{BASE_URL}/api/patrocinadores?mes=6&ano=2024", headers=headers)
        assert response_filtered.status_code == 200
        data_filtered = response_filtered.json()
        
        # Both should return the same data (patrocinadores are not date-filtered)
        assert len(data_all) == len(data_filtered), "Patrocinadores should not be affected by date filters"
        print(f"Patrocinadores count (no filter): {len(data_all)}, (with date params): {len(data_filtered)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
