# SACSE IEEE Manuscript

This directory contains the IEEE-style LaTeX manuscript for the Sovereignty Architecture Cognitive Systems Engineering (SACSE) framework.

## 📁 Files

| File | Description |
|------|-------------|
| `main.tex` | Main IEEE manuscript skeleton with placeholders |
| `appendixA.tex` | Appendix with 100 engineering techniques (include mode) |
| `references.bib` | BibTeX database with all citations (web0–web99) |

## 🔧 Compilation

### Option A: Standard BibTeX (Recommended)

```bash
cd papers/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Option B: Using latexmk (Automated)

```bash
cd papers/
latexmk -pdf main.tex
```

### Option C: Overleaf

1. Upload all three files (`main.tex`, `appendixA.tex`, `references.bib`) to an Overleaf project
2. Click **Recompile** — Overleaf runs the BibTeX chain automatically

## 📖 Structure

### Main Document (`main.tex`)

The main document follows IEEE conference format (`IEEEtran` document class) and includes:

- Title and author block (placeholders to fill)
- Abstract
- Keywords
- Standard IEEE sections (Introduction, Background, Methodology, Implementation, Evaluation, Discussion, Conclusion)
- Appendix integration via `\input{appendixA}`
- Bibliography using `IEEEtran` style

### Appendix (`appendixA.tex`)

Contains 100 engineering techniques organized into 10 clusters:

1. **Cognitive Architecture Foundations** (Techniques 1–10)
2. **Distributed Consensus Mechanisms** (Techniques 11–20)
3. **Knowledge Representation and Reasoning** (Techniques 21–30)
4. **Security and Sovereignty Patterns** (Techniques 31–40)
5. **Agent Communication and Coordination** (Techniques 41–50)
6. **Learning and Adaptation Systems** (Techniques 51–60)
7. **Interpretability and Alignment** (Techniques 61–70)
8. **Infrastructure and Deployment** (Techniques 71–80)
9. **Evaluation and Benchmarking** (Techniques 81–90)
10. **Governance and Compliance** (Techniques 91–100)

Each technique includes:
- A concise description at publishable abstraction level
- Citation reference (e.g., `\cite{web0}`)
- `[REDACTED]` markers where dual-use implementation details are omitted

### References (`references.bib`)

100 BibTeX entries (keyed `web0` through `web99`) covering:
- Foundational AI/cognitive science papers
- Distributed systems literature
- Security and cryptography standards
- Multi-agent systems specifications
- Machine learning benchmarks
- Governance and compliance frameworks

## 📝 Usage Notes

### Important: BibTeX vs. Biber

This project uses **classic BibTeX**, not biblatex/biber:

- ✅ `\bibliographystyle{IEEEtran}` + `\bibliography{references}`
- ❌ `\usepackage[backend=biber]{biblatex}` + `\addbibresource{}`

If you want to switch to biblatex/biber, you'll need to:
1. Replace `\usepackage{cite}` with `\usepackage[backend=biber,style=ieee]{biblatex}`
2. Replace `\bibliography{references}` with `\addbibresource{references.bib}` and `\printbibliography`

### Appendix Integration

The appendix is designed for "include mode" — it has no `\documentclass` or `\begin{document}` wrapper. It's included via:

```latex
\appendix
\input{appendixA}
```

### Referencing the Appendix

In the main text, reference the appendix using:

```latex
See Appendix~\ref{sec:appendix-techniques} for the full catalog of 100 
techniques with detailed descriptions and citations.
```

## 🎯 Appendix Overview (for Methodology Section)

> The SACSE methodology is supported by a comprehensive catalog of 100 engineering techniques, fully documented in Appendix A. These techniques span ten thematic clusters—from cognitive architecture foundations and distributed consensus mechanisms to interpretability, alignment, and governance compliance. Each technique is presented at a neutral, publishable abstraction level with appropriate citations to foundational literature. Implementation-specific details that may present dual-use concerns are marked as redacted. This modular catalog enables practitioners to selectively adopt techniques appropriate to their specific system requirements while maintaining traceability to established engineering practices.

## 📄 License

This manuscript template is provided for academic and research purposes. Please ensure proper attribution when using or adapting this work.

## 🔗 Related Resources

- [IEEEtran Documentation](https://ctan.org/pkg/ieeetran)
- [IEEE Author Center](https://ieeeauthorcenter.ieee.org/)
- [Overleaf IEEE Templates](https://www.overleaf.com/gallery/tagged/ieee-official)
