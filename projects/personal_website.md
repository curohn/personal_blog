# Personal Website

A portfolio site to showcase my work, research, and professional journey — and a project in its own right for developing web development skills.

## Features

- **Home**: Featured projects, currently working on, and to-do sections.

- **Projects**: Markdown-rendered writeups for each project, with tool/language tags and GitHub links. Sidebar navigation between projects.

- **Murmuration**: Live boid flocking simulation with user-adjustable separation, alignment, and cohesion weights and radii.

- **About Me**: Compact left-aligned timeline of work experience and education, with resume download.

- **Weather-based theming**: The site themes itself based on Atlanta's real-time weather and time of day. Six time-of-day palettes (night, dawn, morning, noon, afternoon, dusk) with weather condition overlays (clear, clouds, rain, storm, snow, fog). Rain, snow, storm, and fog are rendered as canvas animations. A sun/glow orb shifts position and color across the day. A live Atlanta weather badge shows in the nav.

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS custom properties, vanilla JavaScript
- **Content**: Markdown files rendered at runtime
- **Weather**: OpenWeatherMap API (30-min cached)
- **Hosting**: Render — [j-curran.com](https://j-curran.com)
