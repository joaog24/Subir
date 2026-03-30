import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import api from '../services/api';

const Login = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    senha: '',
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isLogin) {
        const response = await api.post('/auth/login', {
          email: formData.email,
          senha: formData.senha,
        });
        localStorage.setItem('ecp_token', response.data.access_token);
        setIsAuthenticated(true);
        toast.success('Login realizado com sucesso!');
        navigate('/');
      } else {
        await api.post('/auth/register', formData);
        toast.success('Conta criada com sucesso! Faça login.');
        setIsLogin(true);
        setFormData({ nome: '', email: '', senha: '' });
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao processar solicitação');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div 
      className="min-h-screen flex items-center justify-center p-4"
      style={{
        backgroundImage: 'url(https://customer-assets.emergentagent.com/job_piedade-sports/artifacts/k6ejao75_estadio.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <div className="absolute inset-0 bg-[#0A1F51]/80"></div>
      
      <Card className="relative z-10 w-full max-w-md p-8 shadow-2xl" data-testid="login-card">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <img 
              src="https://customer-assets.emergentagent.com/job_piedade-sports/artifacts/nuyr9yj4_logo.png" 
              alt="E.C.P Logo" 
              className="w-24 h-24 object-contain"
            />
          </div>
          <h1 className="text-3xl font-bold text-[#0A1F51] mb-2" data-testid="login-title">
            Esporte Clube Piedade
          </h1>
          <p className="text-[#FFC107] font-bold text-lg">Sistema de Gerenciamento</p>
          <p className="text-slate-600 mt-2">
            {isLogin ? 'Entre para gerenciar o clube' : 'Crie sua conta'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {!isLogin && (
            <div>
              <Label htmlFor="nome" className="text-sm font-semibold text-slate-700">
                Nome Completo
              </Label>
              <Input
                id="nome"
                type="text"
                data-testid="register-name-input"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                required
                className="mt-1.5 border-slate-300 focus:ring-2 focus:ring-[#0A1F51]"
              />
            </div>
          )}

          <div>
            <Label htmlFor="email" className="text-sm font-semibold text-slate-700">
              E-mail
            </Label>
            <Input
              id="email"
              type="email"
              data-testid="login-email-input"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              className="mt-1.5 border-slate-300 focus:ring-2 focus:ring-[#0A1F51]"
            />
          </div>

          <div>
            <Label htmlFor="senha" className="text-sm font-semibold text-slate-700">
              Senha
            </Label>
            <Input
              id="senha"
              type="password"
              data-testid="login-password-input"
              value={formData.senha}
              onChange={(e) => setFormData({ ...formData, senha: e.target.value })}
              required
              className="mt-1.5 border-slate-300 focus:ring-2 focus:ring-[#0A1F51]"
            />
          </div>

          <Button
            type="submit"
            data-testid="login-submit-button"
            disabled={loading}
            className="w-full bg-[#002B8C] hover:bg-[#0A1F51] text-white font-bold py-3 rounded-lg transition-all duration-200 hover:translate-y-[-1px]"
          >
            {loading ? 'Processando...' : isLogin ? 'Entrar' : 'Criar Conta'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <button
            type="button"
            data-testid="toggle-auth-mode"
            onClick={() => setIsLogin(!isLogin)}
            className="text-sm text-slate-600 hover:text-[#0A1F51] font-medium"
          >
            {isLogin ? 'Não tem conta? Cadastre-se' : 'Já tem conta? Faça login'}
          </button>
        </div>
      </Card>
    </div>
  );
};

export default Login;
