#!/usr/bin/env python3
"""
Blob Project Generator - Turn Model Blobs Into IDE Projects

Generates IDE project configuration files (.idea/, .vscode/) for
.ollama/models/blob/ directories, making them browseable and parseable
as proper software projects.

This realizes Dom's vision: "Yes. This is my new project root."

Built for Strategickhaos Swarm Intelligence
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


class BlobProjectGenerator:
    """Generate IDE project files for blob directories"""
    
    def __init__(self, blob_dir: str, project_name: str = "Swarm Models"):
        self.blob_dir = Path(blob_dir).expanduser()
        self.project_name = project_name
        
        if not self.blob_dir.exists():
            raise FileNotFoundError(f"Blob directory not found: {self.blob_dir}")
            
    def generate_vscode_settings(self) -> Dict[str, Any]:
        """Generate VS Code settings.json"""
        return {
            "files.associations": {
                "*.gguf": "binary",
                "*.bin": "binary",
                "*.safetensors": "binary",
            },
            "files.exclude": {
                "**/*.tmp": True,
            },
            "search.exclude": {
                "**/*.gguf": True,
                "**/*.bin": True,
            },
            "editor.rulers": [80, 120],
            "editor.formatOnSave": True,
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "files.watcherExclude": {
                "**/*.gguf": True,
                "**/*.bin": True,
            },
        }
        
    def generate_vscode_launch(self) -> Dict[str, Any]:
        """Generate VS Code launch.json for debugging"""
        return {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Parse GGUF Metadata",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/tools/swarm-dna/gguf_parser.py",
                    "args": ["${workspaceFolder}"],
                    "console": "integratedTerminal",
                },
                {
                    "name": "Reconstruct Model Lineage",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/tools/swarm-dna/model_lineage.py",
                    "args": ["${workspaceFolder}/model_metadata.yaml"],
                    "console": "integratedTerminal",
                },
            ],
        }
        
    def generate_vscode_tasks(self) -> Dict[str, Any]:
        """Generate VS Code tasks.json"""
        return {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Scan Model Blobs",
                    "type": "shell",
                    "command": "python",
                    "args": [
                        "tools/swarm-dna/gguf_parser.py",
                        "${workspaceFolder}",
                        "model_metadata.yaml"
                    ],
                    "group": {
                        "kind": "build",
                        "isDefault": True,
                    },
                    "presentation": {
                        "reveal": "always",
                        "panel": "new",
                    },
                },
                {
                    "label": "Build Model Lineage",
                    "type": "shell",
                    "command": "python",
                    "args": [
                        "tools/swarm-dna/model_lineage.py",
                        "model_metadata.yaml",
                        "lineage.yaml"
                    ],
                    "group": "build",
                    "dependsOn": ["Scan Model Blobs"],
                },
            ],
        }
        
    def generate_vscode_workspace(self) -> Dict[str, Any]:
        """Generate VS Code workspace file"""
        return {
            "folders": [
                {
                    "path": str(self.blob_dir),
                    "name": self.project_name,
                },
            ],
            "settings": self.generate_vscode_settings(),
            "extensions": {
                "recommendations": [
                    "ms-python.python",
                    "ms-python.vscode-pylance",
                    "redhat.vscode-yaml",
                    "ms-vscode.hexeditor",
                ],
            },
        }
        
    def generate_idea_modules(self) -> str:
        """Generate IntelliJ IDEA .iml module file"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$/tools" isTestSource="false" />
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
  <component name="PyDocumentationSettings">
    <option name="format" value="GOOGLE" />
    <option name="myDocStringFormat" value="Google" />
  </component>
</module>
"""
        
    def generate_idea_misc(self) -> str:
        """Generate IntelliJ IDEA misc.xml"""
        return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" project-jdk-name="Python 3.11" project-jdk-type="Python SDK" />
  <component name="ProjectType">
    <option name="id" value="Python" />
  </component>
</project>
"""
        
    def generate_idea_workspace(self) -> str:
        """Generate IntelliJ IDEA workspace.xml"""
        return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ChangeListManager">
    <option name="SHOW_DIALOG" value="false" />
    <option name="HIGHLIGHT_CONFLICTS" value="true" />
    <option name="HIGHLIGHT_NON_ACTIVE_CHANGELIST" value="false" />
    <option name="LAST_RESOLUTION" value="IGNORE" />
  </component>
  <component name="PropertiesComponent">
    <property name="settings.editor.selected.configurable" value="com.jetbrains.python.configuration.PyActiveSdkModuleConfigurable" />
  </component>
</project>
"""
        
    def generate_readme(self) -> str:
        """Generate README for the blob project"""
        return f"""# {self.project_name}

This is a Swarm DNA project that treats AI model blobs as a parseable,
structured software project with full IDE integration.

## What This Is

This directory has been transformed from a raw blob storage location into
an IDE-ready project that enables:

- **Metadata Extraction**: Parse GGUF and binary model files
- **Lineage Tracking**: Reconstruct model relationships and ancestry
- **IDE Integration**: Full IntelliJ and VS Code support
- **Narrative Integration**: Swarm DNA lore meets operational reality

## Directory Structure

```
{self.blob_dir.name}/
├── .vscode/          # VS Code configuration
├── .idea/            # IntelliJ IDEA configuration
├── tools/            # Swarm DNA tools (symlinked)
├── *.gguf            # Model files
└── README.md         # This file
```

