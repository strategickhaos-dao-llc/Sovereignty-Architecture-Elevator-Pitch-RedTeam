# Overleaf Deployment Guide for LaTeX Pre-Print

## What is Overleaf?

**Overleaf** is a free, collaborative, cloud-based LaTeX editor that provides:
- Real-time LaTeX compilation
- No local LaTeX installation needed
- PDF preview and download
- Version control and collaboration
- Templates and examples
- GitHub synchronization

**URL:** https://www.overleaf.com

---

## Quick Start (5 Minutes)

### Step 1: Create Overleaf Account

```
1. Navigate to: https://www.overleaf.com/register
2. Choose sign-up method:
   - Email (recommended for academic work)
   - Google Account
   - ORCID (direct academic integration)
   - GitHub (for code/paper integration)
3. Verify email address
4. Complete profile setup
```

### Step 2: Create New Project

**Option A: Upload Existing LaTeX File**
```
1. Click "New Project" (top left)
2. Select "Upload Project"
3. Choose file upload method:
   - Upload .tex file directly
   - Upload ZIP with all files
   - Recommended: Upload just the .tex file first
4. Name project: "Sovereignty Architecture Pre-Print"
5. Click "Create"
```

**Option B: Start from Blank Template**
```
1. Click "New Project"
2. Select "Blank Project"
3. Name: "Sovereignty Architecture Pre-Print"
4. Copy-paste LaTeX content from repository
5. Click "Recompile" to generate PDF
```

---

## Uploading Your Paper

### Prepare Files Locally

```bash
cd /home/runner/work/Sovereignty-Architecture-Elevator-Pitch-/Sovereignty-Architecture-Elevator-Pitch-/academic/preprints/

# Your main file:
sovereignty-architecture-preprint.tex

# Any images or additional files (if needed):
# - figures/
# - references.bib
```

### Upload to Overleaf

**Method 1: Direct File Upload**
```
1. Open your Overleaf project
2. Click "Upload" button (top left)
3. Select "sovereignty-architecture-preprint.tex"
4. File appears in project file list
5. Click "Recompile" to generate PDF
```

**Method 2: Copy-Paste Content**
```
1. Open sovereignty-architecture-preprint.tex locally
2. Copy all content (Ctrl+A, Ctrl+C)
3. In Overleaf, open main.tex
4. Paste content (Ctrl+V)
5. Rename file to sovereignty-architecture-preprint.tex (optional)
6. Click "Recompile"
```

---

## Compiling Your Document

### First Compilation

```
1. Ensure main .tex file is open in editor
2. Click "Recompile" button (top right)
3. Wait for compilation (usually 5-30 seconds)
4. PDF preview appears on right side
5. Check for errors in compile log (bottom)
```

### Troubleshooting Compilation Errors

**Common Error: Missing Package**
```
Error: ! LaTeX Error: File 'somepackage.sty' not found.

Solution:
- Overleaf includes most packages automatically
- Check package name spelling
- Some specialized packages may not be available
- Consider using alternative packages
```

**Common Error: Encoding Issues**
```
Error: Unicode character errors

Solution:
- Ensure document uses UTF-8 encoding
- Check for special characters
- Use LaTeX commands for special symbols (e.g., \$ instead of $)
```

**Common Error: Bibliography Issues**
```
Error: Citation undefined

Solution:
- If using BibTeX, recompile twice (for cross-references)
- Verify .bib file is uploaded
- Check citation keys match
```

### Compilation Settings

```
1. Click "Menu" (top left hamburger icon)
2. Settings section shows:
   - Compiler: pdfLaTeX (default, recommended)
   - TeX Live version: 2024 (latest)
   - Main document: sovereignty-architecture-preprint.tex
   - Spell check: English (US)
3. Adjust as needed
```

---

## Editing and Refinement

### LaTeX Editor Features

**Syntax Highlighting:**
- Commands highlighted in blue
- Comments in gray
- Math mode in different color
- Errors underlined in red

**Auto-Complete:**
- Start typing `\` for command suggestions
- Common commands auto-complete
- Citation keys auto-complete

**Error Detection:**
- Red underlines for syntax errors
- Click error message to jump to line
- Compile log shows detailed errors

### Making Changes

**Update Content:**
```latex
% Make edits directly in the editor
% Example: Update date
\date{November 23, 2025}

% Example: Update ORCID
ORCID: 0000-0003-XXXX-XXXX  % Replace XXXX with actual numbers

