import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

export async function GET(request: NextRequest) {
  const url = request.nextUrl.searchParams.get("url")?.trim();

  if (!url) {
    return NextResponse.json({ error: "A sitemap URL is required." }, { status: 400 });
  }

  let parsed: URL;
  try {
    parsed = new URL(url);
  } catch {
    return NextResponse.json({ error: "Enter a valid sitemap URL." }, { status: 400 });
  }

  if (!/^https?:$/.test(parsed.protocol)) {
    return NextResponse.json({ error: "Only http and https sitemap URLs are supported." }, { status: 400 });
  }

  try {
    const response = await fetch(parsed.toString(), {
      headers: {
        "user-agent": "Content-Strategy-Creator/1.0"
      },
      cache: "no-store"
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: `Could not fetch sitemap URL (${response.status}).` },
        { status: 400 }
      );
    }

    const xml = await response.text();
    return NextResponse.json({ xml });
  } catch {
    return NextResponse.json(
      { error: "The sitemap URL could not be fetched from the server." },
      { status: 502 }
    );
  }
}
