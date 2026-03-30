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
import { Plus, MoreVertical, Pencil, Trash2, Search } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import api from '../services/api';

const Atletas = () => {
  const [atletas, setAtletas] = useState([]);
  const [filteredAtletas, setFilteredAtletas] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    nome: '',
    posicao: '',
    telefone: '',
    ativo: true,
  });

  useEffect(() => {
    loadAtletas();
  }, []);

  useEffect(() => {
    const filtered = atletas.filter((a) =>
      a.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.posicao.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredAtletas(filtered);
  }, [searchTerm, atletas]);

  const loadAtletas = async () => {
    try {
      const response = await api.get('/atletas');
      setAtletas(response.data);
      setFilteredAtletas(response.data);
    } catch (error) {
      toast.error('Erro ao carregar atletas');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await api.put(`/atletas/${editingId}`, formData);
        toast.success('Atleta atualizado com sucesso!');
      } else {
        await api.post('/atletas', formData);
        toast.success('Atleta criado com sucesso!');
      }
      setOpen(false);
      resetForm();
      loadAtletas();
    } catch (error) {
      toast.error('Erro ao salvar atleta');
    }
  };

  const handleEdit = (atleta) => {
    setEditingId(atleta.id);
    setFormData({
      nome: atleta.nome,
      posicao: atleta.posicao,
      telefone: atleta.telefone,
      ativo: atleta.ativo,
    });
    setOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este atleta?')) {
      try {
        await api.delete(`/atletas/${id}`);
        toast.success('Atleta excluído com sucesso!');
        loadAtletas();
      } catch (error) {
        toast.error('Erro ao excluir atleta');
      }
    }
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({ nome: '', posicao: '', telefone: '', ativo: true });
  };

  return (
    <div className="space-y-6 fade-up" data-testid="atletas-page">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold text-slate-900 tracking-tight">Atletas</h1>
          <p className="text-slate-600 mt-1">Gerencie os atletas do clube</p>
        </div>
        <Dialog open={open} onOpenChange={(val) => { setOpen(val); if (!val) resetForm(); }}>
          <DialogTrigger asChild>
            <Button className="bg-[#0A192F] hover:bg-[#112240] text-white" data-testid="add-atleta-button">
              <Plus className="w-4 h-4 mr-2" />
              Novo Atleta
            </Button>
          </DialogTrigger>
          <DialogContent data-testid="atleta-dialog">
            <DialogHeader>
              <DialogTitle>{editingId ? 'Editar Atleta' : 'Novo Atleta'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4" aria-describedby="atleta-form-description">
              <p id="atleta-form-description" className="sr-only">Preencha os dados do atleta</p>
              <div>
                <Label htmlFor="nome">Nome</Label>
                <Input
                  id="nome"
                  data-testid="atleta-nome-input"
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  required
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label htmlFor="posicao">Posição</Label>
                <Input
                  id="posicao"
                  data-testid="atleta-posicao-input"
                  value={formData.posicao}
                  onChange={(e) => setFormData({ ...formData, posicao: e.target.value })}
                  required
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label htmlFor="telefone">Telefone</Label>
                <Input
                  id="telefone"
                  data-testid="atleta-telefone-input"
                  value={formData.telefone}
                  onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
                  required
                  className="mt-1.5"
                />
              </div>
              <div>
                <Label htmlFor="ativo">Status</Label>
                <Select value={formData.ativo.toString()} onValueChange={(val) => setFormData({ ...formData, ativo: val === 'true' })}>
                  <SelectTrigger className="mt-1.5" data-testid="atleta-ativo-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="true">Ativo</SelectItem>
                    <SelectItem value="false">Inativo</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button type="submit" className="w-full bg-[#0A192F] hover:bg-[#112240]" data-testid="atleta-submit-button">
                {editingId ? 'Atualizar' : 'Criar'}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Search */}
      <Card className="p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
          <Input
            placeholder="Buscar por nome ou posição..."
            data-testid="search-atletas-input"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </Card>

      {/* Table */}
      <Card className="shadow-sm">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Nome</TableHead>
              <TableHead>Posição</TableHead>
              <TableHead>Telefone</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredAtletas.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-slate-500">
                  Nenhum atleta encontrado
                </TableCell>
              </TableRow>
            ) : (
              filteredAtletas.map((atleta) => (
                <TableRow key={atleta.id} data-testid={`atleta-row-${atleta.id}`}>
                  <TableCell className="font-medium">{atleta.nome}</TableCell>
                  <TableCell>{atleta.posicao}</TableCell>
                  <TableCell>{atleta.telefone}</TableCell>
                  <TableCell>
                    <Badge variant={atleta.ativo ? 'default' : 'secondary'} className={atleta.ativo ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-800'}>
                      {atleta.ativo ? 'Ativo' : 'Inativo'}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" data-testid={`atleta-actions-${atleta.id}`}>
                          <MoreVertical className="w-4 h-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => handleEdit(atleta)} data-testid={`edit-atleta-${atleta.id}`}>
                          <Pencil className="w-4 h-4 mr-2" />
                          Editar
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleDelete(atleta.id)} className="text-red-600" data-testid={`delete-atleta-${atleta.id}`}>
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

export default Atletas;
