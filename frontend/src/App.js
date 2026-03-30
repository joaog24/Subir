import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from './components/ui/sonner';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Atletas from './pages/Atletas';
import Treinos from './pages/Treinos';
import Partidas from './pages/Partidas';
import Financeiro from './pages/Financeiro';
import Relatorios from './pages/Relatorios';
import Layout from './components/Layout';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('ecp_token');
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  const PrivateRoute = ({ children }) => {
    if (loading) return <div>Carregando...</div>;
    return isAuthenticated ? children : <Navigate to="/login" />;
  };

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Layout setIsAuthenticated={setIsAuthenticated}>
                  <Dashboard />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/atletas"
            element={
              <PrivateRoute>
                <Layout setIsAuthenticated={setIsAuthenticated}>
                  <Atletas />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/treinos"
            element={
              <PrivateRoute>
                <Layout setIsAuthenticated={setIsAuthenticated}>
                  <Treinos />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/partidas"
            element={
              <PrivateRoute>
                <Layout setIsAuthenticated={setIsAuthenticated}>
                  <Partidas />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/financeiro"
            element={
              <PrivateRoute>
                <Layout setIsAuthenticated={setIsAuthenticated}>
                  <Financeiro />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/relatorios"
            element={
              <PrivateRoute>
                <Layout setIsAuthenticated={setIsAuthenticated}>
                  <Relatorios />
                </Layout>
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" richColors />
    </div>
  );
}

export default App;
