#!/usr/bin/env -S deno run --allow-read --allow-run --allow-env

/**
 * Development script for resume project
 * Opens the PDF and starts typst watch
 */

import $ from "jsr:@david/dax@0.42.0";
import { dirname, join, basename } from "jsr:@std/path@1.0.8";

// Get the current working directory
const cwd = Deno.cwd();

// Change to the resume directory (parent of scripts) only if currently in scripts dir
if (basename(cwd) === "scripts") {
  const scriptPath = import.meta.url.replace("file://", "");
  const resumeDir = dirname(dirname(scriptPath));
  Deno.chdir(resumeDir);
}

// Open the PDF file in the default viewer (cross-platform)
console.log("Opening will_cygan_resume.pdf...");

const osType = Deno.build.os;
try {
  if (osType === "darwin") {
    // macOS
    await $`open will_cygan_resume.pdf`;
  } else if (osType === "linux") {
    // Linux
    await $`xdg-open will_cygan_resume.pdf`;
  } else if (osType === "windows") {
    // Windows
    await $`cmd /c start will_cygan_resume.pdf`;
  } else {
    console.log("Warning: Unknown OS type. Attempting to use xdg-open...");
    const result = await $`xdg-open will_cygan_resume.pdf`.noThrow();
    if (result.code !== 0) {
      console.log("Could not open PDF automatically");
    }
  }
} catch (error) {
  console.error("Error opening PDF:", error.message);
}

// Start typst watch in the foreground
console.log("Starting typst watch...");
await $`typst watch will_cygan_resume.typ`;