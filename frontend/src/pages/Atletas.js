import React, { useState, useEffect, useRef } from 'react';
import { toast } from 'sonner';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Badge } from '../components/ui/badge';
import { Plus, Pencil, Trash2, Search, Upload, UserCircle2 } from 'lucide-react';
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
    foto: null,
    pe_dominante: 'direito',
    ativo: true,
  });
  const fileInputRef = useRef(null);

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

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 2 * 1024 * 1024) {
        toast.error('Imagem muito grande! Máximo 2MB');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData({ ...formData, foto: reader.result });
      };
      reader.readAsDataURL(file);
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
      foto: atleta.foto,
      pe_dominante: atleta.pe_dominante || 'direito',
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
    setFormData({ nome: '', posicao: '', telefone: '', foto: null, pe_dominante: 'direito', ativo: true });
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const FootIcon = ({ side, isActive }) => (
    <svg
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ transform: side === 'esquerdo' ? 'scaleX(-1)' : 'none' }}
    >
      <path
        d="M14 3C13.45 3 13 3.45 13 4C13 4.55 13.45 5 14 5C14.55 5 15 4.55 15 4C15 3.45 14.55 3 14 3ZM12 5C11.45 5 11 5.45 11 6C11 6.55 11.45 7 12 7C12.55 7 13 6.55 13 6C13 5.45 12.55 5 12 5ZM10 7C9.45 7 9 7.45 9 8C9 8.55 9.45 9 10 9C10.55 9 11 8.55 11 8C11 7.45 10.55 7 10 7ZM8.5 9C7.95 9 7.5 9.45 7.5 10C7.5 10.55 7.95 11 8.5 11C9.05 11 9.5 10.55 9.5 10C9.5 9.45 9.05 9 8.5 9ZM7.5 11.5C6.67 11.5 6 12.17 6 13C6 13.83 6.67 14.5 7.5 14.5C7.89 14.5 8.24 14.35 8.5 14.11L9.5 20C9.61 20.56 10.11 21 10.69 21H12.31C12.89 21 13.39 20.56 13.5 20L14.5 14.11C14.76 14.35 15.11 14.5 15.5 14.5C16.33 14.5 17 13.83 17 13C17 12.17 16.33 11.5 15.5 11.5C15.11 11.5 14.76 11.65 14.5 11.89L14 8C14 7.45 13.55 7 13 7H10C9.45 7 9 7.45 9 8L8.5 11.89C8.24 11.65 7.89 11.5 7.5 11.5Z"
        fill={isActive ? '#FFC107' : '#64748B'}
        opacity={isActive ? '1' : '0.3'}
      />
    </svg>
  );

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
            <Button className="bg-[#002B8C] hover:bg-[#0A1F51] text-white" data-testid="add-atleta-button">
              <Plus className="w-4 h-4 mr-2" />
              Novo Atleta
            </Button>
          </DialogTrigger>
          <DialogContent data-testid="atleta-dialog" className="max-w-lg">
            <DialogHeader>
              <DialogTitle>{editingId ? 'Editar Atleta' : 'Novo Atleta'}</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4" aria-describedby="atleta-form-description">
              <p id="atleta-form-description" className="sr-only">Preencha os dados do atleta</p>
              
              {/* Foto */}
              <div className="flex flex-col items-center gap-4">
                <div className="relative">
                  {formData.foto ? (
                    <img
                      src={formData.foto}
                      alt="Preview"
                      className="w-32 h-32 rounded-full object-cover border-4 border-[#002B8C]"
                    />
                  ) : (
                    <div className="w-32 h-32 rounded-full bg-slate-200 flex items-center justify-center border-4 border-[#002B8C]">
                      <UserCircle2 className="w-24 h-24 text-slate-400" />
                    </div>
                  )}
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="absolute bottom-0 right-0 bg-[#FFC107] hover:bg-[#FFD54F] text-[#0A1F51] p-2 rounded-full shadow-lg transition-all"
                  >
                    <Upload className="w-4 h-4" />
                  </button>
                </div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                />
                <p className="text-xs text-slate-500">Clique no ícone para adicionar foto (máx. 2MB)</p>
              </div>

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
                <Label htmlFor="pe_dominante">Pé Dominante</Label>
                <Select value={formData.pe_dominante} onValueChange={(val) => setFormData({ ...formData, pe_dominante: val })}>
                  <SelectTrigger className="mt-1.5" data-testid="atleta-pe-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="direito">Direito</SelectItem>
                    <SelectItem value="esquerdo">Esquerdo</SelectItem>
                    <SelectItem value="ambidestro">Ambidestro</SelectItem>
                  </SelectContent>
                </Select>
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
              <Button type="submit" className="w-full bg-[#002B8C] hover:bg-[#0A1F51]" data-testid="atleta-submit-button">
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

      {/* Athletes Grid */}
      {filteredAtletas.length === 0 ? (
        <Card className="p-12 text-center">
          <UserCircle2 className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <p className="text-slate-500 text-lg">Nenhum atleta encontrado</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredAtletas.map((atleta) => (
            <Card key={atleta.id} className="overflow-hidden hover:shadow-lg transition-shadow duration-200" data-testid={`atleta-card-${atleta.id}`}>
              <div className="relative">
                <div className="bg-gradient-to-br from-[#0A1F51] to-[#002B8C] h-24"></div>
                <div className="absolute -bottom-12 left-1/2 transform -translate-x-1/2">
                  {atleta.foto ? (
                    <img
                      src={atleta.foto}
                      alt={atleta.nome}
                      className="w-24 h-24 rounded-full object-cover border-4 border-white shadow-lg"
                    />
                  ) : (
                    <div className="w-24 h-24 rounded-full bg-slate-200 flex items-center justify-center border-4 border-white shadow-lg">
                      <UserCircle2 className="w-20 h-20 text-slate-400" />
                    </div>
                  )}
                </div>
              </div>
              <div className="pt-16 pb-6 px-6 text-center">
                <h3 className="text-lg font-bold text-slate-900 mb-1">{atleta.nome}</h3>
                <p className="text-sm text-[#FFC107] font-semibold mb-2">{atleta.posicao}</p>
                <p className="text-sm text-slate-600 mb-3">{atleta.telefone}</p>
                
                {/* Pé Dominante */}
                {atleta.pe_dominante && (
                  <div className="flex justify-center gap-3 mb-3">
                    <div className="flex flex-col items-center">
                      <FootIcon 
                        side="esquerdo" 
                        isActive={atleta.pe_dominante === 'esquerdo' || atleta.pe_dominante === 'ambidestro'} 
                      />
                      <span className={`text-xs mt-1 ${(atleta.pe_dominante === 'esquerdo' || atleta.pe_dominante === 'ambidestro') ? 'text-[#FFC107] font-semibold' : 'text-slate-400'}`}>
                        ESQ
                      </span>
                    </div>
                    <div className="flex flex-col items-center">
                      <FootIcon 
                        side="direito" 
                        isActive={atleta.pe_dominante === 'direito' || atleta.pe_dominante === 'ambidestro'} 
                      />
                      <span className={`text-xs mt-1 ${(atleta.pe_dominante === 'direito' || atleta.pe_dominante === 'ambidestro') ? 'text-[#FFC107] font-semibold' : 'text-slate-400'}`}>
                        DIR
                      </span>
                    </div>
                  </div>
                )}
                
                <div className="flex justify-center mb-4">
                  <Badge 
                    variant={atleta.ativo ? 'default' : 'secondary'} 
                    className={atleta.ativo ? 'bg-[#28A745] text-white' : 'bg-slate-200 text-slate-800'}
                  >
                    {atleta.ativo ? 'Ativo' : 'Inativo'}
                  </Badge>
                </div>
                <div className="flex gap-2 justify-center">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleEdit(atleta)}
                    data-testid={`edit-atleta-${atleta.id}`}
                    className="flex-1"
                  >
                    <Pencil className="w-3 h-3 mr-1" />
                    Editar
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleDelete(atleta.id)}
                    data-testid={`delete-atleta-${atleta.id}`}
                    className="text-red-600 hover:bg-red-50"
                  >
                    <Trash2 className="w-3 h-3" />
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Atletas;
