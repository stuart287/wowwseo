# Recommendation Style

For bundled local examples, read `source-pack-guide.md` and inspect `source-packs/`.

## Voice

- Write in direct, client-ready language.
- Be specific about the current state and the action required.
- Avoid overstating low-risk issues.
- Keep educational explanations short; the report should be useful to decision makers and implementers.

## Finding Pattern

Use this shape:

1. State what was checked.
2. State the evidence and count.
3. Explain why it matters.
4. Recommend the fix.

Example:

`The crawl found 42 internal links pointing to URLs that return 404 errors. These links create dead ends for users and waste crawl budget. Replace the broken links with relevant live URLs, or remove the links where the target content no longer exists.`

## Severity Guidance

Red issues:

- HTTP and HTTPS versions are both accessible or indexable.
- Broken internal links at scale.
- Important pages returning 404 or being noindexed unintentionally.
- Redirect loops or long redirect chains.
- XML sitemap contains 3xx, 4xx, or non-indexable URLs at meaningful scale.
- Duplicate indexable pages without canonical control.
- Malware, security warnings, or serious SSL misconfiguration.

Orange issues:

- Internal links to 301s where final URLs are known.
- Some low-value indexable pages.
- Missing structured data on important templates.
- Important pages more than three clicks deep.
- Performance issues without clear traffic or conversion impact.
- Orphan pages that may be useful but are not business-critical.

Green notes:

- Correctly configured SSL.
- Preferred domain resolves cleanly.
- Sitemap contains indexable canonical URLs.
- No material redirect chains or broken internal links.
- Structured data validates on key templates.

Blue recommendations:

- Use imperatives: `Update`, `Remove`, `Redirect`, `Noindex`, `Canonicalise`, `Add`, `Review`, `Consolidate`.
- Pair each action with the target URL set or template.

## Practical Recommendation Types

- Update internal links so they point directly to the final 200-status HTTPS URL.
- 301 redirect removed or renamed pages to the most relevant live equivalent.
- Remove broken links when no replacement page exists.
- Remove non-indexable, redirected, or 404 URLs from XML sitemaps.
- Add important indexable URLs to the sitemap.
- Apply `noindex` to low-value utility, tag, archive, search, or uploaded HTML pages when they should not rank.
- Improve internal linking to orphan or deep important pages.
- Consolidate duplicate pages and use self-referencing canonicals on the preferred version.
- Force HTTPS and redirect all domain variants to the preferred canonical host.
- Compress images, defer non-critical JavaScript, reduce unused CSS/JS, and review server response time for performance issues.
- Build and test redirect maps before migration launch.
- Keep proposed sitemap, robots, noindex, and canonical recommendations separate from current-state crawl findings.
- Verify migration fixes after launch with a fresh crawl and Google Search Console checks.

## Migration Recommendation Style

For migration-related audits:

- Say whether the evidence is a live crawl issue, a pre-launch planning item, or a post-launch QA item.
- Use wording such as `Before launch`, `At launch`, and `After launch` when sequencing matters.
- Preserve benchmark context for traffic, rankings, backlinks, PageSpeed, and indexation.
- Avoid saying a proposed sitemap or robots draft is implemented until the live site confirms it.
- Flag subdomain noindex/canonical recommendations as host-specific implementation tasks.
