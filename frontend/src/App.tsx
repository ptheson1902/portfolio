import React, { useState } from 'react';
import { Header, AdminBar } from './components';
import { AuthProvider } from './context/AuthContext';
import { ProfileSection, SkillsSection, ProjectsSection, ChatSection } from './pages';

const AppContent: React.FC = () => {
  const [activeSection, setActiveSection] = useState('profile');

  const renderSection = () => {
    switch (activeSection) {
      case 'profile':
        return <ProfileSection />;
      case 'skills':
        return <SkillsSection />;
      case 'projects':
        return <ProjectsSection />;
      case 'chat':
        return <ChatSection />;
      default:
        return <ProfileSection />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-dark-bg">
      <Header activeSection={activeSection} onSectionChange={setActiveSection} />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderSection()}
      </main>
      <footer className="border-t border-slate-200 dark:border-dark-border py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-slate-500 dark:text-slate-400">
          <p>PHAM THE SON - Portfolio</p>
          <p className="mt-1">Built with React, TypeScript, FastAPI</p>
        </div>
      </footer>
      <AdminBar />
    </div>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;
