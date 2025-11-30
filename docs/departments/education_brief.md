# Education & Curriculum Department Brief

> **Target Audience:** Education & Curriculum Department  
> **Goal:** Use the 100 questions as a modular learning framework (SNHU-aligned, Bloom Level 5–6)

---

## Overview

This document explains how the Education & Curriculum department can use the 100 Bloom's Taxonomy questions as the foundation for a comprehensive BS/CS curriculum, integrated with AI-generated educational videos.

---

## Mapping of All 100 Questions by Module + Difficulty

### Module 1: Foundations of Computing (Q001-Q017)

| Question | Bloom Level | Difficulty | Prerequisites | Learning Outcome |
|----------|-------------|------------|---------------|------------------|
| Q001 | 5 (Evaluate) | Medium | None | Evaluate architectural trade-offs |
| Q002 | 5 (Evaluate) | Medium | Q001 | Assess security implications |
| Q003 | 5 (Evaluate) | Medium | Q001 | Evaluate development methodologies |
| Q004 | 5 (Evaluate) | Hard | Algorithms basics | Compare algorithm efficiency |
| Q005 | 5 (Evaluate) | Hard | Q001, Q004 | Assess technology trends |
| Q006 | 6 (Create) | Hard | Q001-Q005 | Design disaster recovery |
| Q007 | 6 (Create) | Medium | Q002 | Develop evaluation framework |
| Q008 | 6 (Create) | Hard | Q002, Q006 | Create security checklist |
| Q009 | 6 (Create) | Hard | Q003, Q006 | Design CI/CD pipeline |
| Q010 | 6 (Create) | Medium | Q002 | Construct governance policy |
| Q011-Q017 | Mixed | Varied | See question file | Various outcomes |

### Module 2: Infrastructure & Cloud Architecture (Q018-Q034)

| Focus Area | Questions | Key Competencies |
|------------|-----------|------------------|
| Cloud Economics | Q011-Q012 | Cost-benefit analysis, vendor assessment |
| Container Orchestration | Q013 | Platform comparison and selection |
| Security Architecture | Q014-Q015 | Zero-trust, IaC effectiveness |
| Architecture Design | Q016-Q020 | Multi-cloud, capacity planning, observability |

### Module 3: Security & Compliance (Q035-Q051)

| Focus Area | Questions | Key Competencies |
|------------|-----------|------------------|
| Frameworks | Q021-Q022 | NIST CSF, security testing approaches |
| Legal Compliance | Q023-Q025 | CFAA, security awareness |
| Defensive Operations | Q026-Q030 | Security programs, incident response |

### Module 4: AI & Machine Learning Operations (Q052-Q068)

| Focus Area | Questions | Key Competencies |
|------------|-----------|------------------|
| AI Ethics | Q031-Q035 | Content ethics, bias, sustainability |
| AI Governance | Q036-Q040 | Governance frameworks, evaluation |

### Module 5: Business Strategy & Governance (Q069-Q085)

| Focus Area | Questions | Key Competencies |
|------------|-----------|------------------|
| Organizational Structure | Q041-Q045 | DAO vs LLC, fiduciary duties, governance |
| Strategic Planning | Q046-Q050 | Planning, risk management, communication |

### Module 6: Educational Technology & Pedagogy (Q086-Q100)

| Focus Area | Questions | Key Competencies |
|------------|-----------|------------------|
| Learning Design | Q051-Q055 | Instruction methods, personalization |
| Assessment | Q056-Q060 | Curriculum design, rubrics, analytics |
| Capstone Integration | Q061-Q100 | Cross-domain synthesis projects |

---

## Suggested Sequence & Prerequisites

### Recommended Learning Path

```
                    ┌─────────────────┐
                    │    Module 1     │
                    │   Foundations   │
                    │   (Q001-Q017)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │  Module 2  │  │  Module 3  │  │  Module 4  │
     │   Infra    │  │  Security  │  │   AI/ML    │
     │(Q018-Q034) │  │(Q035-Q051) │  │(Q052-Q068) │
     └──────┬─────┘  └──────┬─────┘  └──────┬─────┘
            │               │               │
            └───────────────┴───────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │    Module 5    │
                   │    Business    │
                   │  (Q069-Q085)   │
                   └────────┬───────┘
                            │
                            ▼
                   ┌────────────────┐
                   │    Module 6    │
                   │    EdTech +    │
                   │    Capstone    │
                   │  (Q086-Q100)   │
                   └────────────────┘
```

### Prerequisites by Question

**No Prerequisites (Entry Points):**
- Q001 (Architecture fundamentals)
- Q011 (Cloud economics)
- Q021 (Security frameworks)
- Q031 (AI ethics)
- Q041 (Business structures)

**Requires Prior Questions:**
- Q006-Q010: Require Q001-Q005
- Q016-Q020: Require Q011-Q015
- Q026-Q030: Require Q021-Q025
- All Module 6: Require completion of Modules 1-5

---

## Instructions for Using AI Videos in Class or Self-Study

### For Instructors (Classroom Use)

#### Before Class
1. **Review the AI Video:** Watch the video for the question being covered
2. **Prepare Discussion Points:** Note areas for deeper exploration
3. **Identify Supplementary Materials:** Find case studies or examples

#### During Class
1. **Introduction (5 min):** Frame the question and learning objectives
2. **Video Viewing (10-15 min):** Play the AI-generated video
3. **Guided Discussion (15-20 min):** 
   - What did you find most compelling?
   - What would you add or challenge?
   - How does this apply to real-world scenarios?
4. **Application Activity (20-30 min):** Hands-on exercise related to question

