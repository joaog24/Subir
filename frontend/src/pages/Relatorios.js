import React from 'react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { FileText, Download } from 'lucide-react';
import { toast } from 'sonner';
import api from '../services/api';

const Relatorios = () => {
  const handleExport = async (tipo, formato) => {
    try {
      const token = localStorage.getItem('ecp_token');
      const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
      const url = `${BACKEND_URL}/api/export/${formato}/${tipo}`;
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) throw new Error('Erro ao exportar');

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `ecp_${tipo}.${formato === 'excel' ? 'xlsx' : 'pdf'}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(downloadUrl);

      toast.success('Relatório exportado com sucesso!');
    } catch (error) {
      toast.error('Erro ao exportar relatório');
    }
  };

  const relatorios = [
    {
      titulo: 'Relatório de Atletas',
      descricao: 'Lista completa de atletas com posições e status',
      tipo: 'atletas',
      icon: '👥',
    },
    {
      titulo: 'Relatório de Treinos',
      descricao: 'Histórico de treinos realizados com presenças',
      tipo: 'treinos',
      icon: '🏋️',
    },
    {
      titulo: 'Relatório de Partidas',
      descricao: 'Registro de todas as partidas e resultados',
      tipo: 'partidas',
      icon: '🏆',
    },
    {
      titulo: 'Relatório Financeiro',
      descricao: 'Movimentações financeiras: receitas e despesas',
      tipo: 'financeiro',
      icon: '💰',
    },
  ];

  return (
    <div className="space-y-6 fade-up" data-testid="relatorios-page">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-slate-900 tracking-tight">Relatórios</h1>
        <p className="text-slate-600 mt-1">Exporte dados do sistema em Excel ou PDF</p>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {relatorios.map((rel) => (
          <Card key={rel.tipo} className="p-6 shadow-sm hover:shadow-md transition-shadow duration-200" data-testid={`relatorio-${rel.tipo}`}>
            <div className="flex items-start gap-4">
              <div className="text-4xl">{rel.icon}</div>
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-slate-800 mb-2">{rel.titulo}</h3>
                <p className="text-slate-600 text-sm mb-4">{rel.descricao}</p>
                <div className="flex gap-3">
                  <Button
                    onClick={() => handleExport(rel.tipo, 'excel')}
                    variant="outline"
                    size="sm"
                    className="border-emerald-600 text-emerald-600 hover:bg-emerald-50"
                    data-testid={`export-excel-${rel.tipo}`}
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Excel
                  </Button>
                  <Button
                    onClick={() => handleExport(rel.tipo, 'pdf')}
                    variant="outline"
                    size="sm"
                    className="border-red-600 text-red-600 hover:bg-red-50"
                    data-testid={`export-pdf-${rel.tipo}`}
                  >
                    <FileText className="w-4 h-4 mr-2" />
                    PDF
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Info Card */}
      <Card className="p-6 bg-blue-50 border-blue-200">
        <div className="flex gap-3">
          <FileText className="w-6 h-6 text-blue-600 flex-shrink-0" />
          <div>
            <h4 className="font-semibold text-blue-900 mb-1">Sobre os relatórios</h4>
            <p className="text-blue-800 text-sm">
              Os relatórios são gerados em tempo real com os dados mais atualizados do sistema.
              Escolha o formato Excel para análise de dados ou PDF para impressão e apresentação.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Relatorios;
