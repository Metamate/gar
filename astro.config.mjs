// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';

// On GitHub Actions, derive the Pages URL from the repository so project sites
// (https://<owner>.github.io/<repo>/) get the right base path automatically.
const [owner, repo] = (process.env.GITHUB_REPOSITORY ?? '').split('/');
const isUserSite = repo?.toLowerCase() === `${owner?.toLowerCase()}.github.io`;

// https://astro.build/config
export default defineConfig({
	site: owner ? `https://${owner}.github.io` : undefined,
	base: repo && !isUserSite ? `/${repo}` : undefined,
	integrations: [
		// Must come before starlight so it claims ```mermaid blocks before
		// Expressive Code turns them into highlighted code.
		mermaid({
			// Follows Starlight's light/dark toggle via the data-theme attribute.
			autoTheme: true,
			enableLog: false,
		}),
		starlight({
			title: 'GAR',
			description: 'Course site for Game Architecture (GAR).',
			lastUpdated: true,
			logo: {
				src: './src/assets/logo.png',
				alt: 'GAR',
			},
			favicon: '/favicon.ico',
			sidebar: [
				{
					label: 'Course',
					items: [
						{ label: 'Syllabus', slug: 'syllabus' },
						{ label: 'Schedule', slug: 'schedule' },
						{ label: 'Project', slug: 'project' },
					],
				},
				{ label: 'Sessions', items: [{ autogenerate: { directory: 'sessions' } }] },
				{ label: 'Resources', items: [{ autogenerate: { directory: 'resources' } }] },
			],
		}),
	],
});
