"use client";

import { useEffect, useState } from "react";

type Item = {
  id: number;
  nome: string;
  criado_em: string;
};

type EstadoApi = {
  status: "carregando" | "ok" | "erro";
  itens: Item[];
  mensagem: string;
};

export default function Home() {
  const [estado, setEstado] = useState<EstadoApi>({
    status: "carregando",
    itens: [],
    mensagem: "Carregando..."
  });

  useEffect(() => {
    const apiUrl =
      process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

    async function carregar() {
      try {
        const resposta = await fetch(`${apiUrl}/itens`);
        if (!resposta.ok) {
          throw new Error("Resposta inválida da API");
        }
        const dados = (await resposta.json()) as Item[];
        setEstado({
          status: "ok",
          itens: dados,
          mensagem: "API conectada com sucesso"
        });
      } catch (erro) {
        setEstado({
          status: "erro",
          itens: [],
          mensagem: `Erro ao conectar na API: ${String(erro)}`
        });
      }
    }

    carregar();
  }, []);

  return (
    <main className="container">
      <section className="card">
        <h1>Nature As a Service (NaaS)</h1>
        <p>Status da API: {estado.mensagem}</p>
        <h2>Itens de exemplo</h2>
        {estado.itens.length === 0 ? (
          <p>Nenhum item encontrado.</p>
        ) : (
          <ul>
            {estado.itens.map((item) => (
              <li key={item.id}>
                <strong>{item.nome}</strong> — criado em {item.criado_em}
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
