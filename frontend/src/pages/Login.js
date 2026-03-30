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
        backgroundImage: 'url(https://images.pexels.com/photos/4328745/pexels-photo-4328745.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <div className="absolute inset-0 bg-[#0A192F]/85"></div>
      
      <Card className="relative z-10 w-full max-w-md p-8 shadow-2xl" data-testid="login-card">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-[#0A192F] mb-2" data-testid="login-title">
            E.C.P Manager
          </h1>
          <p className="text-[#FACC15] font-semibold text-lg">Esporte Clube Piedade</p>
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
                className="mt-1.5 border-slate-300 focus:ring-2 focus:ring-[#0A192F]"
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
              className="mt-1.5 border-slate-300 focus:ring-2 focus:ring-[#0A192F]"
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
              className="mt-1.5 border-slate-300 focus:ring-2 focus:ring-[#0A192F]"
            />
          </div>

          <Button
            type="submit"
            data-testid="login-submit-button"
            disabled={loading}
            className="w-full bg-[#0A192F] hover:bg-[#112240] text-white font-bold py-3 rounded-lg transition-all duration-200 hover:translate-y-[-1px]"
          >
            {loading ? 'Processando...' : isLogin ? 'Entrar' : 'Criar Conta'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <button
            type="button"
            data-testid="toggle-auth-mode"
            onClick={() => setIsLogin(!isLogin)}
            className="text-sm text-slate-600 hover:text-[#0A192F] font-medium"
          >
            {isLogin ? 'Não tem conta? Cadastre-se' : 'Já tem conta? Faça login'}
          </button>
        </div>
      </Card>
    </div>
  );
};

export default Login;
