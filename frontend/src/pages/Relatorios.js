import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { FileText, Download, Calendar } from 'lucide-react';
import { toast } from 'sonner';

const meses = [
  { value: 'null', label: 'Todos' },
  { value: '1', label: 'Janeiro' },
  { value: '2', label: 'Fevereiro' },
  { value: '3', label: 'Março' },
  { value: '4', label: 'Abril' },
  { value: '5', label: 'Maio' },
  { value: '6', label: 'Junho' },
  { value: '7', label: 'Julho' },
  { value: '8', label: 'Agosto' },
  { value: '9', label: 'Setembro' },
  { value: '10', label: 'Outubro' },
  { value: '11', label: 'Novembro' },
  { value: '12', label: 'Dezembro' },
];

const anos = [
  { value: 'null', label: 'Todos' },
  { value: '2024', label: '2024' },
  { value: '2025', label: '2025' },
  { value: '2026', label: '2026' },
];

const relatorios = [
  {
    titulo: 'Relatório de Atletas',
    descricao: 'Lista completa de atletas com posições e status',
    tipo: 'atletas',
    temFiltro: false,
  },
  {
    titulo: 'Relatório de Treinos',
    descricao: 'Histórico de treinos realizados com presenças',
    tipo: 'treinos',
    temFiltro: true,
  },
  {
    titulo: 'Relatório de Partidas',
    descricao: 'Registro de todas as partidas e resultados',
    tipo: 'partidas',
    temFiltro: true,
  },
  {
    titulo: 'Relatório Financeiro',
    descricao: 'Movimentações financeiras: receitas e despesas',
    tipo: 'financeiro',
    temFiltro: true,
  },
];

const ReportCard = ({ rel }) => {
  const [mes, setMes] = useState('null');
  const [ano, setAno] = useState('null');

  const handleExport = async (formato) => {
    try {
      const token = localStorage.getItem('ecp_token');
      const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

      const params = new URLSearchParams();
      if (ano !== 'null') params.append('ano', ano);
      if (mes !== 'null' && ano !== 'null') params.append('mes', mes);
      const queryStr = params.toString() ? `?${params.toString()}` : '';

      const url = `${BACKEND_URL}/api/export/${formato}/${rel.tipo}${queryStr}`;

      const response = await fetch(url, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (!response.ok) throw new Error('Erro ao exportar');

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `ecp_${rel.tipo}.${formato === 'excel' ? 'xlsx' : 'pdf'}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(downloadUrl);

      toast.success('Relatório exportado com sucesso!');
    } catch (error) {
      toast.error('Erro ao exportar relatório');
    }
  };

  const getPeriodoLabel = () => {
    if (ano === 'null') return 'Todos os períodos';
    const mesLabel = mes !== 'null' ? meses.find(m => m.value === mes)?.label : null;
    return mesLabel ? `${mesLabel}/${ano}` : `Ano ${ano}`;
  };

  return (
    <Card className="p-6 shadow-sm hover:shadow-md transition-shadow duration-200" data-testid={`relatorio-${rel.tipo}`}>
      <div className="space-y-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-800">{rel.titulo}</h3>
          <p className="text-slate-500 text-sm mt-1">{rel.descricao}</p>
        </div>

        {rel.temFiltro && (
          <div className="flex items-center gap-3 pt-1">
            <Calendar className="w-4 h-4 text-slate-400 flex-shrink-0" />
            <Select value={ano} onValueChange={(val) => { setAno(val); if (val === 'null') setMes('null'); }}>
              <SelectTrigger className="w-28 h-9 text-sm" data-testid={`relatorio-${rel.tipo}-ano`}>
                <SelectValue placeholder="Ano" />
              </SelectTrigger>
              <SelectContent>
                {anos.map(a => (
                  <SelectItem key={a.value} value={a.value}>{a.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={mes} onValueChange={setMes} disabled={ano === 'null'}>
              <SelectTrigger className="w-32 h-9 text-sm" data-testid={`relatorio-${rel.tipo}-mes`}>
                <SelectValue placeholder="Mês" />
              </SelectTrigger>
              <SelectContent>
                {meses.map(m => (
                  <SelectItem key={m.value} value={m.value}>{m.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        <div className="flex items-center justify-between pt-1">
          <span className="text-xs text-slate-400" data-testid={`relatorio-${rel.tipo}-periodo`}>
            {rel.temFiltro ? getPeriodoLabel() : 'Cadastro completo'}
          </span>
          <div className="flex gap-2">
            <Button
              onClick={() => handleExport('excel')}
              variant="outline"
              size="sm"
              className="border-emerald-600 text-emerald-600 hover:bg-emerald-50 h-8 text-xs"
              data-testid={`export-excel-${rel.tipo}`}
            >
              <Download className="w-3.5 h-3.5 mr-1.5" />
              Excel
            </Button>
            <Button
              onClick={() => handleExport('pdf')}
              variant="outline"
              size="sm"
              className="border-red-600 text-red-600 hover:bg-red-50 h-8 text-xs"
              data-testid={`export-pdf-${rel.tipo}`}
            >
              <FileText className="w-3.5 h-3.5 mr-1.5" />
              PDF
            </Button>
          </div>
        </div>
      </div>
    </Card>
  );
};

const Relatorios = () => {
  return (
    <div className="space-y-6 fade-up" data-testid="relatorios-page">
      <div>
        <h1 className="text-4xl font-bold text-slate-900 tracking-tight">Relatórios</h1>
        <p className="text-slate-600 mt-1">Exporte dados do sistema em Excel ou PDF</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {relatorios.map((rel) => (
          <ReportCard key={rel.tipo} rel={rel} />
        ))}
      </div>

      <Card className="p-6 bg-blue-50 border-blue-200">
        <div className="flex gap-3">
          <FileText className="w-6 h-6 text-blue-600 flex-shrink-0" />
          <div>
            <h4 className="font-semibold text-blue-900 mb-1">Sobre os relatórios</h4>
            <p className="text-blue-800 text-sm">
              Os relatórios são gerados em tempo real com os dados mais atualizados do sistema.
              Selecione o ano e mês desejado ou exporte todos os dados de uma vez.
              Escolha o formato Excel para análise de dados ou PDF para impressão.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Relatorios;