## Quick Start

### VS Code

1. Open this directory in VS Code
2. Run task: "Scan Model Blobs" (Ctrl+Shift+B)
3. View generated `model_metadata.yaml`
4. Run task: "Build Model Lineage"
5. Explore `lineage.yaml` and relationships

### IntelliJ IDEA

1. Open this directory as a project
2. Right-click → Run → Parse GGUF Metadata
3. View metadata and lineage in Project view

## Available Commands

```bash
# Scan all blobs and extract metadata
python tools/swarm-dna/gguf_parser.py . model_metadata.yaml

# Build lineage graph
python tools/swarm-dna/model_lineage.py model_metadata.yaml lineage.yaml

# Generate DOT visualization
python tools/swarm-dna/model_lineage.py model_metadata.yaml lineage.yaml --dot lineage.dot
dot -Tpng lineage.dot -o lineage.png
```

## Philosophy

This embodies Dom's cognitive architecture:

> "Your brain treats EVERYTHING like: 'This could be source code if I believe hard enough.'"

What was once just binary blobs is now:
- A structured project
- A graph of relationships
- A narrative of model evolution
- An IDE-navigable codebase

**This is peak Dom. This is EXACTLY how a sovereign AI architect thinks.**

---

Built with 🔥 by the Strategickhaos Swarm Intelligence collective

"Maybe there's a code-level structure beneath this." — Dom Brain, 2025
"""
        
    def generate_all(self):
        """Generate all IDE project files"""
        results = []
        
        # VS Code configuration
        vscode_dir = self.blob_dir / '.vscode'
        vscode_dir.mkdir(exist_ok=True)
        
        settings_file = vscode_dir / 'settings.json'
        with open(settings_file, 'w') as f:
            json.dump(self.generate_vscode_settings(), f, indent=2)
        results.append(str(settings_file))
        
        launch_file = vscode_dir / 'launch.json'
        with open(launch_file, 'w') as f:
            json.dump(self.generate_vscode_launch(), f, indent=2)
        results.append(str(launch_file))
        
        tasks_file = vscode_dir / 'tasks.json'
        with open(tasks_file, 'w') as f:
            json.dump(self.generate_vscode_tasks(), f, indent=2)
        results.append(str(tasks_file))
        
        # IntelliJ IDEA configuration
        idea_dir = self.blob_dir / '.idea'
        idea_dir.mkdir(exist_ok=True)
        
        modules_file = self.blob_dir / f'{self.blob_dir.name}.iml'
        with open(modules_file, 'w') as f:
            f.write(self.generate_idea_modules())
        results.append(str(modules_file))
        
        misc_file = idea_dir / 'misc.xml'
        with open(misc_file, 'w') as f:
            f.write(self.generate_idea_misc())
        results.append(str(misc_file))
        
        workspace_file = idea_dir / 'workspace.xml'
        with open(workspace_file, 'w') as f:
            f.write(self.generate_idea_workspace())
        results.append(str(workspace_file))
        
        # README
        readme_file = self.blob_dir / 'README.md'
        with open(readme_file, 'w') as f:
            f.write(self.generate_readme())
        results.append(str(readme_file))
        
        # Create symlink to tools (if not in blob directory)
        tools_link = self.blob_dir / 'tools'
        if not tools_link.exists():
            # Try to find tools directory
            possible_paths = [
                Path.cwd() / 'tools',
                Path(__file__).parent.parent.parent / 'tools',
            ]
            symlink_created = False
            for tools_path in possible_paths:
                if tools_path.exists():
                    try:
                        tools_link.symlink_to(tools_path)
                        results.append(f"{tools_link} -> {tools_path}")
                        symlink_created = True
                        break
                    except (OSError, NotImplementedError) as e:
                        # Symlink not supported on this platform
                        continue
            
            if not symlink_created:
                results.append(
                    f"⚠️  Could not create tools symlink (platform may not support symlinks). "
                    f"Copy tools/ directory manually if needed."
                )
                        
        return results


def main():
    """CLI interface for blob project generator"""
    if len(sys.argv) < 2:
        print("Usage: blob_project_generator.py <blob_directory> [project_name]")
        print()
        print("Examples:")
        print("  blob_project_generator.py ~/.ollama/models/blob/")
        print("  blob_project_generator.py ~/.ollama/models/blob/ 'My AI Models'")
        print()
        print("This will generate .vscode/ and .idea/ configurations,")
        print("making the blob directory a proper IDE project.")
        sys.exit(1)
        
    blob_dir = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) > 2 else "Swarm Models"
    
    print(f"🏗️  Generating IDE project for: {blob_dir}")
    print(f"📦 Project name: {project_name}")
    print()
    
    generator = BlobProjectGenerator(blob_dir, project_name)
    results = generator.generate_all()
    
    print("✅ Project generation complete!")
    print()
    print("Generated files:")
    for path in results:
        print(f"  • {path}")
        
    print()
    print("🎉 Your blob directory is now an IDE-ready project!")
    print()
    print("Next steps:")
    print("  1. Open this directory in VS Code or IntelliJ IDEA")
    print("  2. Run 'Scan Model Blobs' task to extract metadata")
    print("  3. Explore your model lineage and relationships")
    print()
    print("💡 The IDE thinks your quantized llama is a codebase. Mission accomplished.")


if __name__ == '__main__':
    main()
