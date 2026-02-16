import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    // Support both publishDate (from scraper) and pubDate (legacy)
    publishDate: z.coerce.date().optional(),
    pubDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    author: z.string().optional(),
    tags: z.array(z.string()).optional(),
    source: z.string().optional(), // Original URL for redirects
    neighborhood: z.string().optional(), // For existing posts
  }).transform((data) => ({
    ...data,
    // Normalize to pubDate for consistency with existing pages
    pubDate: data.pubDate || data.publishDate || new Date(),
  })),
});

export const collections = {
  blog,
};
