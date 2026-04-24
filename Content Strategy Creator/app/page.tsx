import Link from "next/link";
import { bundledMaps } from "@/lib/maps";

function formatNumber(value: number) {
  return new Intl.NumberFormat("en-ZA").format(value);
}

export default function HomePage() {
  return (
    <main className="shell">
      <div className="container">
        <section className="hero">
          <h1>Internal Link Maps</h1>
          <p>
            Open a client map to explore internal links, focused page searches, incoming and outgoing
            relationships, recommendations, upload support, and URL-level filtering in a Vercel-friendly shell.
          </p>
        </section>

        <section className="card-grid">
          {bundledMaps.map((map) => (
            <Link key={map.slug} href={`/maps/${map.slug}`} className="map-card">
              <span className="eyebrow">{map.domain}</span>
              <div>
                <h2>{map.clientName}</h2>
                <p>{map.description}</p>
              </div>
              <div className="metrics">
                <small>{formatNumber(map.uniquePages)} pages</small>
                <small>{formatNumber(map.uniqueEdges)} link pairs</small>
                <small>{formatNumber(map.linksRetained)} retained links</small>
              </div>
            </Link>
          ))}
        </section>
      </div>
    </main>
  );
}
