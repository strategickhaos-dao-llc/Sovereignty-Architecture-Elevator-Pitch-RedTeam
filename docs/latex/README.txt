================================================================================
 SACSE Framework - Appendix B LaTeX Publication Files
 README.txt - Compile Instructions and Notes
================================================================================

This directory contains the complete, publication-ready LaTeX source files for
Appendix B of the Strategickhaos Autonomous Cognitive-Systems Engineering (SACSE)
Framework documentation.

FILES INCLUDED
--------------
  appendixB.tex  - IEEEtran-compatible LaTeX source containing:
                   * Section 4.7: Interpretation and Analysis Guidelines
                   * Appendix B: Sanitized Catalog of 100 Engineering Techniques
                   * All redaction markers preserved as [REDACTED — OPERATIONAL SAFETY]

  references.bib - Complete IEEE-style BibTeX bibliography containing:
                   * 100+ peer-reviewed citations
                   * All public, scholarly sources
                   * No operational secrets or sensitive implementation details

  README.txt     - This file


COMPILATION INSTRUCTIONS
------------------------
Method 1: Using pdflatex and bibtex (recommended)
  
  $ pdflatex appendixB
  $ bibtex appendixB
  $ pdflatex appendixB
  $ pdflatex appendixB

  Note: Running pdflatex twice after bibtex ensures all cross-references
  and citations are properly resolved.

Method 2: Using latexmk (automated)

  $ latexmk -pdf appendixB

  latexmk will automatically run pdflatex and bibtex the necessary number
  of times to resolve all references.

Method 3: Using Overleaf or online LaTeX editors

  1. Upload both appendixB.tex and references.bib to your project
  2. Ensure the main document is set to appendixB.tex
  3. Compile using the default PDF compiler


REQUIRED PACKAGES
-----------------
The following LaTeX packages are required (typically included in standard
TeX distributions like TeX Live or MiKTeX):

  - IEEEtran (document class)
  - cite
  - amsmath, amssymb, amsfonts
  - algorithmic
  - graphicx
  - textcomp
  - hyperref
  - appendix


REDACTION POLICY
----------------
All operationally sensitive implementation details have been redacted and
marked with [REDACTED — OPERATIONAL SAFETY]. This includes:

  * Specific configuration parameters
  * Implementation code or pseudocode
  * System architecture details that could enable misuse
  * Any information that could compromise operational security

The redaction markers are intentional and should be preserved in the
final publication. They indicate that detailed implementation is available
through appropriate access-controlled channels.


PROVENANCE AND INTEGRITY
------------------------
All files in this package are processed through the SACSE documentation
pipeline which maintains:

  * Cryptographic checksums for integrity verification
  * Timestamp attestation for version control
  * Actor identification for audit trails

The preprocessing pipeline is defined in:
  - strategickhaos_chat_disclaimer.yaml (manifest)
  - strategickhaos_disclaimer.py (processing script)


CITATION FORMAT
---------------
The bibliography follows IEEE citation style. All entries reference:

  * Peer-reviewed journal articles
  * Conference proceedings
  * Technical reports from recognized standards bodies
  * Foundational textbooks in the field

No proprietary or restricted sources are cited.


TECHNIQUE CATALOG STRUCTURE
---------------------------
The 100 techniques are organized into 10 thematic clusters:

  Cluster 1:  Distributed Cognition Foundations (1-10)
  Cluster 2:  Active Inference and Predictive Processing (11-20)
  Cluster 3:  Retrieval-Augmented Generation (21-30)
  Cluster 4:  Cryptographic Provenance (31-40)
  Cluster 5:  Reproducibility Engineering (41-50)
  Cluster 6:  Security and Threat Modeling (51-60)
  Cluster 7:  Human-AI Collaboration (61-70)
  Cluster 8:  Language Model Engineering (71-80)
  Cluster 9:  Ethical AI and Governance (81-90)
  Cluster 10: Advanced and Emerging Techniques (91-100)

Each technique entry includes:
  - Technique number and title
  - Neutral, scholarly description
  - One or more peer-reviewed citations
  - Redacted implementation placeholder


OUTPUT FORMAT
-------------
The compiled PDF will be formatted according to IEEE journal standards:

  * Two-column layout
  * 10pt font size
  * Numbered references
  * Hyperlinked citations and cross-references


SUPPORT
-------
For questions about compilation or content, please refer to:

  * Repository: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
  * Documentation: See SECURITY.md for responsible disclosure policies


================================================================================
 Copyright (c) Strategickhaos DAO LLC
 Licensed under MIT License - See LICENSE file in repository root
================================================================================