#### After Class
1. **Assign Assessment:** Use rubric to evaluate student responses
2. **Provide Feedback:** Connect back to learning objectives
3. **Track Progress:** Record completion in learning management system

### For Self-Study (Independent Learners)

#### Study Session Structure
1. **Preview (5 min):** Read the question and identify what you already know
2. **Watch Video (10-15 min):** Take notes on key concepts
3. **Reflect (10 min):** Summarize the main points in your own words
4. **Apply (20-30 min):** Complete the associated assessment
5. **Review (5 min):** Check your understanding against the rubric

#### Tips for Self-Study Success
- Study in a distraction-free environment
- Take handwritten notes for better retention
- Discuss with peers or online communities
- Revisit challenging questions after completing related content

### Accessing the Videos

**Via KnowledgePod (Recommended):**
```
https://learn.strategickhaos.io/pod/q001
https://learn.strategickhaos.io/pod/q002
...
```

**Via Direct CDN (Backup):**
```
https://cdn.strategickhaos.io/videos/q001.mp4
https://cdn.strategickhaos.io/videos/q002.mp4
...
```

---

## Assessment Ideas and Rubrics (Bloom Level 5–6)

### Assessment Types by Bloom Level

#### Level 5 (Evaluate) Assessments

**Written Analysis (1000-1500 words)**
- Present a scenario and ask students to evaluate options
- Require evidence-based reasoning
- Include pros/cons analysis

**Comparative Assessment**
- Compare two or more approaches/technologies
- Justify preference with criteria
- Acknowledge trade-offs

**Case Study Critique**
- Provide a real-world case study
- Ask students to identify strengths and weaknesses
- Recommend improvements

#### Level 6 (Create) Assessments

**Design Project**
- Create an original design (architecture, policy, framework)
- Document design decisions and rationale
- Defend design in peer review

**Implementation Project**
- Build a working prototype or proof-of-concept
- Document implementation process
- Reflect on lessons learned

**Capstone Portfolio**
- Synthesize learning across multiple modules
- Create comprehensive deliverable
- Present to panel or stakeholders

### Universal Rubric (Bloom Level 5-6)

| Criterion | Exemplary (4) | Proficient (3) | Developing (2) | Beginning (1) |
|-----------|---------------|----------------|----------------|---------------|
| **Analysis Depth** | Comprehensive analysis with multiple perspectives and nuanced understanding | Thorough analysis with most key perspectives addressed | Adequate analysis but missing some perspectives | Superficial analysis lacking depth |
| **Evidence Quality** | Strong, relevant evidence from multiple authoritative sources | Adequate evidence from appropriate sources | Limited evidence or questionable sources | Minimal or no supporting evidence |
| **Reasoning** | Logical, coherent reasoning with clear connections | Generally logical with minor gaps | Some logical gaps or unclear connections | Illogical or disjointed reasoning |
| **Originality** | Innovative approach with creative insights | Original thinking with some creative elements | Some original ideas but mostly conventional | Relies primarily on existing approaches |
| **Communication** | Clear, professional, well-organized presentation | Generally clear with good organization | Adequate clarity but some organizational issues | Unclear or poorly organized |
| **Application** | Strong connection to real-world contexts with practical implications | Good connection to practical applications | Some connection to practice | Minimal practical application |

### Sample Assessment: Q001 (Monolithic vs Microservices)

**Prompt:**
> You are advising a startup that has raised $2M in seed funding and plans to launch their MVP in 6 months. They need to choose between a monolithic architecture and microservices. Evaluate the trade-offs and make a recommendation with justification.

**Rubric Application:**

| Criterion | What to Look For |
|-----------|------------------|
| Analysis Depth | Considers team size, timeline, budget, technical debt, scalability needs |
| Evidence Quality | References industry case studies, framework documentation, expert opinions |
| Reasoning | Clear logical flow from analysis to recommendation |
| Originality | Creative consideration of hybrid approaches or phased migration |
| Communication | Professional memo format, executive summary, clear structure |
| Application | Specific to startup context, acknowledges real constraints |

### Module Completion Requirements

| Module | Assessments Required | Passing Threshold |
|--------|---------------------|-------------------|
| Module 1 | 3 evaluations + 2 designs | 75% average |
| Module 2 | 3 evaluations + 2 designs | 75% average |
| Module 3 | 2 evaluations + 3 designs | 80% average (security-critical) |
| Module 4 | 2 evaluations + 2 designs | 75% average |
| Module 5 | 3 evaluations + 2 designs | 75% average |
| Module 6 | 1 evaluation + Capstone project | 80% average |

---

## SNHU Alignment Notes

### Competency Mapping

The 100 questions align with SNHU's competency-based education model:

| SNHU Competency | Questions Addressing |
|-----------------|---------------------|
| Critical Thinking | All Level 5 questions |
| Technical Skills | Modules 1-4 |
| Business Acumen | Module 5 |
| Communication | All assessment responses |
| Ethics | Q023, Q031-Q040 |

### Credit Equivalency (Suggested)

- **Module 1-6 Completion:** Equivalent to 3-credit upper-division course
- **Capstone Completion:** Equivalent to additional 3-credit capstone course
- **Full Program:** 6 credit-hour equivalency

---

## Support Resources

### For Instructors
- Office hours with curriculum team
- Instructor guide (detailed facilitation notes)
- Assessment bank with additional questions

### For Students
- Peer study groups
- Tutoring support
- Accessibility accommodations

### Technical Support
- Video playback issues: support@strategickhaos.io
- Platform access: access@strategickhaos.io

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-30 | Education Team | Initial brief |

**Classification:** Internal - Education Department
