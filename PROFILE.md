# Profile README

Edit [profile.config.json](profile.config.json) to change the profile, featured projects, links, or palette. Both GitHub appearance modes use the same Ink light palette. The renderer displays project banners in grayscale.

Run these commands with Node.js 20 or later to refresh the GitHub metadata, public contribution heatmap, and SVGs.

```sh
npm run check
npm run build
```

Commit the resulting README, `profile/generated/`, and the JSON caches in `profile/` together. The generator can reuse the last successful metadata fetch for the same configured projects.

The generator is adapted from [ripgrim/ripgrim](https://github.com/ripgrim/ripgrim) under the [MIT license](LICENSE.profile). The bundled font has its own [license](fonts/CommitMono-LICENSE).
