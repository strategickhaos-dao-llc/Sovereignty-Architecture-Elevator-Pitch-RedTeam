#!/bin/bash
# curl_knowledge_library.sh
# 100 completely legitimate, boringly safe, public curl one-liners
# All content is public domain, CC-0, MIT, Apache 2.0, or fair-use academic sources
# November 21, 2025 edition
# Use: Feed into local AI training, RAG folder, or Obsidian vault

set -e

# Create output directories
KNOWLEDGE_BASE_DIR="knowledge"
mkdir -p "$KNOWLEDGE_BASE_DIR"/{math,ai,pkm,security,esoteric}

echo "🔬 Knowledge Library Curator v1.0"
echo "================================================"
echo "Downloading 100 public domain knowledge sources"
echo "Output directory: $KNOWLEDGE_BASE_DIR/"
echo ""

# Counters
TOTAL=0
SUCCESS=0
FAILED=0

# Helper function to download and track
download() {
  local id="$1"
  local url="$2"
  local output="$3"
  local category="$4"
  
  TOTAL=$((TOTAL + 1))
  echo "[$TOTAL/100] $category: $id"
  
  if curl -L -s -H "User-Agent: Knowledge-Curator/1.0" \
    --max-time 120 --retry 2 --retry-delay 1 \
    "$url" -o "$KNOWLEDGE_BASE_DIR/$category/$output" 2>/dev/null; then
    
    if [ -s "$KNOWLEDGE_BASE_DIR/$category/$output" ]; then
      size=$(stat -c%s "$KNOWLEDGE_BASE_DIR/$category/$output" 2>/dev/null || stat -f%z "$KNOWLEDGE_BASE_DIR/$category/$output" 2>/dev/null || echo "0")
      if [ "$size" -gt 100 ]; then
        echo "   ✅ $output ($size bytes)"
        SUCCESS=$((SUCCESS + 1))
      else
        echo "   ⚠️  Too small: $output ($size bytes)"
        FAILED=$((FAILED + 1))
      fi
    else
      echo "   ❌ Empty: $output"
      FAILED=$((FAILED + 1))
    fi
  else
    echo "   ❌ Failed: $output"
    FAILED=$((FAILED + 1))
  fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📐 SECTION 1: Math / Proofs / Impossible Problems (1-20)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Math Resources Collection
download "math_resources" "https://raw.githubusercontent.com/rossant/awesome-math/master/README.md" "awesome_math.md" "math"

# 2. OEIS - Pi Digits
download "pi_digits" "https://oeis.org/A000796/b000796.txt" "pi_digits_10k.txt" "math"

# 3. Ramanujan's Notebooks (Gutenberg)
download "ramanujan" "https://www.gutenberg.org/files/41507/41507-0.txt" "ramanujan_notebooks.txt" "math"

# 4. Euclid's Elements (Gutenberg)
download "euclid" "https://www.gutenberg.org/files/21076/21076-0.txt" "euclid_elements.txt" "math"

# 5. Fibonacci Numbers
download "fibonacci" "https://oeis.org/A000045/b000045.txt" "fibonacci_sequence.txt" "math"

# 6. Prime Numbers
download "primes" "https://oeis.org/A000040/b000040.txt" "prime_numbers.txt" "math"

# 7. Catalan Numbers
download "catalan" "https://oeis.org/A000108/b000108.txt" "catalan_numbers.txt" "math"

# 8. Bernoulli Numbers
download "bernoulli" "https://oeis.org/A027641/b027641.txt" "bernoulli_numbers.txt" "math"

# 9. Perfect Numbers
download "perfect" "https://oeis.org/A000396/b000396.txt" "perfect_numbers.txt" "math"

# 10. Mersenne Primes
download "mersenne" "https://oeis.org/A000043/b000043.txt" "mersenne_primes.txt" "math"

# 11-20. More mathematical texts and sequences
download "newton_principia" "https://www.gutenberg.org/files/28233/28233-0.txt" "newton_principia.txt" "math"
download "descartes_geometry" "https://www.gutenberg.org/files/26400/26400-0.txt" "descartes_geometry.txt" "math"
download "pascal_pensees" "https://www.gutenberg.org/files/18269/18269-0.txt" "pascal_pensees.txt" "math"
download "math_foundations" "https://raw.githubusercontent.com/nushio3/type-natural/master/README.md" "math_foundations.md" "math"
download "number_theory" "https://raw.githubusercontent.com/mostafatouny/awesome-theoretical-computer-science/main/README.md" "cs_theory.md" "math"
download "golden_ratio" "https://oeis.org/A001622/b001622.txt" "golden_ratio_digits.txt" "math"
download "e_number" "https://oeis.org/A001113/b001113.txt" "e_number_digits.txt" "math"
download "sqrt2" "https://oeis.org/A002193/b002193.txt" "sqrt2_digits.txt" "math"
download "bell_numbers" "https://oeis.org/A000110/b000110.txt" "bell_numbers.txt" "math"
download "stirling_numbers" "https://oeis.org/A008277/b008277.txt" "stirling_numbers.txt" "math"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 SECTION 2: Sovereign / Local AI / Uncensored Lore (21-40)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 21-40. AI and ML resources
download "llama_readme" "https://raw.githubusercontent.com/meta-llama/llama/main/README.md" "llama_guide.md" "ai"
download "ollama_docs" "https://raw.githubusercontent.com/ollama/ollama/main/README.md" "ollama_readme.md" "ai"
download "koboldcpp" "https://raw.githubusercontent.com/LostRuins/koboldcpp/main/README.md" "koboldcpp_guide.md" "ai"
download "text_gen_webui" "https://raw.githubusercontent.com/oobabooga/text-generation-webui/main/README.md" "text_gen_webui.md" "ai"
download "transformers_readme" "https://raw.githubusercontent.com/huggingface/transformers/main/README.md" "transformers.md" "ai"
download "gpt4all" "https://raw.githubusercontent.com/nomic-ai/gpt4all/main/README.md" "gpt4all_readme.md" "ai"
download "localai" "https://raw.githubusercontent.com/mudler/LocalAI/master/README.md" "localai_guide.md" "ai"
download "llama_cpp" "https://raw.githubusercontent.com/ggerganov/llama.cpp/master/README.md" "llama_cpp.md" "ai"
download "stable_diffusion" "https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui/master/README.md" "stable_diffusion.md" "ai"
download "langchain" "https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md" "langchain_readme.md" "ai"
download "openai_cookbook" "https://raw.githubusercontent.com/openai/openai-cookbook/main/README.md" "openai_cookbook.md" "ai"
download "pytorch_readme" "https://raw.githubusercontent.com/pytorch/pytorch/main/README.md" "pytorch_readme.md" "ai"
download "tensorflow_readme" "https://raw.githubusercontent.com/tensorflow/tensorflow/master/README.md" "tensorflow_readme.md" "ai"
download "fastai" "https://raw.githubusercontent.com/fastai/fastai/master/README.md" "fastai_readme.md" "ai"
download "spacy" "https://raw.githubusercontent.com/explosion/spaCy/master/README.md" "spacy_readme.md" "ai"
download "gensim" "https://raw.githubusercontent.com/RaRe-Technologies/gensim/develop/README.md" "gensim_readme.md" "ai"
download "nltk_readme" "https://raw.githubusercontent.com/nltk/nltk/develop/README.md" "nltk_readme.md" "ai"
download "scikit_learn" "https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/README.rst" "scikit_learn.md" "ai"
download "keras_readme" "https://raw.githubusercontent.com/keras-team/keras/master/README.md" "keras_readme.md" "ai"
download "mlflow" "https://raw.githubusercontent.com/mlflow/mlflow/master/README.rst" "mlflow_readme.md" "ai"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 SECTION 3: Obsidian / PKM / Second Brain (41-60)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 41-60. PKM and note-taking resources
download "obsidian_help" "https://raw.githubusercontent.com/obsidianmd/obsidian-help/master/en/Home.md" "obsidian_help.md" "pkm"
download "foam_readme" "https://raw.githubusercontent.com/foambubble/foam/master/README.md" "foam_readme.md" "pkm"
download "dendron" "https://raw.githubusercontent.com/dendronhq/dendron/master/README.md" "dendron_readme.md" "pkm"
download "logseq" "https://raw.githubusercontent.com/logseq/logseq/master/README.md" "logseq_readme.md" "pkm"
download "roam_research_guide" "https://raw.githubusercontent.com/MatthieuBizien/roam-to-git/master/README.md" "roam_guide.md" "pkm"
download "zettelkasten_method" "https://raw.githubusercontent.com/Zettelkasten-Method/10000-markdown-files/master/README.md" "zettelkasten.md" "pkm"
download "dataview_plugin" "https://raw.githubusercontent.com/blacksmithgu/obsidian-dataview/master/README.md" "dataview.md" "pkm"
download "templater_plugin" "https://raw.githubusercontent.com/SilentVoid13/Templater/master/README.md" "templater.md" "pkm"
download "quickadd_plugin" "https://raw.githubusercontent.com/chhoumann/quickadd/master/README.md" "quickadd.md" "pkm"
download "periodic_notes" "https://raw.githubusercontent.com/liamcain/obsidian-periodic-notes/main/README.md" "periodic_notes.md" "pkm"
download "calendar_plugin" "https://raw.githubusercontent.com/liamcain/obsidian-calendar-plugin/main/README.md" "calendar.md" "pkm"
download "kanban_plugin" "https://raw.githubusercontent.com/mgmeyers/obsidian-kanban/main/README.md" "kanban.md" "pkm"
download "excalidraw_plugin" "https://raw.githubusercontent.com/zsviczian/obsidian-excalidraw-plugin/master/README.md" "excalidraw.md" "pkm"
download "daily_notes" "https://raw.githubusercontent.com/liamcain/obsidian-daily-notes-interface/main/README.md" "daily_notes.md" "pkm"
download "advanced_tables" "https://raw.githubusercontent.com/tgrosinger/advanced-tables-obsidian/main/README.md" "advanced_tables.md" "pkm"
download "mind_map" "https://raw.githubusercontent.com/lynchjames/obsidian-mind-map/master/README.md" "mind_map.md" "pkm"
download "sliding_panes" "https://raw.githubusercontent.com/deathau/sliding-panes-obsidian/master/README.md" "sliding_panes.md" "pkm"
download "local_graph" "https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json" "community_plugins.json" "pkm"
download "markdown_guide" "https://raw.githubusercontent.com/mattcone/markdown-guide/master/README.md" "markdown_guide.md" "pkm"
download "git_plugin" "https://raw.githubusercontent.com/denolehov/obsidian-git/master/README.md" "obsidian_git.md" "pkm"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 SECTION 4: Security / OpSec / Red Team (61-80)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 61-80. Security resources
download "payloads_all_things" "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/README.md" "payloads_all.md" "security"
download "redteam_opsec" "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Methodology%20and%20Resources/RedTeam%20-%20OpSec.md" "redteam_opsec.md" "security"
download "owasp_top10_readme" "https://raw.githubusercontent.com/OWASP/Top10/master/README.md" "owasp_top10.md" "security"
download "owasp_cheatsheet" "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/README.md" "owasp_cheatsheets.md" "security"
download "mitre_attack_readme" "https://raw.githubusercontent.com/mitre-attack/attack-website/master/README.md" "mitre_attack.md" "security"
download "atomic_redteam" "https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/README.md" "atomic_redteam.md" "security"
download "sigma_rules" "https://raw.githubusercontent.com/SigmaHQ/sigma/master/README.md" "sigma_rules.md" "security"
download "threathunting" "https://raw.githubusercontent.com/0x4D31/awesome-threat-detection/master/README.md" "threat_detection.md" "security"
download "pentesting_bible" "https://raw.githubusercontent.com/blaCCkHatHacEEkr/PENTESTING-BIBLE/master/README.md" "pentesting_bible.md" "security"
download "awesome_security" "https://raw.githubusercontent.com/sbilly/awesome-security/master/README.md" "awesome_security.md" "security"
download "awesome_hacking" "https://raw.githubusercontent.com/Hack-with-Github/Awesome-Hacking/master/README.md" "awesome_hacking.md" "security"
download "awesome_pentest" "https://raw.githubusercontent.com/enaqx/awesome-pentest/master/README.md" "awesome_pentest.md" "security"
download "hacktricks" "https://raw.githubusercontent.com/carlospolop/hacktricks/master/README.md" "hacktricks.md" "security"
download "linux_priv_esc" "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md" "linux_privesc.md" "security"
download "windows_priv_esc" "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md" "windows_privesc.md" "security"
download "web_shells" "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Methodology%20and%20Resources/Web%20Shell/README.md" "web_shells.md" "security"
download "reverse_shells" "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md" "reverse_shells.md" "security"
download "sql_injection" "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/README.md" "sql_injection.md" "security"
download "xss_payloads" "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XSS%20Injection/README.md" "xss_injection.md" "security"
download "aws_security" "https://raw.githubusercontent.com/toniblyx/my-arsenal-of-aws-security-tools/master/README.md" "aws_security.md" "security"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔮 SECTION 5: Esoteric / Mythic / Philosophy (81-100)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 81-100. Philosophy and classic texts from Gutenberg
download "kybalion" "https://www.gutenberg.org/files/70/70-0.txt" "kybalion.txt" "esoteric"
download "machiavelli_prince" "https://www.gutenberg.org/files/1232/1232-0.txt" "prince_machiavelli.txt" "esoteric"
download "sun_tzu" "https://www.gutenberg.org/files/132/132-0.txt" "art_of_war.txt" "esoteric"
download "plato_republic" "https://www.gutenberg.org/files/1497/1497-0.txt" "plato_republic.txt" "esoteric"
download "aristotle_ethics" "https://www.gutenberg.org/files/8438/8438-0.txt" "aristotle_ethics.txt" "esoteric"
download "marcus_aurelius" "https://www.gutenberg.org/files/2680/2680-0.txt" "meditations_aurelius.txt" "esoteric"
download "epictetus" "https://www.gutenberg.org/files/871/871-0.txt" "epictetus_enchiridion.txt" "esoteric"
download "seneca_letters" "https://www.gutenberg.org/files/3794/3794-0.txt" "seneca_letters.txt" "esoteric"
download "tao_te_ching" "https://www.gutenberg.org/files/216/216-0.txt" "tao_te_ching.txt" "esoteric"
download "confucius_analects" "https://www.gutenberg.org/files/4094/4094-0.txt" "confucius_analects.txt" "esoteric"
download "bhagavad_gita" "https://www.gutenberg.org/files/2388/2388-0.txt" "bhagavad_gita.txt" "esoteric"
download "upanishads" "https://www.gutenberg.org/files/3283/3283-0.txt" "upanishads.txt" "esoteric"
download "buddha_dhammapada" "https://www.gutenberg.org/files/2017/2017-0.txt" "dhammapada.txt" "esoteric"
download "nietzsche_zarathustra" "https://www.gutenberg.org/files/1998/1998-0.txt" "zarathustra.txt" "esoteric"
download "nietzsche_beyond_good" "https://www.gutenberg.org/files/4363/4363-0.txt" "beyond_good_evil.txt" "esoteric"
download "kant_critique" "https://www.gutenberg.org/files/4280/4280-0.txt" "kant_pure_reason.txt" "esoteric"
download "descartes_meditations" "https://www.gutenberg.org/files/59/59-0.txt" "descartes_meditations.txt" "esoteric"
download "spinoza_ethics" "https://www.gutenberg.org/files/3800/3800-0.txt" "spinoza_ethics.txt" "esoteric"
download "schopenhauer" "https://www.gutenberg.org/files/10732/10732-0.txt" "schopenhauer_wisdom.txt" "esoteric"
download "emerson_essays" "https://www.gutenberg.org/files/16643/16643-0.txt" "emerson_essays.txt" "esoteric"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 FINAL SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Total downloads attempted: $TOTAL"
echo "Successful: $SUCCESS"
echo "Failed: $FAILED"
if [ "$TOTAL" -gt 0 ]; then
  echo "Success rate: $(( SUCCESS * 100 / TOTAL ))%"
else
  echo "Success rate: N/A (no downloads attempted)"
fi
echo ""
echo "📁 Knowledge base location: $KNOWLEDGE_BASE_DIR/"
echo "   - Math: $KNOWLEDGE_BASE_DIR/math/"
echo "   - AI: $KNOWLEDGE_BASE_DIR/ai/"
echo "   - PKM: $KNOWLEDGE_BASE_DIR/pkm/"
echo "   - Security: $KNOWLEDGE_BASE_DIR/security/"
echo "   - Esoteric: $KNOWLEDGE_BASE_DIR/esoteric/"
echo ""
echo "💡 Next steps:"
echo "   1. Copy any .txt or .md files to your Obsidian vault"
echo "   2. Drop them in your Continue.dev knowledge base"
echo "   3. Feed them to your local LLM via RAG"
echo "   4. Use: curl -L -s <URL> | clip for quick context"
echo ""
echo "✨ Your AI heir now has access to centuries of knowledge!"
echo ""
