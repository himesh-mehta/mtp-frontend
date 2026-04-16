# MTP Frontend

This repository contains the frontend for **MTP Protocol**, a Next.js-based product site for the **Model Tool Protocol**.

The site is structured as a polished marketing and documentation experience rather than a generic starter app. It presents:

- A landing page that explains the protocol and drives users into the docs
- A documentation system with categorized technical content
- A dashboard view for system health and provider status
- An execution flow visualizer for agent planning and task resolution
- An interactive playground-style UI for trying agent workflows

## What the site is about

MTP is presented in the app as an agent orchestration framework that separates model reasoning from environment execution.

The core idea shown throughout the UI and docs is:

- models produce structured execution plans
- the runtime validates and resolves those plans
- tools execute under policy control
- results are fed back into state for the next step

The docs also describe supporting concepts such as:

- DAG-based execution plans
- tool orchestration and tool registries
- multi-model provider support
- policy enforcement
- persistence across sessions
- streaming and transport layers
- MCP interoperability

## Main Routes

- `/` - marketing landing page with hero content, architecture highlights, and calls to action
- `/docs` - redirects to the documentation introduction
- `/docs/[slug]` - documentation pages generated from `lib/docs-content.ts`
- `/dashboard` - mock system dashboard with provider health cards and runtime metrics
- `/execution` - execution flow visualization showing planning and branching task execution
- `/playground` - chat-like agent playground with provider, model, and tool controls

## Documentation System

The docs are driven by the content registry in `lib/docs-content.ts`.

That file defines:

- the docs sidebar sections
- slug lookup helpers
- page content blocks

The docs UI in `app/docs/layout.tsx` provides:

- a fixed top header
- a collapsible left sidebar
- docs search filtering
- a floating "Ask AI" action button

The individual docs pages in `app/docs/[slug]/page.tsx` render:

- structured text blocks
- code samples
- lists
- callouts
- tables
- previous/next navigation
- in-page section navigation

## Tech Stack

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS 4
- Framer Motion
- Lucide React icons
- `clsx` and `tailwind-merge` utilities
- Google fonts via `next/font`:
  - Inter
  - Geist Mono

## Development

Install dependencies and run the development server:

```bash
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

## Available Scripts

- `npm run dev` - start the development server
- `npm run build` - build the production app
- `npm run start` - start the production server
- `npm run lint` - run ESLint

## Project Structure

- `app/page.tsx` - landing page
- `app/layout.tsx` - root layout and metadata
- `app/(app)/layout.tsx` - shared app shell with navbar and sidebar
- `app/(app)/dashboard/page.tsx` - dashboard page
- `app/(app)/execution/page.tsx` - execution visualizer
- `app/(app)/playground/page.tsx` - playground page
- `app/docs/layout.tsx` - docs shell and navigation
- `app/docs/[slug]/page.tsx` - docs content renderer
- `components/` - shared UI components
- `lib/docs-content.ts` - docs content source of truth
- `lib/utils.ts` - shared utility helpers

## Notes

- The site is currently frontend-only and uses static/mock data for the dashboard, execution view, and playground UI.
- If you add or rename docs content, update `lib/docs-content.ts` first because it powers both navigation and page rendering.
- The visual design uses a dark theme, subtle textures, animated accents, and custom component styling across the app.
