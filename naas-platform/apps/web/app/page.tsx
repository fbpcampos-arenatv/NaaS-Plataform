import Link from "next/link";

const urlApi = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Ranking = {
  cidade_id: number;
  cidade: string;
  pontuacao: number;
};

async function carregarRanking(): Promise<Ranking[]> {
  const resposta = await fetch(`${urlApi}/esi/ranking`, { cache: "no-store" });
  if (!resposta.ok) {
    return [];
  }
  return resposta.json();
}

export default async function PaginaInicial() {
  const ranking = await carregarRanking();

  return (
    <main className="space-y-10">
      <section className="bg-slate-900 rounded-2xl p-6 shadow">
        <h2 className="text-2xl font-semibold mb-2">Índice Ambiental ESI-1000</h2>
        <p className="text-slate-300 mb-6">
          Ranking global com base em séries históricas normalizadas e pesos configuráveis.
        </p>
        <div className="grid md:grid-cols-2 gap-4">
          {ranking.map((item) => (
            <div key={item.cidade_id} className="bg-slate-800 p-4 rounded-xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-lg font-semibold">{item.cidade}</p>
                  <p className="text-slate-400">Pontuação: {item.pontuacao}</p>
                </div>
                <Link
                  href={`/cidade/${item.cidade_id}`}
                  className="text-emerald-300 hover:text-emerald-200"
                >
                  Ver detalhes
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-6">
        <div className="bg-slate-900 rounded-2xl p-6">
          <h3 className="text-xl font-semibold">Prevenção Preditiva</h3>
          <p className="text-slate-300 mt-2">Alertas, brigadas e missões ativas.</p>
          <Link href="/brigadas" className="text-emerald-300 mt-4 inline-block">
            Acessar módulo
          </Link>
        </div>
        <div className="bg-slate-900 rounded-2xl p-6">
          <h3 className="text-xl font-semibold">TAC e Compensação</h3>
          <p className="text-slate-300 mt-2">Gestão de TACs, obrigações e projetos.</p>
          <Link href="/tac" className="text-emerald-300 mt-4 inline-block">
            Acessar módulo
          </Link>
        </div>
        <div className="bg-slate-900 rounded-2xl p-6">
          <h3 className="text-xl font-semibold">Governança</h3>
          <p className="text-slate-300 mt-2">Conselhos, decisões e auditoria imutável.</p>
        </div>
      </section>
    </main>
  );
}
