#!/usr/bin/env -S deno run --allow-run --allow-read --allow-write

/**
 * Local CI Runner using Act
 * 
 * This script uses nektos/act to run GitHub Actions workflows locally.
 * It provides fast feedback for testing workflow changes without pushing to GitHub.
 * 
 * Usage: ./scripts/run-local-ci.ts [options]
 */

import * as colors from "https://deno.land/std@0.208.0/fmt/colors.ts";

interface RunOptions {
  workflow?: string;
  job?: string;
  verbose?: boolean;
  dryRun?: boolean;
}

class LocalCIRunner {
  private readonly workflowsDir = ".github/workflows";
  
  constructor() {
    this.checkPrerequisites();
  }

  private async checkPrerequisites(): Promise<void> {
    console.log(colors.blue("🔍 Checking prerequisites..."));
    
    try {
      // Check if we're running in Deno
      if (typeof Deno === 'undefined') {
        throw new Error("This script must be run with Deno");
      }

      // Check if act is installed
      const actCheck = await new Deno.Command("act", {
        args: ["--version"],
        stdout: "piped",
        stderr: "piped",
      }).output();

      if (!actCheck.success) {
        throw new Error("Act is not installed or not in PATH");
      }

      // Check if Docker is running
      const dockerCheck = await new Deno.Command("docker", {
        args: ["info"],
        stdout: "piped",
        stderr: "piped",
      }).output();

      if (!dockerCheck.success) {
        throw new Error("Docker is not running or not installed");
      }

      console.log(colors.green("✅ Prerequisites check passed"));
    } catch (error) {
      console.error(colors.red(`❌ Prerequisites check failed: ${error instanceof Error ? error.message : String(error)}`));
      console.log(colors.yellow("\n📦 Installation Instructions:"));
      
      if (typeof Deno === 'undefined') {
        console.log(colors.white("  Deno: curl -fsSL https://deno.land/install.sh | sh"));
      }
      
      console.log(colors.white("  Act (macOS): brew install act"));
      console.log(colors.white("  Act (Linux): curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"));
      console.log(colors.white("  Docker: https://docs.docker.com/get-docker/"));
      console.log(colors.yellow("\n💡 Make sure Docker is installed and running."));
      Deno.exit(1);
    }
  }

  private async listWorkflows(): Promise<string[]> {
    try {
      const workflows: string[] = [];
      for await (const entry of Deno.readDir(this.workflowsDir)) {
        if (entry.isFile && (entry.name.endsWith('.yml') || entry.name.endsWith('.yaml'))) {
          workflows.push(entry.name);
        }
      }
      return workflows;
    } catch {
      return [];
    }
  }

  async runWorkflow(options: RunOptions = {}): Promise<void> {
    const { workflow = "compile-resume.yml", job, verbose = false, dryRun = false } = options;

    console.log(colors.blue(`🚀 Running workflow: ${workflow}`));
    
    if (dryRun) {
      console.log(colors.yellow("🔍 Dry run mode - showing what would be executed"));
    }

    const args: string[] = [];

    if (job) {
      args.push("--job", job);
    }

    if (verbose) {
      args.push("--verbose");
    }

    if (dryRun) {
      args.push("--dryrun");
    }

    // Add platform specification for better compatibility
    args.push("--platform", "ubuntu-latest=catthehacker/ubuntu:act-latest");
    
    // Act will auto-detect workflows in .github/workflows/

    try {
      console.log(colors.gray(`Running: act ${args.join(" ")}`));
      
      const process = new Deno.Command("act", {
        args,
        stdout: "piped",
        stderr: "piped",
      });

      const child = process.spawn();
      
      // Stream output in real-time
      const decoder = new TextDecoder();
      
      const readStream = async (stream: ReadableStream<Uint8Array>, prefix: string, color: (text: string) => string) => {
        const reader = stream.getReader();
        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const text = decoder.decode(value);
            const lines = text.split('\n').filter(line => line.trim());
            
            for (const line of lines) {
              console.log(color(`${prefix} ${line}`));
            }
          }
        } finally {
          reader.releaseLock();
        }
      };

