# Unsolicited Perspective from a SRE Interviewer

If one were to design a bingo card for r/itcareerquestions, the proverbial center piece would be the "How do I get out of helpdesk and into xyz" square. In fact, if you look up "Getting out of helpdesk" in the search bar, there are no fewer than 100+ odd posts inquiring about the same topic.

These posts suggest combination of few things:
- Homelab
- Certification
- School
- "Extra" work experience

and those suggestions are pretty helpful for getting someone started on that journey out of helpdesk. However, I have not seen a post that shares the perspectives from one of these cloud engineering teams and I think that insight could be helpful for people looking to move into these roles.

> "Naw"
> -Rosa Parks, when asked to troubleshoot a printer, 1964

I also started off from a help desk position and this subreddit (as well as r/linuxadmin) provided indispensable information on what to work on. u/jeffbx also was super kind enough to respond to my personal DMs (plz no leak) when I needed some validation on some of my next moves. I want to pay that kindness forward so here I am with this post.

## Perspective from a hiring team:

There are two types of SRE/Cloud/DevOps/Platform roles: **revenue center roles** vs **cost center roles**. Engineers belonging to the revenue center are typically staff members who report to a business unit under a CTO or VP of Engineering. They are primarily tasked with working on production systems that are front-office/client facing. These roles generally pay more and are more closely aligned with software engineering teams. This has an interesting implication; it usually means these roles will have more whiteboarding/hackerrank type of questions embedded in their interview process. Engineers belonging to cost center roles usually report under CIO/CISO and maintain systems that are back-office facing (Active Directory, internal tooling, VMs being used by different teams). These roles tend to have more systems design questions rather programming questions in the interview process. The cloud roles that are in cost-center business unit are usually more reachable by help desk applicants due to cultural similarities.

My team handles both functions (probably going to get split in the not too distant future). Hiring practices vary by teams, orgs and industries, but our team streamlines applicants into two main hiring pipeline: **Experienced (L5+)** and **Junior/New-Grad/Change-of-career (L3 - L4)**. Most people looking to jump out of help desk rarely fall into experienced hire bucket so I'll skip the experienced one. For the inexperienced hire bucket, my team does a 4-stage interview process, which I think is pretty standard:

1. HR Screen
2. Engineering Screen
3. Engineering Interview
4. Panel Interview (including the manager)

The functions of each stage is different, but they primarily aim to answer two key questions:

