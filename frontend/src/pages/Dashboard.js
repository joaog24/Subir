import React, { useState, useEffect } from 'react';
import { toast } from 'sonner';
import { Card } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Users, Dumbbell, Trophy, TrendingUp, TrendingDown, DollarSign } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [charts, setCharts] = useState(null);
  const [mes, setMes] = useState(null);
  const [ano, setAno] = useState(new Date().getFullYear());
  const [loading, setLoading] = useState(true);

  const meses = [
    { value: null, label: 'Todos' },
    { value: 1, label: 'Janeiro' },
    { value: 2, label: 'Fevereiro' },
    { value: 3, label: 'Março' },
    { value: 4, label: 'Abril' },
    { value: 5, label: 'Maio' },
    { value: 6, label: 'Junho' },
    { value: 7, label: 'Julho' },
    { value: 8, label: 'Agosto' },
    { value: 9, label: 'Setembro' },
    { value: 10, label: 'Outubro' },
    { value: 11, label: 'Novembro' },
    { value: 12, label: 'Dezembro' },
  ];

  const anos = [2024, 2025, 2026];

  useEffect(() => {
    loadData();
  }, [mes, ano]);

  const loadData = async () => {
    try {
      setLoading(true);
      const params = mes ? `?mes=${mes}&ano=${ano}` : '';
      const statsRes = await api.get(`/dashboard/stats${params}`);
      setStats(statsRes.data);

      const chartsRes = await api.get(`/dashboard/charts?ano=${ano}`);
      setCharts(chartsRes.data);
    } catch (error) {
      toast.error('Erro ao carregar dados do dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading || !stats || !charts) {
    return (
      <div className="flex items-center justify-center h-64" data-testid="dashboard-loading">
        <p className="text-slate-500">Carregando...</p>
      </div>
    );
  }

  const kpiCards = [
    { label: 'Atletas Ativos', value: stats.total_atletas_ativos, icon: Users, color: 'bg-[#002B8C]' },
    { label: 'Treinos Realizados', value: stats.total_treinos, icon: Dumbbell, color: 'bg-[#28A745]' },
    { label: 'Partidas', value: stats.total_partidas, icon: Trophy, color: 'bg-[#0A1F51]' },
    { label: 'Receitas', value: `R$ ${stats.total_receitas.toFixed(2)}`, icon: TrendingUp, color: 'bg-[#28A745]', valueColor: 'text-[#28A745]' },
    { label: 'Despesas', value: `R$ ${stats.total_despesas.toFixed(2)}`, icon: TrendingDown, color: 'bg-[#DC3545]', valueColor: 'text-[#DC3545]' },
    { label: 'Saldo', value: `R$ ${stats.saldo.toFixed(2)}`, icon: DollarSign, color: stats.saldo >= 0 ? 'bg-[#28A745]' : 'bg-[#DC3545]', valueColor: stats.saldo >= 0 ? 'text-[#28A745]' : 'text-[#DC3545]' },
  ];

  const mesesNomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  
  const financeiroData = charts.financeiro_mensal.map(item => ({
    mes: mesesNomes[item.mes - 1],
    Receitas: item.receitas,
    Despesas: item.despesas,
  }));

  const treinosData = charts.treinos_mensal.map(item => ({
    mes: mesesNomes[item.mes - 1],
    treinos: item.total,
  }));

  const resultadosData = [
    { name: 'Vitórias', value: charts.resultados.vitorias, color: '#28A745' },
    { name: 'Empates', value: charts.resultados.empates, color: '#FFC107' },
    { name: 'Derrotas', value: charts.resultados.derrotas, color: '#DC3545' },
  ];

  return (
    <div className="space-y-6 fade-up" data-testid="dashboard">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold text-slate-900 tracking-tight">Dashboard</h1>
          <p className="text-slate-600 mt-1">Visão geral do clube</p>
        </div>
        <div className="flex gap-3">
          <Select value={mes?.toString() || 'null'} onValueChange={(val) => setMes(val === 'null' ? null : parseInt(val))}>
            <SelectTrigger className="w-40" data-testid="month-filter">
              <SelectValue placeholder="Mês" />
            </SelectTrigger>
            <SelectContent>
              {meses.map((m) => (
                <SelectItem key={m.value || 'null'} value={m.value?.toString() || 'null'}>
                  {m.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={ano.toString()} onValueChange={(val) => setAno(parseInt(val))}>
            <SelectTrigger className="w-32" data-testid="year-filter">
              <SelectValue placeholder="Ano" />
            </SelectTrigger>
            <SelectContent>
              {anos.map((a) => (
                <SelectItem key={a} value={a.toString()}>
                  {a}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {kpiCards.map((card, index) => {
          const Icon = card.icon;
          return (
            <Card key={index} className="p-6 shadow-sm hover:shadow-md transition-shadow duration-200" data-testid={`kpi-${card.label.toLowerCase().replace(/\s/g, '-')}`}>
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-500 uppercase tracking-wide">{card.label}</p>
                  <p className={`text-3xl font-bold mt-2 ${card.valueColor || 'text-slate-900'}`}>{card.value}</p>
                </div>
                <div className={`${card.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Financeiro */}
        <Card className="p-6 shadow-sm" data-testid="chart-financeiro">
          <h3 className="text-xl font-semibold text-slate-800 mb-4">Receitas vs Despesas</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={financeiroData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
              <XAxis dataKey="mes" stroke="#64748B" />
              <YAxis stroke="#64748B" />
              <Tooltip contentStyle={{ backgroundColor: '#0A192F', border: 'none', borderRadius: '8px', color: '#fff' }} />
              <Legend />
              <Bar dataKey="Receitas" fill="#28A745" radius={[8, 8, 0, 0]} />
              <Bar dataKey="Despesas" fill="#DC3545" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Treinos */}
        <Card className="p-6 shadow-sm" data-testid="chart-treinos">
          <h3 className="text-xl font-semibold text-slate-800 mb-4">Treinos por Mês</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={treinosData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
              <XAxis dataKey="mes" stroke="#64748B" />
              <YAxis stroke="#64748B" />
              <Tooltip contentStyle={{ backgroundColor: '#0A192F', border: 'none', borderRadius: '8px', color: '#fff' }} />
              <Legend />
              <Line type="monotone" dataKey="treinos" stroke="#002B8C" strokeWidth={3} dot={{ fill: '#FFC107', r: 5 }} />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Resultados */}
      <Card className="p-6 shadow-sm" data-testid="chart-resultados">
        <h3 className="text-xl font-semibold text-slate-800 mb-4">Resultados das Partidas</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={resultadosData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {resultadosData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip contentStyle={{ backgroundColor: '#0A192F', border: 'none', borderRadius: '8px', color: '#fff' }} />
          </PieChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );
};

export default Dashboard;
