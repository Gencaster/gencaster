export const metaHead = (
  metaTitle: string,
  metaDescription: string,
  metaImageUrl?: string,
  siteUrl?: string,
) => {
  const meta = {
    title: metaTitle,
    meta: [
      { name: "description", content: metaDescription },
      { hid: "description", name: "description", content: metaDescription },

      // Twitter Card data
      { name: "twitter:title", content: metaTitle, hid: "custom" },
      { name: "twitter:description", content: metaDescription, hid: "custom" },

      // Open Graph
      { property: "og:title", content: metaTitle, hid: "custom" },
      {
        property: "og:description",
        content: metaDescription,
        hid: "og:description",
      },
      { property: "og:image", content: metaImageUrl, hid: "og:image" },
    ],
  };

  if (metaImageUrl) {
    meta.meta.push({ name: "og:image", content: metaImageUrl });
    meta.meta.push({
      name: "twitter:image",
      content: metaImageUrl,
      hid: "custom",
    });
  }

  if (siteUrl) {
    meta.meta.push({ property: "og:url", content: siteUrl, hid: "custom" });
  }

  return meta;
};
