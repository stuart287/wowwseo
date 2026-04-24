import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Internal Link Maps",
  description: "Interactive internal link maps for client sites."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
