export type BundledMap = {
  slug: string;
  clientName: string;
  domain: string;
  description: string;
  uniquePages: number;
  uniqueEdges: number;
  linksRetained: number;
  publicPath: string;
};

export const bundledMaps: BundledMap[] = [
  {
    slug: "united-telecoms",
    clientName: "United Telecoms",
    domain: "unitedtelecoms.co.za",
    description: "Internal link map with filters, presets, recommendations, and upload support.",
    uniquePages: 588,
    uniqueEdges: 60759,
    linksRetained: 60762,
    publicPath: "/internal-link-visualisation/united-telecoms-internal-link-map.html"
  },
  {
    slug: "baracuda",
    clientName: "Baracuda",
    domain: "baracuda.co.za",
    description: "Internal link map with focused URL filtering, grouped recommendations, and summary panels.",
    uniquePages: 89,
    uniqueEdges: 3032,
    linksRetained: 3032,
    publicPath: "/internal-link-visualisation/baracuda-internal-link-map.html"
  },
  {
    slug: "food-label-maker",
    clientName: "Food Label Maker",
    domain: "foodlabelmaker.com",
    description: "Internal link map for large multilingual regulatory content sets, with subtree-focused URL filtering and upload support.",
    uniquePages: 2021,
    uniqueEdges: 95399,
    linksRetained: 95439,
    publicPath: "/internal-link-visualisation/food-label-maker-internal-link-map.html"
  }
];

export function getBundledMap(slug: string) {
  return bundledMaps.find((map) => map.slug === slug);
}
