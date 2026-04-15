# Typst Resume Reference

Quick reference for the `modern-cv` Typst template used in `will_cygan_resume.typ`.

## Official Documentation

- **Main docs**: https://typst.app/docs/reference
- **Syntax**: https://typst.app/docs/reference/syntax/
- **Styling**: https://typst.app/docs/reference/styling/
- **Scripting**: https://typst.app/docs/reference/scripting/
- **Context**: https://typst.app/docs/reference/context/

## Template Import

```typst
#import "@preview/modern-cv:0.8.0": *
```

This imports the modern-cv template from the Typst package registry.

## Document Setup

```typst
#show: resume.with(
  author: (
    firstname: "Will",
    lastname: "Cygan",
    email: "wcygan.io@gmail.com",
    homepage: "https://wcygan.net",
    github: "wcygan",
    linkedin: "wcygan",
    positions: (
      "Senior Software Engineer",
    ),
  ),
  profile-picture: none,
  date: datetime.today().display(),
  language: "en",
  colored-headers: true,
  show-footer: false,
  paper-size: "us-letter",
)
```

**Key parameters:**
- `author`: Dictionary with contact information
- `positions`: Tuple of job titles (can have multiple)
- `profile-picture`: Use `none` for no photo (recommended)
- `colored-headers`: `true` for colored section headers
- `show-footer`: `false` to hide footer with page numbers
- `paper-size`: `"us-letter"` for US resumes

## Section Headers

```typst
= Work Experience
= Projects
= Skills
= Education
```

Use single `=` for top-level sections.

## Work Experience / Projects / Education

### resume-entry

Creates an entry with title, location, date, and description.

```typst
#resume-entry(
  title: "Senior Software Engineer",
  location: "Chicago, IL",
  date: "March 2024 – Present",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)
```

**Parameters:**
- `title`: Job title or project name (required)
- `location`: City/state or GitHub link (required)
- `date`: Date range with en dash `–` (required)
- `description`: Company name or brief description (required)
- `title-link`: URL to make title clickable (optional)

**Date formatting:**
- Use en dash `–` (not hyphen `-`): "March 2024 – Present"
- Format: "Month YYYY – Month YYYY" or "Month YYYY – Present"
- For single dates (Education): "2021" or "May 2021"

### resume-item

Bullet points under an entry.

```typst
#resume-item[
  - First accomplishment with quantifiable impact
  - Second accomplishment with technical details
  - Third accomplishment showing business value
]
```

**Important:**
- Use standard hyphen `-` for bullets (not en dash)
- Each bullet is a separate line starting with `-`
- Bullets can span multiple lines - Typst handles wrapping
- No periods at end of bullets
- Aim for 1-2 lines per bullet when rendered

## Projects with GitHub Links

```typst
#resume-entry(
  title: "Anton (Kubernetes Homelab)",
  location: [#github-link("wcygan/anton")],
)
```

**github-link function:**
- `#github-link("username/repo")` creates clickable GitHub link
- Wrap in `[ ]` when using in location field

## Skills Section

```typst
#resume-skill-item(
  "Languages",
  (
    "Java",
    "Rust",
    "Go",
    "Python",
    "TypeScript",
  ),
)
```

**Parameters:**
- First argument: Category name (string)
- Second argument: Tuple of skills (comma-separated, trailing comma optional)

**Multiple categories:**
```typst
#resume-skill-item(
  "Languages",
  ("Java", "Rust", "Go", "Python"),
)
#resume-skill-item(
  "Technologies",
  ("Kafka", "Kubernetes", "Docker", "Terraform"),
)
#resume-skill-item(
  "Databases",
  ("MySQL", "PostgreSQL", "Redis", "MongoDB"),
)
```

## Special Characters

**Dollar signs** (must be escaped):
```typst
- Reduced costs by \$2M+ annually
```

**En dashes** (for date ranges):
```typst
date: "March 2024 – Present"  // en dash: –
```

**Regular dashes** (for bullets and hyphenated words):
```typst
- Built fault-tolerant system  // hyphen in text
- Second bullet point          // hyphen for bullet
```

## Comments

```typst
// This is a single-line comment

/* This is a
   multi-line comment */
```

## Line Breaks and Formatting

**Continuing long bullets:**
```typst
#resume-item[
  - Architected alerting system processing 50,000+ QPS using Kafka,
    Samza, and Venice, enabling real-time payment failure detection
    that reduced involuntary churn by 15%
]
```

Typst automatically handles line wrapping, but you can add manual breaks for readability in source code.

**No manual formatting needed:**
- Don't add extra spaces or tabs for alignment
- Don't use `\n` or `\\` for line breaks (like LaTeX)
- Typst handles all formatting based on the template

## Common Patterns

### LinkedIn Work Experience Entry

