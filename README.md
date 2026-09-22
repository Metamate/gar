# Game Architecture

Course site built with [Astro](https://docs.astro.build) and [Starlight](https://starlight.astro.build).

## Commands

| Command           | Action                                      |
| :---------------- | :------------------------------------------ |
| `npm install`     | Install dependencies                        |
| `npm run dev`     | Start the dev server at `localhost:4321`    |
| `npm run build`   | Build the site to `./dist/`                 |
| `npm run preview` | Preview the build locally                   |

## Project structure

```text
.
├── .github/workflows/deploy.yml   # GitHub Pages deploy on push to main
├── astro.config.mjs               # Site title, logo and sidebar
├── public/favicon.ico
└── src/
    ├── assets/                    # Images referenced from pages (logo, session figures)
    ├── components/                # Interactive components used in MDX pages
    └── content/docs/
        ├── index.mdx              # Home page
        ├── syllabus.md            # Official course description
        ├── schedule.md            # Overview of the 12 sessions
        ├── project.md             # Course project brief
        ├── sessions/              # One page per session (sidebar order via `sidebar.order`)
        └── resources/
```

## Writing pages

- Add a `.md` file under `src/content/docs/`. Its path becomes its URL.
- Files in `sessions/` and `resources/` appear in the sidebar automatically.
  Set `sidebar.order` in frontmatter to control their order.
- Rename a page to `.mdx` to use components like `<Aside>`, `<Tabs>`, `<Steps>`, or your own
  components from `src/components/`. `sessions/01-pong.mdx` shows examples.
- Link between pages with **relative** links, such as `../schedule/`, so links still work when
  the site is served from a subpath on GitHub Pages.

## Deploying to GitHub Pages

1. Push this repository to GitHub on the `main` branch.
2. In the repository, go to **Settings → Pages** and set **Source** to **GitHub Actions**.

The workflow sets `site` and `base` from the repository name. A repository named `gar-app`
publishes to `https://<owner>.github.io/gar-app/`.
