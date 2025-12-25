const urlApi = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type TAC = { id: number; titulo: string; status: string };

async function carregarTacs(): Promise<TAC[]> {
  const resposta = await fetch(`${urlApi}/tac`, { cache: "no-store" });
  if (!resposta.ok) {
    return [];
  }
  return resposta.json();
}

export default async function PaginaTAC() {
  const tacs = await carregarTacs();

  return (
    <main className="space-y-8">
      <section className="bg-slate-900 rounded-2xl p-6">
        <h2 className="text-2xl font-semibold mb-4">Painel de TACs</h2>
        <p className="text-slate-300 mb-6">
          Acompanhamento de execução com status técnico e jurídico.
        </p>
        <ul className="space-y-3">
          {tacs.length === 0 && <li className="text-slate-400">Nenhum TAC encontrado.</li>}
          {tacs.map((tac) => (
            <li key={tac.id} className="bg-slate-800 p-4 rounded-xl">
              <p className="font-semibold">{tac.titulo}</p>
              <p className="text-slate-400">Status: {tac.status}</p>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
