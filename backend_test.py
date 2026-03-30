import requests
import sys
from datetime import datetime
import json

class ECPManagerAPITester:
    def __init__(self, base_url="https://piedade-sports.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "status": "PASSED" if success else "FAILED",
            "details": details
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=30)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if not success:
                try:
                    error_data = response.json()
                    details += f", Error: {error_data.get('detail', 'Unknown error')}"
                except:
                    details += f", Response: {response.text[:200]}"

            self.log_test(name, success, details)
            
            if success:
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                return False, {}

        except Exception as e:
            self.log_test(name, False, f"Exception: {str(e)}")
            return False, {}

    def test_auth(self):
        """Test authentication endpoints"""
        print("\n🔐 Testing Authentication...")
        
        # Test login with correct credentials
        success, response = self.run_test(
            "Login with valid credentials",
            "POST",
            "auth/login",
            200,
            data={"email": "diretoria@ecp.com.br", "senha": "ecp2024"}
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            print(f"   Token obtained: {self.token[:20]}...")
        else:
            print("   ❌ Failed to get authentication token")
            return False

        # Test login with invalid credentials
        self.run_test(
            "Login with invalid credentials",
            "POST",
            "auth/login",
            401,
            data={"email": "wrong@email.com", "senha": "wrongpass"}
        )

        # Test get current user
        self.run_test(
            "Get current user info",
            "GET",
            "auth/me",
            200
        )

        return True

    def test_atletas(self):
        """Test athletes CRUD operations"""
        print("\n👥 Testing Athletes...")
        
        # List athletes
        success, athletes = self.run_test("List athletes", "GET", "atletas", 200)
        
        # Create athlete
        athlete_data = {
            "nome": "João Silva Test",
            "posicao": "Atacante",
            "telefone": "(11) 99999-9999",
            "ativo": True
        }
        success, created = self.run_test("Create athlete", "POST", "atletas", 200, athlete_data)
        
        if success and 'id' in created:
            athlete_id = created['id']
            
            # Get specific athlete
            self.run_test(f"Get athlete {athlete_id}", "GET", f"atletas/{athlete_id}", 200)
            
            # Update athlete
            update_data = {**athlete_data, "posicao": "Meio-campo"}
            self.run_test(f"Update athlete {athlete_id}", "PUT", f"atletas/{athlete_id}", 200, update_data)
            
            # Delete athlete
            self.run_test(f"Delete athlete {athlete_id}", "DELETE", f"atletas/{athlete_id}", 200)

    def test_treinos(self):
        """Test training CRUD operations"""
        print("\n🏋️ Testing Training...")
        
        # List training sessions
        self.run_test("List training sessions", "GET", "treinos", 200)
        
        # Create training
        training_data = {
            "data": "2024-12-01",
            "local": "Campo Principal",
            "observacoes": "Treino de teste"
        }
        success, created = self.run_test("Create training", "POST", "treinos", 200, training_data)
        
        if success and 'id' in created:
            training_id = created['id']
            
            # Get specific training
            self.run_test(f"Get training {training_id}", "GET", f"treinos/{training_id}", 200)
            
            # Update training
            update_data = {**training_data, "local": "Campo Secundário"}
            self.run_test(f"Update training {training_id}", "PUT", f"treinos/{training_id}", 200, update_data)
            
            # Test attendance endpoints
            self.run_test(f"Get training attendance {training_id}", "GET", f"presencas/treino/{training_id}", 200)
            
            # Delete training
            self.run_test(f"Delete training {training_id}", "DELETE", f"treinos/{training_id}", 200)

    def test_partidas(self):
        """Test matches CRUD operations"""
        print("\n🏆 Testing Matches...")
        
        # List matches
        self.run_test("List matches", "GET", "partidas", 200)
        
        # Create match
        match_data = {
            "data": "2024-12-01",
            "adversario": "Time Teste FC",
            "local": "Casa",
            "gols_clube": 2,
            "gols_adversario": 1
        }
        success, created = self.run_test("Create match", "POST", "partidas", 200, match_data)
        
        if success and 'id' in created:
            match_id = created['id']
            
            # Get specific match
            self.run_test(f"Get match {match_id}", "GET", f"partidas/{match_id}", 200)
            
            # Update match
            update_data = {**match_data, "gols_clube": 3}
            self.run_test(f"Update match {match_id}", "PUT", f"partidas/{match_id}", 200, update_data)
            
            # Delete match
            self.run_test(f"Delete match {match_id}", "DELETE", f"partidas/{match_id}", 200)

    def test_financeiro(self):
        """Test financial operations"""
        print("\n💰 Testing Financial...")
        
        # Test sponsors
        self.run_test("List sponsors", "GET", "patrocinadores", 200)
        
        sponsor_data = {
            "nome": "Empresa Teste LTDA",
            "tipo": "Principal",
            "contato": "contato@teste.com",
            "ativo": True
        }
        success, sponsor = self.run_test("Create sponsor", "POST", "patrocinadores", 200, sponsor_data)
        
        # Test revenues
        self.run_test("List revenues", "GET", "recebimentos", 200)
        
        revenue_data = {
            "descricao": "Patrocínio Teste",
            "valor": 1000.50,
            "data": "2024-12-01",
            "patrocinador_id": sponsor.get('id') if sponsor else None
        }
        success, revenue = self.run_test("Create revenue", "POST", "recebimentos", 200, revenue_data)
        
        # Test expenses
        self.run_test("List expenses", "GET", "despesas", 200)
        
        expense_data = {
            "descricao": "Material Esportivo",
            "categoria": "Equipamentos",
            "valor": 500.00,
            "data": "2024-12-01"
        }
        success, expense = self.run_test("Create expense", "POST", "despesas", 200, expense_data)
        
        # Clean up
        if revenue and 'id' in revenue:
            self.run_test(f"Delete revenue {revenue['id']}", "DELETE", f"recebimentos/{revenue['id']}", 200)
        if expense and 'id' in expense:
            self.run_test(f"Delete expense {expense['id']}", "DELETE", f"despesas/{expense['id']}", 200)
        if sponsor and 'id' in sponsor:
            self.run_test(f"Delete sponsor {sponsor['id']}", "DELETE", f"patrocinadores/{sponsor['id']}", 200)

    def test_dashboard(self):
        """Test dashboard endpoints"""
        print("\n📊 Testing Dashboard...")
        
        # Test dashboard stats
        self.run_test("Get dashboard stats", "GET", "dashboard/stats", 200)
        self.run_test("Get dashboard stats with filters", "GET", "dashboard/stats?mes=12&ano=2024", 200)
        
        # Test dashboard charts
        self.run_test("Get dashboard charts", "GET", "dashboard/charts?ano=2024", 200)

    def test_exports(self):
        """Test export functionality"""
        print("\n📄 Testing Exports...")
        
        export_types = ['atletas', 'treinos', 'partidas', 'financeiro']
        
        for export_type in export_types:
            # Test Excel export
            self.run_test(f"Export {export_type} to Excel", "GET", f"export/excel/{export_type}", 200)
            
            # Test PDF export (only for supported types)
            if export_type in ['atletas', 'partidas', 'financeiro']:
                self.run_test(f"Export {export_type} to PDF", "GET", f"export/pdf/{export_type}", 200)

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting E.C.P Manager API Tests...")
        print(f"Testing against: {self.base_url}")
        
        # Test authentication first
        if not self.test_auth():
            print("❌ Authentication failed - stopping tests")
            return False
        
        # Run all other tests
        self.test_atletas()
        self.test_treinos()
        self.test_partidas()
        self.test_financeiro()
        self.test_dashboard()
        self.test_exports()
        
        # Print summary
        print(f"\n📊 Test Summary:")
        print(f"   Total tests: {self.tests_run}")
        print(f"   Passed: {self.tests_passed}")
        print(f"   Failed: {self.tests_run - self.tests_passed}")
        print(f"   Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    tester = ECPManagerAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())