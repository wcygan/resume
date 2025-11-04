# Resume Optimizer Skill

Comprehensive resume optimization skill that automatically activates when users need help improving their engineering resumes.

## What This Skill Does

Analyzes and optimizes engineering resumes using proven methodologies:
- **STAR/XYZ/CAR frameworks** for compelling bullet points
- **ATS optimization** based on 2.5M resume research
- **Hiring manager insights** from Meta, FAANG, and Fortune 500 companies
- **Action verb enhancement** replacing weak with strong verbs
- **Quantification strategies** for demonstrating impact
- **Formatting best practices** for 10-second scan readability

## Activation Triggers

This skill automatically activates when you:
- "Review my resume"
- "Help me improve these bullet points"
- "Optimize my resume for this job description"
- "Make my resume more ATS-friendly"
- "How can I quantify this experience?"
- "Tailor my resume for [role/company]"

## What's Included

### SKILL.md
Main instructions for Claude Code with:
- Systematic optimization framework
- Formatting guidelines
- Bullet point quality checklist (STAR/XYZ/CAR)
- ATS optimization strategies
- Job-specific tailoring workflow
- Career level adaptations

### REFERENCE.md
Comprehensive reference guide with:
- Detailed STAR/XYZ/CAR examples
- Action verb library (tier 1/2/3)
- Quantification strategies and templates
- Before/after bullet point examples
- Industry-specific keywords
- Common mistakes library
- Quick reference checklists

### TYPST-REFERENCE.md
Typst-specific documentation for this project:
- modern-cv template syntax and functions
- resume-entry, resume-item, resume-skill-item usage
- Typst special characters and formatting
- Compilation and debugging tips
- Best practices for Typst resume editing
- Common issues and solutions

### Templates
- **optimization-report.md**: Structured template for presenting resume analysis

## Knowledge Base

This skill leverages expert advice from:
- r/EngineeringResumes Wiki (formatting, STAR/CAR methods)
- Tech Interview Handbook (FAANG strategies, XYZ formula)
- Hiring Manager insights (Meta, defense/aerospace)
- SRE Interviewer perspective (technical screening criteria)
- Recruiter best practices (ex-Amazon/Google recruiters)
- Jobscan research (2.5M+ resume analysis)

## Example Usage

### Basic Resume Review
```
User: "Can you review my resume?"

Claude: [Activates resume-optimizer skill]
[Reads will_cygan_resume.typ]
[Analyzes across all dimensions]
[Provides structured optimization report]
```

### Job-Specific Tailoring
```
User: "Tailor my resume for this Senior Backend Engineer role"
[Pastes job description]

Claude: [Activates resume-optimizer skill]
[Analyzes job description for keywords]
[Maps current resume to requirements]
[Provides specific tailoring recommendations]
```

### Bullet Point Improvement
```
User: "How can I improve this bullet: 'Worked on microservices using Docker and Kubernetes'"

Claude: [Activates resume-optimizer skill]
[Applies STAR/XYZ/CAR frameworks]
[Suggests quantified alternatives with Typst syntax]
```

## Output Format

Reports organized by priority:
- 🔴 **Critical Issues**: Must-fix problems (formatting, weak verbs, missing STAR)
- 🟡 **Improvements**: Optimization opportunities (better quantification, stronger verbs)
- 🟢 **Enhancements**: Additional polish (job-specific tailoring, advanced strategies)

Each recommendation includes:
- Current state
- Specific issue identified
- Concrete fix with example
- Rationale citing expert sources

## Key Principles

1. **Evidence-based**: Every recommendation backed by hiring manager insights or research
2. **Specific**: No generic advice - concrete examples for every suggestion
3. **Actionable**: Clear before/after examples with Typst syntax when relevant
4. **Comprehensive**: Covers formatting, content, ATS, and job-specific tailoring
5. **Prioritized**: Critical fixes first, enhancements later

## Success Criteria

An optimized resume will:
- ✅ Pass the 10-second scan test (key info immediately visible)
- ✅ Follow STAR/XYZ/CAR for all bullets
- ✅ Use strong action verbs (no "helped", "worked on", "assisted")
- ✅ Quantify achievements where possible
- ✅ Maintain 1-2 line bullets maximum
- ✅ Include relevant keywords naturally
- ✅ Format cleanly for ATS parsing
- ✅ Fit on single page (unless 10+ YoE senior role)

## Research Citations

Key findings incorporated:
- Including target job title → **10.2x more interview requests** (Jobscan)
- 99.7% of recruiters use keyword filters in ATS (Jobscan)
- Hiring managers spend **10-15 seconds** on initial resume scan
- 70% of resumes have **basic formatting issues** (hiring manager data)
- Both PDF and Word formats parse equally well in modern ATS

## Integration with Project

This skill understands the Typst resume project structure:
- Source file: `will_cygan_resume.typ`
- Template: modern-cv (v0.8.0)
- Build: `deno task compile` or `typst compile`
- Preview: `deno task dev` or `typst watch`

Recommendations include Typst-specific syntax when suggesting changes.

## Continuous Improvement

The skill references the `/advice` directory for the latest best practices and can incorporate new methodologies as they're added to the knowledge base.
