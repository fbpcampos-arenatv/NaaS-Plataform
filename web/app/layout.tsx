import "./globals.css";

export const metadata = {
  title: "NaaS",
  description: "Nature As a Service"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