```typst
#resume-entry(
  title: "Senior Software Engineer",
  location: "Chicago, IL",
  date: "March 2024 – Present",
  description: "LinkedIn",
  title-link: "https://www.linkedin.com/in/wcygan/",
)

#resume-item[
  - Architected system processing 50K+ QPS with Kafka/Samza/Venice
  - Reduced churn by 15% through proactive payment failure alerts
  - Migrated 4 services to gRPC, improving developer onboarding by 80%
]
```

### Personal Project Entry

```typst
#resume-entry(
  title: "Anton (Kubernetes Homelab)",
  location: [#github-link("wcygan/anton")],
)

#resume-item[
  - Engineered 3-node bare-metal Kubernetes cluster achieving 99.9% uptime
  - Benchmarked distributed systems (TiDB, RedPanda, ScyllaDB)
  - Implemented zero-trust architecture with Cloudflare Tunnels
]
```

### Education Entry

```typst
#resume-entry(
  title: "University of Illinois at Chicago",
  location: "Chicago, IL",
  date: "2021",
  description: "B.S. in Computer Science",
  title-link: "https://www.linkedin.com/in/wcygan/",
)
```

## Compilation

**Watch mode (live preview):**
```bash
typst watch will_cygan_resume.typ
# or
just dev
```

**Compile to PDF:**
```bash
typst compile will_cygan_resume.typ
# or
just compile
```

**Output:**
- Creates `will_cygan_resume.pdf` in the same directory
- PDF uses Letter size (8.5" x 11") paper
- Automatically handles page breaks if content exceeds one page

## Best Practices for Resume Content

### Bullet Points

**DO:**
- Start with strong action verbs (architected, implemented, designed)
- Include quantifiable metrics (50K+ QPS, 15% reduction, \$2M+)
- Specify technologies used (Kafka, MySQL, Kubernetes)
- Keep to 1-2 lines when rendered in PDF
- Focus on impact and results

**DON'T:**
- Start with weak verbs (helped, worked on, assisted)
- Leave achievements unquantified
- Use vague descriptions without technical details
- Create 3+ line bullets (too verbose)
- Include personal pronouns (I, we, my)

### Date Formatting

**Consistent format throughout:**
```typst
"March 2024 – Present"        // Current position
"Feb 2022 – March 2024"       // Past position
"2021"                        // Education graduation year
```

**Always:**
- Use full month names (March, not Mar or 3)
- Use en dash `–` with spaces: ` – `
- Capitalize month names
- Include 4-digit years

### Skills Organization

**Group by category:**
```typst
#resume-skill-item("Languages", (...))      // Programming languages
#resume-skill-item("Technologies", (...))   // Frameworks, tools
#resume-skill-item("Databases", (...))      // Database systems
```

**Order within categories:**
- Most important/relevant first
- Interview-ready skills only
- No soft skills (teamwork, communication)

## Template Limitations & Workarounds

### Cannot Customize

The modern-cv template provides limited customization. You **cannot** easily change:
- Section header colors (unless modifying template source)
- Bullet point styles (always uses `-`)
- Overall layout structure (fixed single-column)

### Must Maintain Structure

```typst
// ✅ Correct structure
#resume-entry(...)
#resume-item[
  - Bullet 1
  - Bullet 2
]

// ❌ Will break template
#resume-entry(...)
- Bullet 1  // Not inside #resume-item[]
- Bullet 2
```

## Debugging Common Issues

### Issue: Dollar signs not showing
**Solution:** Escape with backslash
```typst
\$2M+  // Correct
$2M+   // Wrong - $ has special meaning in Typst
```

### Issue: Bullets not aligned properly
**Solution:** Ensure bullets are inside `#resume-item[]` block
```typst
#resume-item[
  - Bullet 1
  - Bullet 2
]
```

### Issue: Date range uses wrong dash
**Solution:** Use en dash `–` (Option+Hyphen on Mac, Alt+0150 on Windows)
```typst
"March 2024 – Present"  // ✅ en dash
"March 2024 - Present"  // ❌ hyphen
```

### Issue: GitHub link not clickable
**Solution:** Use `#github-link()` function wrapped in `[]`
```typst
location: [#github-link("wcygan/anton")]  // ✅
location: "wcygan/anton"                  // ❌ plain text
```

## File Organization

```
resume/
├── will_cygan_resume.typ    # Source file
├── will_cygan_resume.pdf    # Compiled output
├── justfile                # Tasks: dev, compile, ci
└── scripts/
    ├── dev.py              # Development server (PEP 723 / uv)
    └── run-local-ci.py     # Pre-push testing (PEP 723 / uv)
```

## Quick Checklist

Before committing changes:
- [ ] Compile successfully: `typst compile will_cygan_resume.typ`
- [ ] No compilation errors or warnings
- [ ] PDF renders correctly (check with PDF viewer)
- [ ] All bullets 1-2 lines when rendered
- [ ] En dashes `–` used in all date ranges
- [ ] Dollar signs escaped: `\$`
- [ ] All links clickable in PDF
- [ ] Skills properly categorized
- [ ] Consistent date formatting throughout
- [ ] Test with: `./scripts/run-local-ci.ts`
