# Personal Website

A portfolio site to showcase my work, research, and professional journey — and a project in its own right for developing web development skills.

## Features

- **Home**: Featured projects, currently working on, and to-do sections rendered as frosted glass cards over the live background.

- **Projects**: Markdown-rendered writeups for each project, with tool/language tags, GitHub links, and a sticky sidebar for navigation between projects.

- **Murmuration**: Controls panel for the live boid flocking simulation running in the background. Adjust separation, alignment, cohesion weights and radii to shape the flock visible across every page.

- **About Me**: Left-aligned timeline of work experience and education with resume download.

- **Landscape background**: A procedurally drawn canvas scene — rolling foreground hills, a mid-range layer for depth, and a distant mountain range clustered on the right. Rendered on every page behind all content.

- **Weather-based theming**: The site themes itself based on Atlanta's real-time weather and time of day. Six time-of-day palettes (night, dawn, morning, noon, afternoon, dusk) derived from actual sunrise/sunset times. Weather condition overlays (clear, clouds, rain, storm, snow, fog) shift the palette and drive canvas effects — rain drops, wind streaks, snow flakes, lightning flashes, and drifting fog. A sun/moon orb shifts position and opacity across the day.

- **Frosted glass UI**: All cards, the header, footer, and sidebars use `backdrop-filter` blur over the canvas, giving a semi-transparent glass appearance that changes with the scene behind it.

- **Live Atlanta weather badge**: Pulsing green dot in the nav showing current temperature and conditions.

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS custom properties, vanilla JavaScript
- **Content**: Markdown files rendered at runtime
- **Weather**: OpenWeatherMap API (30-min cached)
- **Hosting**: Render — [j-curran.com](https://j-curran.com)