      // Read stdout and stderr concurrently
      await Promise.all([
        readStream(child.stdout, "[OUT]", colors.white),
        readStream(child.stderr, "[ERR]", colors.red),
      ]);

      const result = await child.status;

      if (result.success) {
        console.log(colors.green("\n✅ Workflow completed successfully!"));
        
        // Check if PDF was generated
        try {
          const stat = await Deno.stat("will_cygan_resume.pdf");
          console.log(colors.green(`📄 Resume PDF generated (${Math.round(stat.size / 1024)}KB)`));
        } catch {
          console.log(colors.yellow("⚠️  PDF file not found in current directory"));
        }
      } else {
        console.log(colors.red(`\n❌ Workflow failed with exit code: ${result.code}`));
        Deno.exit(result.code || 1);
      }

    } catch (error) {
      console.error(colors.red(`❌ Error running workflow: ${error instanceof Error ? error.message : String(error)}`));
      Deno.exit(1);
    }
  }

  async listAvailableWorkflows(): Promise<void> {
    console.log(colors.blue("📋 Available workflows:"));
    const workflows = await this.listWorkflows();
    
    if (workflows.length === 0) {
      console.log(colors.yellow("  No workflows found in .github/workflows/"));
      return;
    }

    workflows.forEach(workflow => {
      console.log(colors.white(`  • ${workflow}`));
    });
  }

  async showHelp(): Promise<void> {
    console.log(colors.blue("🎯 Local CI Runner - Run GitHub Actions locally with Act\n"));
    
    console.log(colors.white("Usage:"));
    console.log("  ./scripts/run-local-ci.ts [options]");
    console.log("  deno run --allow-run --allow-read --allow-write scripts/run-local-ci.ts [options]\n");
    
    console.log(colors.white("Options:"));
    console.log("  --workflow <name>    Specify workflow file (default: compile-resume.yml)");
    console.log("  --job <name>         Run specific job only");
    console.log("  --verbose            Enable verbose output");
    console.log("  --dry-run            Show what would be executed without running");
    console.log("  --list               List available workflows");
    console.log("  --help               Show this help message\n");
    
    console.log(colors.white("Examples:"));
    console.log("  # Run default workflow (direct execution)");
    console.log("  ./scripts/run-local-ci.ts");
    console.log("");
    console.log("  # Run with verbose output");
    console.log("  ./scripts/run-local-ci.ts --verbose");
    console.log("");
    console.log("  # Dry run to see what would execute");
    console.log("  ./scripts/run-local-ci.ts --dry-run");
    console.log("");
    console.log("  # Alternative: explicit Deno command");
    console.log("  deno run --allow-run --allow-read --allow-write scripts/run-local-ci.ts");
  }
}

// Parse command line arguments
function parseArgs(args: string[]): RunOptions & { list?: boolean; help?: boolean } {
  const options: RunOptions & { list?: boolean; help?: boolean } = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    switch (arg) {
      case "--workflow":
        options.workflow = args[++i];
        break;
      case "--job":
        options.job = args[++i];
        break;
      case "--verbose":
        options.verbose = true;
        break;
      case "--dry-run":
        options.dryRun = true;
        break;
      case "--list":
        options.list = true;
        break;
      case "--help":
        options.help = true;
        break;
      default:
        if (arg.startsWith("--")) {
          console.error(colors.red(`Unknown option: ${arg}`));
          Deno.exit(1);
        }
    }
  }
  
  return options;
}

// Main execution
async function main() {
  const args = parseArgs(Deno.args);
  const runner = new LocalCIRunner();

  if (args.help) {
    await runner.showHelp();
    return;
  }

  if (args.list) {
    await runner.listAvailableWorkflows();
    return;
  }

  await runner.runWorkflow(args);
}

if (import.meta.main) {
  main().catch((error) => {
    console.error(colors.red(`Fatal error: ${error.message}`));
    Deno.exit(1);
  });
} 