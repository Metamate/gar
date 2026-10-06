// @ts-check
import { readFileSync } from "node:fs"
import { defineConfig } from "astro/config"
import starlight from "@astrojs/starlight"
import mermaid from "astro-mermaid"

// Inlined into every page, so it works under any base path.
const pauseAnimations = readFileSync(
  new URL("./src/scripts/pause-animations.js", import.meta.url),
  "utf-8",
)

// On GitHub Actions, derive the Pages URL from the repository so project sites
// (https://<owner>.github.io/<repo>/) get the right base path automatically.
const [owner, repo] = (process.env.GITHUB_REPOSITORY ?? "").split("/")
const isUserSite = repo?.toLowerCase() === `${owner?.toLowerCase()}.github.io`

// https://astro.build/config
export default defineConfig({
  site: owner ? `https://${owner}.github.io` : undefined,
  base: repo && !isUserSite ? `/${repo}` : undefined,
  // The game images are pixel art: converted to WebP losslessly (lossy compression blurs the
  // pixels and adds block artefacts) and resized with nearest neighbour.
  image: {
    service: {
      entrypoint: "astro/assets/services/sharp",
      config: { webp: { lossless: true }, kernel: "nearest" },
    },
  },
  integrations: [
    // Must come before starlight so it claims ```mermaid blocks before
    // Expressive Code turns them into highlighted code.
    mermaid({
      // Follows Starlight's light/dark toggle via the data-theme attribute.
      autoTheme: true,
      enableLog: false,
    }),
    starlight({
      title: "GAR",
      description: "Course site for Game Architecture (GAR).",
      lastUpdated: true,
      customCss: ["./src/styles/retro-font.css", "./src/styles/theme.css"],
      components: { Footer: "./src/components/Footer.astro" },
      logo: {
        src: "./src/assets/logo.png",
        alt: "GAR",
      },
      favicon: "/favicon.ico",
      head: [{ tag: "script", content: pauseAnimations }],
      sidebar: [
        { label: "Home", slug: "" },
        {
          label: "Course",
          items: [
            { label: "Syllabus", slug: "syllabus" },
            { label: "Overview", slug: "overview" },
            { label: "Project", slug: "project" },
            { label: "Exam", slug: "exam" },
            { label: "Course Recap", slug: "recap" },
          ],
        },
        {
          label: "Resources",
          items: [
            {
              label: "Course Games",
              link: "https://github.com/Metamate/gar-games",
            },
            {
              label: "Project Template",
              link: "https://github.com/Metamate/gar-starter",
            },
            {
              label: "Game Programming Patterns",
              link: "https://gameprogrammingpatterns.com/",
            },
            { label: "MonoGame Docs", link: "https://docs.monogame.net/" },
          ],
        },
        {
          label: "Sessions",
          items: [{ autogenerate: { directory: "sessions" } }],
        },
        { label: "Student Games", slug: "student-games" },
      ],
    }),
  ],
})
