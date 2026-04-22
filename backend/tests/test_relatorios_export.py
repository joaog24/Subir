"""
Test suite for Relatórios Export feature with date filters.
Tests export endpoints: /api/export/excel/{tipo} and /api/export/pdf/{tipo}
with optional ?mes=X&ano=Y query parameters.
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestAuth:
    """Authentication for export tests"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "diretoria@ecp.com.br",
            "senha": "ecp2024"
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        return response.json()["access_token"]
    
    def test_login_success(self):
        """Verify login works"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "diretoria@ecp.com.br",
            "senha": "ecp2024"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "diretoria@ecp.com.br"


class TestExcelExport:
    """Test Excel export endpoints with date filters"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "diretoria@ecp.com.br",
            "senha": "ecp2024"
        })
        return response.json()["access_token"]
    
    # Atletas - no date filter
    def test_export_excel_atletas_no_filter(self, auth_token):
        """Atletas export should work without filters"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/atletas",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in response.headers.get("content-type", "")
        assert len(response.content) > 0
    
    # Treinos - with various filters
    def test_export_excel_treinos_no_filter(self, auth_token):
        """Treinos export without filters - all data"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/treinos",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")
    
    def test_export_excel_treinos_year_filter(self, auth_token):
        """Treinos export with year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/treinos?ano=2024",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")
    
    def test_export_excel_treinos_month_year_filter(self, auth_token):
        """Treinos export with month and year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/treinos?ano=2025&mes=6",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")
    
    # Partidas - with various filters
    def test_export_excel_partidas_no_filter(self, auth_token):
        """Partidas export without filters"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/partidas",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")
    
    def test_export_excel_partidas_year_filter(self, auth_token):
        """Partidas export with year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/partidas?ano=2024",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")
    
    def test_export_excel_partidas_month_year_filter(self, auth_token):
        """Partidas export with month and year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/partidas?ano=2024&mes=3",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")
    
    # Financeiro - with various filters
    def test_export_excel_financeiro_no_filter(self, auth_token):
        """Financeiro export without filters"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/financeiro",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")
    
    def test_export_excel_financeiro_year_filter(self, auth_token):
        """Financeiro export with year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/financeiro?ano=2025",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")
    
    def test_export_excel_financeiro_month_year_filter(self, auth_token):
        """Financeiro export with month and year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/excel/financeiro?ano=2026&mes=1",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "spreadsheetml.sheet" in response.headers.get("content-type", "")


class TestPdfExport:
    """Test PDF export endpoints with date filters"""
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "diretoria@ecp.com.br",
            "senha": "ecp2024"
        })
        return response.json()["access_token"]
    
    # Atletas - no date filter
    def test_export_pdf_atletas_no_filter(self, auth_token):
        """Atletas PDF export should work without filters"""
        response = requests.get(
            f"{BASE_URL}/api/export/pdf/atletas",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("content-type", "")
        assert len(response.content) > 0
    
    # Treinos - with various filters
    def test_export_pdf_treinos_no_filter(self, auth_token):
        """Treinos PDF export without filters"""
        response = requests.get(
            f"{BASE_URL}/api/export/pdf/treinos",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("content-type", "")
    
    def test_export_pdf_treinos_year_filter(self, auth_token):
        """Treinos PDF export with year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/pdf/treinos?ano=2025",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("content-type", "")
    
    # Partidas - with various filters
    def test_export_pdf_partidas_no_filter(self, auth_token):
        """Partidas PDF export without filters"""
        response = requests.get(
            f"{BASE_URL}/api/export/pdf/partidas",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("content-type", "")
    
    def test_export_pdf_partidas_month_year_filter(self, auth_token):
        """Partidas PDF export with month and year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/pdf/partidas?ano=2024&mes=3",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("content-type", "")
    
    # Financeiro - with various filters
    def test_export_pdf_financeiro_no_filter(self, auth_token):
        """Financeiro PDF export without filters"""
        response = requests.get(
            f"{BASE_URL}/api/export/pdf/financeiro",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("content-type", "")
    
    def test_export_pdf_financeiro_year_filter(self, auth_token):
        """Financeiro PDF export with year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/pdf/financeiro?ano=2026",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("content-type", "")
    
    def test_export_pdf_financeiro_month_year_filter(self, auth_token):
        """Financeiro PDF export with month and year filter"""
        response = requests.get(
            f"{BASE_URL}/api/export/pdf/financeiro?ano=2026&mes=1",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("content-type", "")


class TestExportUnauthorized:
    """Test that export endpoints require authentication"""
    
    def test_export_excel_unauthorized(self):
        """Excel export should require auth"""
        response = requests.get(f"{BASE_URL}/api/export/excel/atletas")
        assert response.status_code in [401, 403]
    
    def test_export_pdf_unauthorized(self):
        """PDF export should require auth"""
        response = requests.get(f"{BASE_URL}/api/export/pdf/atletas")
        assert response.status_code in [401, 403]