% Example: Update patent application numbers
Application Number: XXXXXX  % Add after filing
```

**Preview Changes:**
```
1. Make edits in left editor pane
2. Click "Recompile" or enable "Auto Compile"
3. PDF preview updates automatically
4. Verify changes look correct
```

---

## Downloading Your PDF

### Quick Download

```
1. Ensure document has compiled successfully
2. Look at PDF preview (right pane)
3. Click "Download PDF" button (top right)
4. PDF saves to your Downloads folder
5. Filename: sovereignty-architecture-preprint.pdf
```

### Download Options

**Download PDF Only:**
```
Menu → Download → PDF
- Fastest option
- Just the compiled PDF
- For sharing and uploading
```

**Download Source:**
```
Menu → Download → Source (ZIP)
- Includes all .tex files
- Includes any images/assets
- For backup and archiving
- For sharing source code
```

**Download PDF with Comments:**
```
Menu → Download → PDF with submission content
- Useful if using review features
- Includes tracked changes
```

---

## File Management

### Adding Bibliography

If you want to add a .bib file for references:

```latex
% In your .tex file, add before \end{document}:
\bibliographystyle{plain}
\bibliography{references}

% Then upload references.bib file:
1. Click "Upload" in Overleaf
2. Select references.bib
3. Recompile (may need to compile twice)
```

**Example references.bib:**
```bibtex
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and others},
  journal={Advances in neural information processing systems},
  volume={30},
  year={2017}
}
```

### Adding Images

If including figures:

```latex
% In preamble:
\usepackage{graphicx}

% In document:
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{architecture-diagram.png}
\caption{Sovereignty Architecture Overview}
\label{fig:architecture}
\end{figure}
```

**Upload image:**
```
1. Click "Upload" in Overleaf
2. Select image file (PNG, JPG, PDF)
3. Place in figures/ folder (optional)
4. Reference in LaTeX as shown above
```

---

## Collaboration Features (Optional)

### Sharing Your Project

**View-Only Link:**
```
1. Click "Share" button
2. Copy "Link sharing" URL
3. Set to "View" or "Edit" permissions
4. Share with collaborators or reviewers
```

**Invite Collaborators:**
```
1. Click "Share" button
2. Enter collaborator email
3. Choose permission level:
   - Can Edit (full access)
   - Can View (read-only)
4. Send invitation
```

### Track Changes

```
1. Menu → Review
2. Enable "Track changes"
3. Edits appear as suggestions
4. Accept/Reject changes
5. Useful for revision process
```

---

## Version Control

### Automatic History

Overleaf automatically saves versions:
```
1. Click "History" button (top right)
2. See all document versions
3. Click any version to preview
4. Restore previous version if needed
5. Compare versions side-by-side
```

### Manual Labels

Mark important versions:
```
1. In History view
2. Click version timestamp
3. Add label (e.g., "Submitted to Zenodo", "v1.0")
4. Labels make versions easy to find
```

---

## GitHub Synchronization (Advanced)

### Link to GitHub

```
1. Menu → GitHub
2. Click "Link to GitHub"
3. Authorize Overleaf
4. Select repository: Sovereignty-Architecture-Elevator-Pitch-
5. Choose branch: main
6. Two-way sync enabled
```

**Benefits:**
- Automatic backup to GitHub
- Work offline with local LaTeX
- Sync with Overleaf for collaboration
- Version control in both systems

**Sync Workflow:**
```
1. Edit in Overleaf
2. Click "GitHub" → "Push to GitHub"
3. Changes committed to repository
4. Or edit locally, push to GitHub
5. Overleaf pulls changes automatically
```

---

## Publishing Checklist

Before uploading to Google Scholar or Zenodo:

- [ ] Document compiles without errors
- [ ] Title is complete and accurate
- [ ] Author name and affiliation correct
- [ ] ORCID added (after registration)
- [ ] Abstract is comprehensive
- [ ] All sections completed
- [ ] References formatted correctly
- [ ] Patent application numbers added (after filing)
- [ ] Contact information verified
- [ ] Date is current
- [ ] License information included
- [ ] No placeholder text (XXXX) remaining
- [ ] Spell-check completed
- [ ] PDF downloads successfully
- [ ] PDF is readable and well-formatted

---

## After Compilation

### Save Your PDF

```
1. Download PDF from Overleaf
2. Save as: sovereignty-architecture-preprint.pdf
3. Verify file opens correctly
4. Check all pages render properly
5. Verify no compilation artifacts
```

### Upload to Zenodo

```
1. Go to https://zenodo.org/deposit/new
2. Upload the compiled PDF
3. Complete metadata form
4. Publish and obtain DOI
5. Update LaTeX with DOI for future versions
```

### Upload to Google Scholar

```
Google Scholar indexes from:
- Your institutional repository (SNHU)
- Zenodo (automatic indexing)
- ArXiv (if submitted)
- Personal website (if configured)

