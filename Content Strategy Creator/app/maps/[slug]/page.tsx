import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { bundledMaps, getBundledMap } from "@/lib/maps";

type PageProps = {
  params: {
    slug: string;
  };
};

export function generateStaticParams() {
  return bundledMaps.map((map) => ({ slug: map.slug }));
}

export function generateMetadata({ params }: PageProps): Metadata {
  const map = getBundledMap(params.slug);
  if (!map) {
    return { title: "Map not found" };
  }
  return {
    title: `${map.clientName} Internal Link Map`,
    description: `Interactive internal link map for ${map.domain}.`
  };
}

export default function MapPage({ params }: PageProps) {
  const map = getBundledMap(params.slug);
  if (!map) notFound();

  return (
    <main className="viewer-shell">
      <header className="viewer-header">
        <div>
          <h1>{map.clientName} Internal Link Map</h1>
          <p>{map.domain}</p>
        </div>
        <Link href="/" className="pill-link">
          All maps
        </Link>
      </header>
      <iframe
        className="viewer-frame"
        src={map.publicPath}
        title={`${map.clientName} internal link map`}
      />
    </main>
  );
}
