import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(),
    pubDate: z.coerce.date(),
    heroImage: z.string().optional(),
    author: z.string().optional(),
    tags: z.array(z.string()).optional(),
    source: z.string().optional(), // Original URL for redirects
    neighborhood: z.string().optional(), // For existing posts
  }),
});

export const collections = {
  blog,
};
