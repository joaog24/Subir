import React, { useState, useEffect } from 'react';
import { toast } from 'sonner';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '../components/ui/dropdown-menu';
import { Badge } from '../components/ui/badge';
import { Plus, MoreVertical, Pencil, Trash2 } from 'lucide-react';
import api from '../services/api';

const Partidas = () => {
  const [partidas, setPartidas] = useState([]);
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    data: '',
    adversario: '',
    local: '',
    gols_clube: 0,
    gols_adversario: 0,
  });

  useEffect(() => {
    loadPartidas();
  }, []);

  const loadPartidas = async () => {
    try {
      const response = await api.get('/partidas');
      setPartidas(response.data);
    } catch (error) {
      toast.error('Erro ao carregar partidas');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await api.put(`/partidas/${editingId}`, formData);
        toast.success('Partida atualizada com sucesso!');
      } else {
        await api.post('/partidas', formData);
        toast.success('Partida registrada com sucesso!');
      }
      setOpen(false);
      resetForm();
      loadPartidas();
    } catch (error) {
      toast.error('Erro ao salvar partida');
    }
  };

  const handleEdit = (partida) => {
    setEditingId(partida.id);
    setFormData({
      data: partida.data,
      adversario: partida.adversario,
      local: partida.local,
      gols_clube: partida.gols_clube,
      gols_adversario: partida.gols_adversario,
    });
    setOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta partida?')) {
      try {
        await api.delete(`/partidas/${id}`);
        toast.success('Partida excluída com sucesso!');
        loadPartidas();
      } catch (error) {
        toast.error('Erro ao excluir partida');
      }
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({ data: '', adversario: '', local: '', gols_clube: 0, gols_adversario: 0 });
  };

  const getResultadoBadge = (resultado) => {
    const configs = {
      'Vitória': { color: 'bg-[#28A745] text-white', variant: 'default' },
      'Empate': { color: 'bg-[#FFC107] text-[#0A1F51]', variant: 'secondary' },
      'Derrota': { color: 'bg-[#DC3545] text-white', variant: 'destructive' },
    };
    const config = configs[resultado] || configs['Empate'];
    return <Badge className={config.color}>{resultado}</Badge>;
  };

  return (
    <div className="space-y-6 fade-up" data-testid="partidas-page">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold text-slate-900 tracking-tight">Partidas</h1>
          <p className="text-slate-600 mt-1">Registre os jogos do clube</p>
        </div>
        <Dialog open={open} onOpenChange={(val) => { setOpen(val); if (!val) resetForm(); }}>
          <DialogTrigger asChild>
            <Button className="bg-[#002B8C] hover:bg-[#0A1F51] text-white" data-testid="add-partida-button">
              <Plus className="w-4 h-4 mr-2" />
              Nova Partida
            </Button>
          </DialogTrigger>
          <DialogContent data-testid="partida-dialog">
            <DialogHeader>
              <DialogTitle>{editingId ? 'Editar Partida' : 'Nova Partida'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4" aria-describedby="partida-form-description">
              <p id="partida-form-description" className="sr-only">Preencha os dados da partida</p>
              <div>
                <Label htmlFor="data">Data</Label>
                <Input
                  id="data"
                  type="date"
                  data-testid="partida-data-input"
                  value={formData.data}
                  onChange={(e) => setFormData({ ...formData, data: e.target.value })}
                  required
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label htmlFor="adversario">Adversário</Label>
                <Input
                  id="adversario"
                  data-testid="partida-adversario-input"
                  value={formData.adversario}
                  onChange={(e) => setFormData({ ...formData, adversario: e.target.value })}
                  required
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label htmlFor="local">Local</Label>
                <Input
                  id="local"
                  data-testid="partida-local-input"
                  value={formData.local}
                  onChange={(e) => setFormData({ ...formData, local: e.target.value })}
                  required
                  className="mt-1.5"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="gols_clube">Gols E.C.P</Label>
                  <Input
                    id="gols_clube"
                    type="number"
                    min="0"
                    data-testid="partida-gols-clube-input"
                    value={formData.gols_clube}
                    onChange={(e) => setFormData({ ...formData, gols_clube: parseInt(e.target.value) || 0 })}
                    required
                    className="mt-1.5"
                  />
                </div>
                <div>
                  <Label htmlFor="gols_adversario">Gols Adversário</Label>
                  <Input
                    id="gols_adversario"
                    type="number"
                    min="0"
                    data-testid="partida-gols-adversario-input"
                    value={formData.gols_adversario}
                    onChange={(e) => setFormData({ ...formData, gols_adversario: parseInt(e.target.value) || 0 })}
                    required
                    className="mt-1.5"
                  />
                </div>
              </div>
              <Button type="submit" className="w-full bg-[#002B8C] hover:bg-[#0A1F51]" data-testid="partida-submit-button">
                {editingId ? 'Atualizar' : 'Registrar'}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Table */}
      <Card className="shadow-sm">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Data</TableHead>
              <TableHead>Adversário</TableHead>
              <TableHead>Local</TableHead>
              <TableHead>Placar</TableHead>
              <TableHead>Resultado</TableHead>
              <TableHead className="text-right">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {partidas.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center text-slate-500">
                  Nenhuma partida encontrada
                </TableCell>
              </TableRow>
            ) : (
              partidas.map((partida) => (
                <TableRow key={partida.id} data-testid={`partida-row-${partida.id}`}>
                  <TableCell className="font-medium">{new Date(partida.data).toLocaleDateString('pt-BR')}</TableCell>
                  <TableCell>{partida.adversario}</TableCell>
                  <TableCell>{partida.local}</TableCell>
                  <TableCell className="font-bold">
                    {partida.gols_clube} x {partida.gols_adversario}
                  </TableCell>
                  <TableCell>{getResultadoBadge(partida.resultado)}</TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" data-testid={`partida-actions-${partida.id}`}>
                          <MoreVertical className="w-4 h-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => handleEdit(partida)} data-testid={`edit-partida-${partida.id}`}>
                          <Pencil className="w-4 h-4 mr-2" />
                          Editar
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleDelete(partida.id)} className="text-red-600" data-testid={`delete-partida-${partida.id}`}>
                          <Trash2 className="w-4 h-4 mr-2" />
                          Excluir
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
};

export default Partidas;
