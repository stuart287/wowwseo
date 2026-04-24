import Link from "next/link";

export default function NotFoundPage() {
  return (
    <main className="shell">
      <div className="container">
        <div className="notice">
          <strong>Map not found.</strong>
          <p>
            The requested map route does not exist in this Next.js shell yet. Return to the map index to open a bundled client view.
          </p>
          <Link href="/" className="pill-link">
            Back to all maps
          </Link>
        </div>
      </div>
    </main>
  );
}
