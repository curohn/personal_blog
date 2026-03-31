# Shot Scout

Shot Scout is a photography scouting companion app built with Flutter. The idea: when you find a great spot — good light, interesting geometry, a view worth coming back to — you shouldn't lose it. Pin it, note the conditions, and come back when the timing is right.

## What It Does

- **Pin locations** with GPS coordinates so you never lose a good spot
- **Track shooting conditions** — ideal time of day, weather, gear notes
- **Gear inventory** for cameras, lenses, and accessories
- **Sun times** calculated from NOAA algorithms — accurate golden hour, blue hour, sunrise/sunset for any location
- **Interactive map** via OpenStreetMap with multiple tile styles
- **Offline-first** — everything stored locally with Hive, no cloud sync, no analytics

## Why I Built It

I wanted something simple that lived on my phone and didn't send my location history to a server somewhere. Most scouting apps are either too heavyweight or require accounts and cloud storage. This one stores everything locally and focuses on the core workflow: find a spot, remember it, come back at the right time.

## Tech Stack

Built with Flutter so it runs on both iOS and Android from a single codebase. State management via Provider. Local storage with Hive (fast, lightweight, no SQL). Location services from `geolocator`, mapping from `flutter_map`.

The dynamic theming — UI colors that shift based on solar phase — was a fun parallel to the weather theming on this site.

## Status

Core features are functional. __App is currently not hosted on any app store.__ Ongoing work on weather API integration, push notification reminders, and photo capture directly in-app.