1. Are they able to work at the 70% pace of our experienced hires in a year from now (and show growth potential)?
2. Would they make a great cultural add on to our team (so don't be toxic, be unique - but in a good way)?

## HR Screen

The HR screen is pretty standard; it determines whether the applicant is eligible to be hired. Wayne Gretzky said it best when he said you miss 100% of the shots you don't take. A good rule of thumb for a help desk applicant is to apply for roles that they meet at least 30% of the qualifications for. You're probably not the most qualified; but at least you're in the running.

A quick note on college degrees and certifications: it goes without saying that a college degree is beneficial. Our org is 95%+ engineering staff and is heavily involved in research. We are deeply-focused group working in AI, next generation energy, and pushing the boundaries of networking. Most of our staff hold a BS degree in sciences/engineering from top schools. Few of them even hold PhD's. If you can get a bachelor's degree without incurring significant cost, then please get them. It will open more doors and possibilities.

However, it is possible to get good jobs without them. I think advice from tptacek is worth a read: https://news.ycombinator.com/item?id=6915155

## Engineering Screen

Once it goes through the screen, their application and cover letter gets dumped into our hiring pipeline and must go through a quick engineering screen. 2 engineers from our team will take a quick scan at the resumes (around ~10 seconds) and then independently vote YES, NO, or MAYBE. If an applicant gets 'YES' and 'NO', then a third engineer will serve as a tie breaker. 2 MAYBE's, combination of MAYBE + YES, or 2 YES's means that an applicant will proceed to the engineering interview steps.

Our teams see many applications and we cannot spend more than 10-15 seconds per application for screens because there are so many. I went through a hair over 1000 resumes for our last hire. Many failed applications are caused by self-inflicted wounds.

### Here are some of the big NO's:

- **A text file dump in RTF**: This whitebeard thought it would be acceptable to submit a resume with grey color for text and no organization. I read it despite straining my eye and it promptly went into the NO pile.

- **"Clever" resume**: A software engineer with a javascript experience submitted his resume written in utf-8 char table. Basically you need to run that resume with .join() function to get a human-readable output. Not sure how it got through the HR screen but it went into the garbage collection.

- **Job hopping for numerous (5+) roles without any upward trajectory or pattern**: I job hopped myself so I understand job hopping but there is a limit. I had a CCNP holder who had 7 jobs in 4 years. If you have 7 jobs in 4 years, it means you never saw a full product lifecycle and never had to deal with consequences of your work. Hard pass. On a semi-related note, candidates with too much MSP experience will get a YES at this stage, but usually flounders at the subsequent stages for the same reason as above. Perhaps I can talk about this in detail for follow up posts.

Resumes must be concise, powerful, and clear. Be mindful of "sometimes less is more" and "does adding x in my resume help the interviewer help understand why I am qualified for the role?" Successful balancing of those 2 principles will usually result in passing of the first 2 steps. On a corollary, this is also a reason why one shouldn't get intimidated by high application count (a la LinkedIn Job page); half of the job applications are DOA.

### Here are some of the YES's:

- Wrote Ansible playbooks for work (even as a help desk) and showed how she was able to save time by using those playbooks instead of doing it manually.

- Provisioned Observium on AWS for polling a single juniper EX2300 for homelab

- **Interesting qualifications**: feeder school alums (i.e. UC Berkeley, USC, etc), FAANG + unicorn help desk positions, interesting projects in github, active participation in a known community (CNCF, USENIX, etc...)

These are super helpful for assessing whether the help desk applicant is ready for next steps. Even if those implementations are not production-grade for us, it helps us understand that the applicant understands our tech stack and signals to us that they're ready to make the next step. If you're in help desk, and you ONLY list help desk duties in your resume, it just tells us that you're good at help desk, and nothing more. We only know the information that you choose to disseminate, so if you have some experience with our tech (or mainstream) stack, then please list them in your resume and be able to talk about them cogently. Relevant certifications, if done well, will usually result in a "YES" for the application.

## Engineering Interview

The next step of the interview is the engineering interview. For us, 2 different engineers who didn't participate in the screen will hop on a zoom call and ask few basic technical questions:

- Figure out the function of the server with root access. Can you do the same if you don't have root access? (I expect a combination of 'systemctl --type=service', 'ss -tlnp', 'lsof')

- How would you implement redundancy on a physical server? (double PSU, RAIDs, IPMIs, etc)

- Grafana is complaining about not being able to connect to a prometheus data source. Troubleshoot it! (ping, nmap, iptables -L and -F)

- Debug this python code. (I forgot the exact code but basically it's trying to chuck an array into a method with arguments that was expecting strings and the rest of the code defaults into Exception block that returns nothing. Converting the array into a string and then passing that string into args will fix it).

- Deploy a container that serves up content via nginx with PostgreSQL (a basic dockerfile with the latest alpine, nginx, few custom configs, and postgresql line will suffice). If you can do it with podman, that'll get you get brownie points.

We are not expecting immediate, or even correct, answers; we are, however, expecting cogent thought process. We value methodical thinking process over correct answers. No one in our team, especially myself, know everything but we count on being able to figure it out eventually. Even if you can't answer the question, please try your best to break down the questions into answerable chunks and make educated guesses.

## Panel Interview

The final step is the panel interview. Everyone gets to ask 3 individual questions + 10 mandated by our team (cultural fit, diversity of thought and core competency). Successful candidates usually get 100% YESs, but we've also taken candidates that get as "low" as 70%.

This is where we really dig at work + life experience and people who are "paper tigers" fail hard and people who actually solved business problems with one of our tech stack really shine. This makes sense - we are hiring problem solvers, not test takers. Certifications makes sense when you're attempting to demonstrate minimal competency and growth potential. If you got an AWS certification, then you really ought to pair that with a tangible work experience. If your current help desk role doesn't permit it, then move into another role that grant you greater flexibility and then transition into a cloud role from there. Rome wasn't built in a day; so too won't be your career.

Other common theme that I often see is a "T-shaped competency". It basically means you're an expert at one specific thing, but then you're kind of minimally competent at everything else. One needs to demonstrate expertise in ALOT (https://roadmap.sh/devops) of things: a programming language, familiarity with OS (usually linux), exposure to the cloud platform of choice (usually AWS), some networking fundamentals, exposure to monitoring, CI/CD (Github actions), cm's (Ansible + TF), and familiarity with k8s. Chances are, if you're amazing at everything, then you're making the big bucks over in FAANGs and unicorns. I personally found candidates demonstrating competency in one specific thing and letting that shine in the interview to be the most promising and usually vote "YES" for those candidates.

I can't state this enough: if you can't get a complete live production environment experience from a cloud position, then the next best thing is solving an actual business problem at work with one of the cloud tools. You should be able to clearly state how, why, and what and talk about the problems you've faced along the way. For my interview, I was able to talk about standing up a basic Puppet master server and then managing linux workstations that way. 2 of my current colleagues were eminent experts at Puppet and we were able to talk in depth about the current state of Puppet.

Many of the cloud roles are starting to expect containers and orchestration. Running a proper production orchestration is difficult, even for us. This is why you see so many options for managed k8s (Rancher, GKE, EKS, etc.). No sane person is expecting a help desk to have experience running a production one, but if you can at least get one up running locally (k3s or minikube), I'd suspect you'd get pretty heavy approval from the hiring teams.

## Final Thoughts:

The current job market is hard for all people, including entry levels. My personal experience is that help desk people who move out successfully have combination of three things: intelligence, persistence, and luck. There are different ways to get "better" at these things:

**Intelligence (EQ + IQ + General Knowledge)**: Start reading books/technical blogs/whitepaper/scientific literature/RFCs about a topic of your interest to complement your homelab. Homelabs are really great at showing you what to do, but not necessarily great at why/how underlying things work. On this note - also go talk to people and listen. The common misconception is that getting out of help desk means you get to duck down and not deal with people. If anything, being an SRE meant you have to talk well to more people whether at work or at conferences. I found this to be a pretty good resource: https://www.youtube.com/watch?v=Unzc731iCUY

**Persistence**: Keep trying when learning a tech stack you don't understand. My first homelab (spinning up an openLDAP implementation on Ubuntu 14 on Digital Ocean) took 9 tries. I tried grokking k8s multiple times and it stuck on the third try.

**Luck** - I can't remember the post, but there was an interesting post on hacker news about creating more "luck" by taking risks. I took jobs across the country and tried unconventional things (pairing with a software engineer after work, doing unpaid SRE internship for 3 months as a side gig with a full time job, etc). It's hard to advise on this one because it's more nebulous than the other two... but I think taking more calculated risks (NOT ALL RISKS will workout) will mean more opportunities for people.

Please strategically move to your next roles, spend your time efficiently on developing new skills, and keep improving and applying. Make sure to take care of your health and good luck!