import React, { useState, useEffect } from 'react';
import { toast } from 'sonner';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '../components/ui/dropdown-menu';
import { Textarea } from '../components/ui/textarea';
import { Checkbox } from '../components/ui/checkbox';
import { Plus, MoreVertical, Pencil, Trash2, Users } from 'lucide-react';
import api from '../services/api';

const Treinos = () => {
  const [treinos, setTreinos] = useState([]);
  const [open, setOpen] = useState(false);
  const [presencaOpen, setPresencaOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [selectedTreino, setSelectedTreino] = useState(null);
  const [atletas, setAtletas] = useState([]);
  const [presencas, setPresencas] = useState([]);
  const [formData, setFormData] = useState({
    data: '',
    local: '',
    observacoes: '',
  });

  useEffect(() => {
    loadTreinos();
    loadAtletas();
  }, []);

  const loadTreinos = async () => {
    try {
      const response = await api.get('/treinos');
      setTreinos(response.data);
    } catch (error) {
      toast.error('Erro ao carregar treinos');
    }
  };

  const loadAtletas = async () => {
    try {
      const response = await api.get('/atletas');
      setAtletas(response.data.filter(a => a.ativo));
    } catch (error) {
      toast.error('Erro ao carregar atletas');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await api.put(`/treinos/${editingId}`, formData);
        toast.success('Treino atualizado com sucesso!');
      } else {
        await api.post('/treinos', formData);
        toast.success('Treino criado com sucesso!');
      }
      setOpen(false);
      resetForm();
      loadTreinos();
    } catch (error) {
      toast.error('Erro ao salvar treino');
    }
  };

  const handleEdit = (treino) => {
    setEditingId(treino.id);
    setFormData({
      data: treino.data,
      local: treino.local,
      observacoes: treino.observacoes,
    });
    setOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este treino?')) {
      try {
        await api.delete(`/treinos/${id}`);
        toast.success('Treino excluído com sucesso!');
        loadTreinos();
      } catch (error) {
        toast.error('Erro ao excluir treino');
      }
    }
  };

  const openPresenca = async (treino) => {
    setSelectedTreino(treino);
    try {
      const response = await api.get(`/presencas/treino/${treino.id}`);
      setPresencas(response.data);
      setPresencaOpen(true);
    } catch (error) {
      toast.error('Erro ao carregar presenças');
    }
  };

  const handlePresencaToggle = (atletaId) => {
    setPresencas(presencas.map(p => 
      p.atleta_id === atletaId ? { ...p, presente: !p.presente } : p
    ));
  };

  const savePresencas = async () => {
    try {
      await api.post('/presencas/bulk', {
        treino_id: selectedTreino.id,
        presencas: presencas.map(p => ({
          atleta_id: p.atleta_id,
          presente: p.presente,
        })),
      });
      toast.success('Presenças salvas com sucesso!');
      setPresencaOpen(false);
      loadTreinos();
    } catch (error) {
      toast.error('Erro ao salvar presenças');
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({ data: '', local: '', observacoes: '' });
  };

  return (
    <div className="space-y-6 fade-up" data-testid="treinos-page">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold text-slate-900 tracking-tight">Treinos</h1>
          <p className="text-slate-600 mt-1">Gerencie os treinos e presenças</p>
        </div>
        <Dialog open={open} onOpenChange={(val) => { setOpen(val); if (!val) resetForm(); }}>
          <DialogTrigger asChild>
            <Button className="bg-[#002B8C] hover:bg-[#0A1F51] text-white" data-testid="add-treino-button">
              <Plus className="w-4 h-4 mr-2" />
              Novo Treino
            </Button>
          </DialogTrigger>
          <DialogContent data-testid="treino-dialog">
            <DialogHeader>
              <DialogTitle>{editingId ? 'Editar Treino' : 'Novo Treino'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4" aria-describedby="treino-form-description">
              <p id="treino-form-description" className="sr-only">Preencha os dados do treino</p>
              <div>
                <Label htmlFor="data">Data</Label>
                <Input
                  id="data"
                  type="date"
                  data-testid="treino-data-input"
                  value={formData.data}
                  onChange={(e) => setFormData({ ...formData, data: e.target.value })}
                  required
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label htmlFor="local">Local</Label>
                <Input
                  id="local"
                  data-testid="treino-local-input"
                  value={formData.local}
                  onChange={(e) => setFormData({ ...formData, local: e.target.value })}
                  required
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label htmlFor="observacoes">Observações</Label>
                <Textarea
                  id="observacoes"
                  data-testid="treino-observacoes-input"
                  value={formData.observacoes}
                  onChange={(e) => setFormData({ ...formData, observacoes: e.target.value })}
                  className="mt-1.5"
                />
              </div>
              <Button type="submit" className="w-full bg-[#002B8C] hover:bg-[#0A1F51]" data-testid="treino-submit-button">
                {editingId ? 'Atualizar' : 'Criar'}
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
              <TableHead>Local</TableHead>
              <TableHead>Observações</TableHead>
              <TableHead>Presenças</TableHead>
              <TableHead className="text-right">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {treinos.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-slate-500">
                  Nenhum treino encontrado
                </TableCell>
              </TableRow>
            ) : (
              treinos.map((treino) => (
                <TableRow key={treino.id} data-testid={`treino-row-${treino.id}`}>
                  <TableCell className="font-medium">{new Date(treino.data).toLocaleDateString('pt-BR')}</TableCell>
                  <TableCell>{treino.local}</TableCell>
                  <TableCell>{treino.observacoes || '-'}</TableCell>
                  <TableCell>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => openPresenca(treino)}
                      data-testid={`presenca-button-${treino.id}`}
                    >
                      <Users className="w-4 h-4 mr-2" />
                      {treino.total_presencas} presentes
                    </Button>
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" data-testid={`treino-actions-${treino.id}`}>
                          <MoreVertical className="w-4 h-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => handleEdit(treino)} data-testid={`edit-treino-${treino.id}`}>
                          <Pencil className="w-4 h-4 mr-2" />
                          Editar
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleDelete(treino.id)} className="text-red-600" data-testid={`delete-treino-${treino.id}`}>
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

      {/* Presença Dialog */}
      <Dialog open={presencaOpen} onOpenChange={setPresencaOpen}>
        <DialogContent className="max-w-2xl" data-testid="presenca-dialog">
          <DialogHeader>
            <DialogTitle>Registrar Presenças</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {presencas.map((p) => (
              <div key={p.atleta_id} className="flex items-center justify-between p-3 border rounded-lg">
                <span className="font-medium">{p.atleta_nome}</span>
                <Checkbox
                  checked={p.presente}
                  onCheckedChange={() => handlePresencaToggle(p.atleta_id)}
                  data-testid={`presenca-checkbox-${p.atleta_id}`}
                />
              </div>
            ))}
          </div>
          <Button onClick={savePresencas} className="w-full bg-[#002B8C] hover:bg-[#0A1F51]" data-testid="save-presencas-button">
            Salvar Presenças
          </Button>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Treinos;
