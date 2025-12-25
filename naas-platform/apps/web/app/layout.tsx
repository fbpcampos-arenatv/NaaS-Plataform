import "./globals.css";

export const metadata = {
  title: "NaaS - Nature As a Service",
  description: "Sistema Operacional Global de Regeneração Ambiental"
};

export default function LayoutRaiz({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen">
        <div className="max-w-6xl mx-auto p-6">
          <header className="mb-8">
            <h1 className="text-3xl font-bold">Nature As a Service (NaaS)</h1>
            <p className="text-slate-300">Sistema Operacional Global de Regeneração Ambiental</p>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
