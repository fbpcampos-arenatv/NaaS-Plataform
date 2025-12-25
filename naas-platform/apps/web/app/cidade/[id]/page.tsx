import Link from "next/link";

const urlApi = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Detalhe = {
  cidade_id: number;
  cidade: string;
  janela_anos: number;
  pontuacao: number;
};

async function carregarDetalhe(id: string): Promise<Detalhe[]> {
  const resposta = await fetch(`${urlApi}/esi/cidades/${id}`, { cache: "no-store" });
  if (!resposta.ok) {
    return [];
  }
  return resposta.json();
}

export default async function PaginaCidade({ params }: { params: { id: string } }) {
  const detalhes = await carregarDetalhe(params.id);
  const nomeCidade = detalhes[0]?.cidade ?? "Cidade";

  return (
    <main className="space-y-6">
      <Link href="/" className="text-emerald-300">Voltar</Link>
      <section className="bg-slate-900 rounded-2xl p-6">
        <h2 className="text-2xl font-semibold mb-4">{nomeCidade}</h2>
        <p className="text-slate-300">Histórico ESI-1000 em diferentes janelas temporais.</p>
      </section>
      <section className="grid md:grid-cols-2 gap-6">
        {detalhes.length === 0 && (
          <div className="bg-slate-900 rounded-2xl p-6 text-slate-400">
            Dados indisponíveis. Faça login na API para acessar detalhes completos.
          </div>
        )}
        {detalhes.map((detalhe) => (
          <div key={detalhe.janela_anos} className="bg-slate-900 rounded-2xl p-6">
            <p className="text-xl font-semibold">Janela de {detalhe.janela_anos} anos</p>
            <p className="text-slate-300">Pontuação: {detalhe.pontuacao}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
