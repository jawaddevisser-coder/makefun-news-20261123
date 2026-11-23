// News-image entry (Node 22, standard library only): the program copies the
// entry.png beside it to /output/entry.png. The image itself is drawn by
// draw_news.py (Pillow, deterministic) and stored in this repository.
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
