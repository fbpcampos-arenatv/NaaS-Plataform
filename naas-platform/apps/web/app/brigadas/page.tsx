import Mapa from "@/components/Mapa";

const urlApi = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Alerta = { id: number; nivel: string; mensagem: string };

type Missao = { id: number; titulo: string; status: string };

async function carregarAlertas(): Promise<Alerta[]> {
  const resposta = await fetch(`${urlApi}/brigadas/alertas`, { cache: "no-store" });
  if (!resposta.ok) {
    return [];
  }
  return resposta.json();
}

async function carregarMissoes(): Promise<Missao[]> {
  const resposta = await fetch(`${urlApi}/brigadas/missoes`, { cache: "no-store" });
  if (!resposta.ok) {
    return [];
  }
  return resposta.json();
}

export default async function PaginaBrigadas() {
  const alertas = await carregarAlertas();
  const missoes = await carregarMissoes();

  return (
    <main className="space-y-8">
      <section className="bg-slate-900 rounded-2xl p-6">
        <h2 className="text-2xl font-semibold mb-2">Mapa de Calor</h2>
        <p className="text-slate-300 mb-4">
          Visualização geoespacial de risco ambiental e perímetros críticos.
        </p>
        <Mapa />
      </section>

      <section className="grid md:grid-cols-2 gap-6">
        <div className="bg-slate-900 rounded-2xl p-6">
          <h3 className="text-xl font-semibold mb-4">Alertas</h3>
          <ul className="space-y-2">
            {alertas.length === 0 && <li className="text-slate-400">Sem alertas disponíveis.</li>}
            {alertas.map((alerta) => (
              <li key={alerta.id} className="bg-slate-800 p-3 rounded-lg">
                <span className="font-semibold">{alerta.nivel}</span> — {alerta.mensagem}
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-slate-900 rounded-2xl p-6">
          <h3 className="text-xl font-semibold mb-4">Missões Ativas</h3>
          <ul className="space-y-2">
            {missoes.length === 0 && <li className="text-slate-400">Sem missões ativas.</li>}
            {missoes.map((missao) => (
              <li key={missao.id} className="bg-slate-800 p-3 rounded-lg">
                <span className="font-semibold">{missao.titulo}</span> — {missao.status}
              </li>
            ))}
          </ul>
        </div>
      </section>
    </main>
  );
}
