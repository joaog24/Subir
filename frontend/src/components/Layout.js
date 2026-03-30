import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  Dumbbell, 
  Trophy, 
  DollarSign, 
  FileText, 
  LogOut,
  Menu
} from 'lucide-react';
import { Button } from './ui/button';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';

const Layout = ({ children, setIsAuthenticated }) => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/atletas', label: 'Atletas', icon: Users },
    { path: '/treinos', label: 'Treinos', icon: Dumbbell },
    { path: '/partidas', label: 'Partidas', icon: Trophy },
    { path: '/financeiro', label: 'Financeiro', icon: DollarSign },
    { path: '/relatorios', label: 'Relatórios', icon: FileText },
  ];

  const handleLogout = () => {
    localStorage.removeItem('ecp_token');
    setIsAuthenticated(false);
  };

  const SidebarContent = () => (
    <div className="flex flex-col h-full">
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="bg-white rounded-lg p-1.5 flex items-center justify-center flex-shrink-0">
            <img 
              src="https://customer-assets.emergentagent.com/job_piedade-sports/artifacts/nuyr9yj4_logo.png" 
              alt="E.C.P Logo" 
              className="w-8 h-8 object-contain"
            />
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="text-lg font-bold text-white tracking-tight leading-tight" data-testid="sidebar-logo">
              Esporte Clube Piedade
            </h1>
            <p className="text-[#FFC107] text-[10px] mt-0.5 font-medium">Sistema de Gerenciamento</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              data-testid={`nav-${item.label.toLowerCase()}`}
              onClick={() => setMobileMenuOpen(false)}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-[#2C4078] text-white border-l-4 border-[#FFC107]'
                  : 'text-white/70 hover:text-white hover:bg-white/5'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-white/10">
        <Button
          onClick={handleLogout}
          data-testid="logout-button"
          className="w-full bg-red-600 hover:bg-red-700 text-white flex items-center justify-center gap-2"
        >
          <LogOut className="w-4 h-4" />
          Sair
        </Button>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-[#F8F9FA]">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex w-64 bg-[#0A1F51] flex-col">
        <SidebarContent />
      </aside>

      {/* Mobile Menu */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
          <SheetTrigger asChild>
            <Button size="icon" variant="outline" data-testid="mobile-menu-button">
              <Menu className="w-5 h-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 p-0 bg-[#0A1F51]">
            <SidebarContent />
          </SheetContent>
        </Sheet>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Topbar */}
        <header className="bg-white border-b border-slate-200 sticky top-0 z-40" data-testid="topbar">
          <div className="px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h2 className="text-xl font-semibold text-slate-800 hidden lg:block">
                {menuItems.find((item) => item.path === location.pathname)?.label || 'Dashboard'}
              </h2>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right">
                <p className="text-sm font-semibold text-slate-800">Olá, admin</p>
                <p className="text-xs text-slate-500">Administrador</p>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8" data-testid="main-content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