Best approach:
1. Upload to Zenodo first
2. Wait 24-48 hours
3. Search Google Scholar
4. Claim paper in your profile
```

### Update Repository

```bash
# Add compiled PDF to repository
git add academic/preprints/sovereignty-architecture-preprint.pdf
git commit -m "Add compiled LaTeX pre-print PDF"
git push

# Update README with DOI badge and citation
```

---

## Templates and Resources

### Overleaf Gallery

Browse templates for inspiration:
```
1. Gallery → Academic Journals
2. Gallery → Conference Papers
3. Gallery → Theses
4. Pick template, click "Open as Template"
5. Customize for your needs
```

### Recommended Templates

- **IEEE Conference Template** - Professional formatting
- **ACM Article Template** - Well-structured academic style
- **ArXiv Template** - Pre-print standard
- **Springer LNCS** - Computer science papers

### LaTeX Resources

**Documentation:**
- Overleaf Learn: https://www.overleaf.com/learn
- LaTeX Wikibook: https://en.wikibooks.org/wiki/LaTeX
- CTAN Package Repository: https://ctan.org

**Support:**
- Overleaf Contact: help@overleaf.com
- StackExchange LaTeX: https://tex.stackexchange.com
- Overleaf Twitter: @overleaf

---

## Tips and Best Practices

### Performance Optimization

```
- Large projects: Split into multiple .tex files with \input{}
- Many images: Use compressed formats (PNG, JPG)
- Compile speed: Use fast compile mode (Menu → Settings)
- Preview: Use Auto Compile for immediate feedback
```

### Common LaTeX Commands

**Formatting:**
```latex
\textbf{bold text}
\textit{italic text}
\underline{underlined}
\texttt{monospace/code}
```

**Lists:**
```latex
\begin{itemize}
\item First item
\item Second item
\end{itemize}

\begin{enumerate}
\item Numbered item
\item Another item
\end{enumerate}
```

**Math:**
```latex
Inline: $E = mc^2$
Display: \[E = mc^2\]
```

**Links:**
```latex
\href{https://example.com}{Link text}
\url{https://example.com}
```

---

## Troubleshooting

### Common Issues

**Problem:** PDF not updating
```
Solution:
- Click "Recompile" button
- Try "Recompile from scratch"
- Check compile log for errors
- Clear cache (Menu → Settings → Clear cached files)
```

**Problem:** Slow compilation
```
Solution:
- Reduce image sizes
- Use fast compile mode
- Split large document into parts
- Upgrade to Overleaf Premium (optional)
```

**Problem:** Lost work
```
Solution:
- Use History feature to recover
- Overleaf auto-saves every few seconds
- Check "History" → find last good version
- Download source regularly as backup
```

---

## Final Steps

### After Successful Compilation

1. **Download PDF**
   - sovereignty-architecture-preprint.pdf
   - Save to multiple locations

2. **Upload to Zenodo**
   - Get DOI for permanent citation
   - Enable long-term preservation

3. **Update ORCID**
   - Add pre-print to profile
   - Link via DOI

4. **Share Widely**
   - X/Twitter announcement
   - LinkedIn post
   - Academic networks
   - GitHub README update

5. **Track Impact**
   - Google Scholar citations
   - Zenodo download statistics
   - Social media engagement
   - Academic mentions

---

**Status:** READY FOR COMPILATION  
**Estimated Time:** 5-10 minutes (account setup + upload + compile)  
**Cost:** FREE (Overleaf free tier is sufficient)  
**Last Updated:** 2025-11-23

---

**Next Steps:**
1. Create Overleaf account at https://www.overleaf.com/register
2. Upload sovereignty-architecture-preprint.tex
3. Compile and verify PDF
4. Download final PDF
5. Upload to Zenodo for DOI
6. Update all references with DOI
7. Share your published work!

**Your compiled PDF will be ready in minutes! 🚀**
