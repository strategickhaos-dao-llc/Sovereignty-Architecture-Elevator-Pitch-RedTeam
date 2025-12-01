"""
Visualization Integration - Unreal/Unity 3D Medical Visualization Bridge
=========================================================================

Bridges the Singularity Engine to game engines for:
- 3D protein structure visualization
- Interactive symptom mapping
- Molecular docking simulations
- Disease progression animations

Uses Unreal Engine and Unity (both free) for photorealistic
medical visualizations that help understand complex biology.
"""

import asyncio
import json
import random
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import struct

import structlog

logger = structlog.get_logger(__name__)


class VisualizationType(Enum):
    """Types of visualizations"""
    PROTEIN_3D = "protein_3d"
    MOLECULAR_DOCKING = "molecular_docking"
    SYMPTOM_MAP = "symptom_map"
    PATHWAY_DIAGRAM = "pathway_diagram"
    CELL_STRUCTURE = "cell_structure"
    ORGAN_SYSTEM = "organ_system"
    DRUG_INTERACTION = "drug_interaction"
    DISEASE_PROGRESSION = "disease_progression"


class RenderEngine(Enum):
    """Supported render engines"""
    UNREAL = "unreal"
    UNITY = "unity"
    BLENDER = "blender"
    WEB_GL = "webgl"


class FileFormat(Enum):
    """Output file formats"""
    FBX = "fbx"
    GLTF = "gltf"
    USD = "usd"
    OBJ = "obj"
    PDB = "pdb"
    MOL2 = "mol2"


@dataclass
class Vector3:
    """3D vector"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]
    
    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}


@dataclass
class Color:
    """RGBA color"""
    r: float = 1.0
    g: float = 1.0
    b: float = 1.0
    a: float = 1.0
    
    def to_list(self) -> List[float]:
        return [self.r, self.g, self.b, self.a]
    
    def to_hex(self) -> str:
        return "#{:02x}{:02x}{:02x}".format(
            int(self.r * 255),
            int(self.g * 255),
            int(self.b * 255)
        )


@dataclass
class Atom:
    """Represents an atom in a molecule"""
    atom_id: int
    element: str
    position: Vector3
    
    # Properties
    radius: float = 1.5
    color: Color = field(default_factory=lambda: Color(0.7, 0.7, 0.7, 1.0))
    charge: float = 0.0
    
    # Bonding
    bonds: List[int] = field(default_factory=list)
    
    # Metadata
    residue_name: str = ""
    chain_id: str = ""
    residue_seq: int = 0


@dataclass
class Bond:
    """Represents a chemical bond"""
    atom1_id: int
    atom2_id: int
    bond_type: str = "single"  # single, double, triple, aromatic
    bond_order: int = 1


@dataclass
class Protein3DModel:
    """3D protein structure model"""
    model_id: str
    name: str
    
    # Structure
    atoms: List[Atom] = field(default_factory=list)
    bonds: List[Bond] = field(default_factory=list)
    
    # Metadata
    pdb_id: Optional[str] = None
    uniprot_id: Optional[str] = None
    sequence: str = ""
    
    # Secondary structure
    helices: List[Dict] = field(default_factory=list)
    sheets: List[Dict] = field(default_factory=list)
    
    # Active sites
    active_sites: List[Dict] = field(default_factory=list)
    binding_sites: List[Dict] = field(default_factory=list)
    
    # Rendering info
    center: Vector3 = field(default_factory=Vector3)
    bounding_box: Tuple[Vector3, Vector3] = field(default_factory=lambda: (Vector3(), Vector3()))
    
    # File paths
    source_file: str = ""
    exported_files: Dict[str, str] = field(default_factory=dict)
    
    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def calculate_center(self):
        """Calculate center of mass"""
        if not self.atoms:
            return
        
        total_x = sum(a.position.x for a in self.atoms)
        total_y = sum(a.position.y for a in self.atoms)
        total_z = sum(a.position.z for a in self.atoms)
        n = len(self.atoms)
        
        self.center = Vector3(total_x / n, total_y / n, total_z / n)
    
    def calculate_bounding_box(self):
        """Calculate bounding box"""
        if not self.atoms:
            return
        
        min_pos = Vector3(
            min(a.position.x for a in self.atoms),
            min(a.position.y for a in self.atoms),
            min(a.position.z for a in self.atoms)
        )
        max_pos = Vector3(
            max(a.position.x for a in self.atoms),
            max(a.position.y for a in self.atoms),
            max(a.position.z for a in self.atoms)
        )
        
        self.bounding_box = (min_pos, max_pos)


@dataclass
class SymptomNode:
    """A node in the symptom map"""
    node_id: str
    name: str
    
    # Position in body map
    body_region: str  # head, torso, limbs, etc.
    position: Vector3 = field(default_factory=Vector3)
    
    # Symptom info
    severity: float = 0.0  # 0-1
    frequency: float = 0.0  # 0-1 (how often it occurs)
    
    # Connections
    related_symptoms: List[str] = field(default_factory=list)
    affected_systems: List[str] = field(default_factory=list)
    
    # Visualization
    color: Color = field(default_factory=lambda: Color(1.0, 0.5, 0.0, 1.0))
    size: float = 1.0
    
    # Metadata
    description: str = ""
    notes: List[str] = field(default_factory=list)


@dataclass
class SymptomMap:
    """Interactive symptom map visualization"""
    map_id: str
    disease_name: str
    
    # Symptoms
    symptoms: Dict[str, SymptomNode] = field(default_factory=dict)
    
    # Connections
    symptom_connections: List[Tuple[str, str, float]] = field(default_factory=list)
    
    # Body regions affected
    affected_regions: Dict[str, float] = field(default_factory=dict)  # region -> severity
    
    # Timeline (if tracking progression)
    progression_stages: List[Dict] = field(default_factory=list)
    
    # Metadata
    patient_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def add_symptom(self, symptom: SymptomNode):
        """Add a symptom to the map"""
        self.symptoms[symptom.node_id] = symptom
        
        # Update affected regions
        if symptom.body_region:
            current = self.affected_regions.get(symptom.body_region, 0.0)
            self.affected_regions[symptom.body_region] = max(current, symptom.severity)
        
        self.updated_at = datetime.now(timezone.utc)
    
    def connect_symptoms(self, symptom1_id: str, symptom2_id: str, strength: float = 1.0):
        """Connect two symptoms"""
        if symptom1_id in self.symptoms and symptom2_id in self.symptoms:
            self.symptom_connections.append((symptom1_id, symptom2_id, strength))
            
            # Update related symptoms in nodes
            self.symptoms[symptom1_id].related_symptoms.append(symptom2_id)
            self.symptoms[symptom2_id].related_symptoms.append(symptom1_id)


@dataclass
class VisualizationScene:
    """A complete visualization scene"""
    scene_id: str
    name: str
    visualization_type: VisualizationType
    
    # Content
    proteins: List[Protein3DModel] = field(default_factory=list)
    symptom_maps: List[SymptomMap] = field(default_factory=list)
    
    # Camera
    camera_position: Vector3 = field(default_factory=lambda: Vector3(0, 0, 100))
    camera_target: Vector3 = field(default_factory=Vector3)
    camera_fov: float = 60.0
    
    # Lighting
    lighting_preset: str = "studio"  # studio, outdoor, dramatic
    ambient_color: Color = field(default_factory=lambda: Color(0.2, 0.2, 0.2, 1.0))
    
    # Animation
    is_animated: bool = False
    animation_duration: float = 0.0  # seconds
    keyframes: List[Dict] = field(default_factory=list)
    
    # Export
    render_engine: RenderEngine = RenderEngine.WEB_GL
    output_format: FileFormat = FileFormat.GLTF
    output_path: str = ""
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class VisualizationBridge:
    """
    Bridge to game engines for medical visualization.
    
    This connects the Singularity Engine to Unreal Engine and Unity
    for creating:
    
    1. 3D protein structure visualizations
    2. Interactive symptom maps
    3. Drug-protein docking animations
    4. Disease progression timelines
    
    All using FREE game engines for photorealistic quality.
    """
    
    # Element colors for molecular visualization
    ELEMENT_COLORS = {
        "H": Color(1.0, 1.0, 1.0),      # White
        "C": Color(0.2, 0.2, 0.2),      # Dark gray
        "N": Color(0.0, 0.0, 1.0),      # Blue
        "O": Color(1.0, 0.0, 0.0),      # Red
        "S": Color(1.0, 1.0, 0.0),      # Yellow
        "P": Color(1.0, 0.5, 0.0),      # Orange
        "Fe": Color(0.5, 0.3, 0.0),     # Brown
        "Ca": Color(0.0, 1.0, 0.0),     # Green
        "Zn": Color(0.5, 0.5, 0.5),     # Gray
    }
    
    # Element radii (in Angstroms)
    ELEMENT_RADII = {
        "H": 1.2,
        "C": 1.7,
        "N": 1.55,
        "O": 1.52,
        "S": 1.8,
        "P": 1.8,
        "Fe": 1.5,
        "Ca": 1.97,
        "Zn": 1.39,
    }
    
    def __init__(
        self,
        output_dir: str = "/var/refinory/visualizations",
        default_engine: RenderEngine = RenderEngine.WEB_GL
    ):
        self.output_dir = Path(output_dir)
        self.default_engine = default_engine
        
        # Scenes
        self.scenes: Dict[str, VisualizationScene] = {}
        
        # Cached models
        self.protein_cache: Dict[str, Protein3DModel] = {}
        self.symptom_map_cache: Dict[str, SymptomMap] = {}
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(
            "VisualizationBridge initialized",
            output_dir=str(output_dir),
            default_engine=default_engine.value
        )
    
    async def create_protein_visualization(
        self,
        pdb_data: str,
        name: Optional[str] = None
    ) -> Protein3DModel:
        """Create a 3D protein visualization from PDB data"""
        model_id = f"protein_{uuid.uuid4().hex[:8]}"
        
        # Parse PDB data
        atoms, bonds = self._parse_pdb(pdb_data)
        
        model = Protein3DModel(
            model_id=model_id,
            name=name or f"Protein_{model_id}",
            atoms=atoms,
            bonds=bonds
        )
        
        # Calculate geometry
        model.calculate_center()
        model.calculate_bounding_box()
        
        # Color atoms by element
        for atom in model.atoms:
            atom.color = self.ELEMENT_COLORS.get(atom.element, Color(0.7, 0.7, 0.7))
            atom.radius = self.ELEMENT_RADII.get(atom.element, 1.5)
        
        # Cache the model
        self.protein_cache[model_id] = model
        
        logger.info(
            f"Created protein visualization {model_id}",
            atoms=len(atoms),
            bonds=len(bonds)
        )
        
        return model
    
    def _parse_pdb(self, pdb_data: str) -> Tuple[List[Atom], List[Bond]]:
        """Parse PDB format data"""
        atoms = []
        bonds = []
        atom_id_map = {}
        
        for line in pdb_data.split("\n"):
            # Parse ATOM records
            if line.startswith("ATOM") or line.startswith("HETATM"):
                try:
                    atom_id = int(line[6:11].strip())
                    element = line[76:78].strip() or line[12:14].strip()
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    residue_name = line[17:20].strip()
                    chain_id = line[21].strip()
                    residue_seq = int(line[22:26].strip())
                    
                    atom = Atom(
                        atom_id=atom_id,
                        element=element,
                        position=Vector3(x, y, z),
                        residue_name=residue_name,
                        chain_id=chain_id,
                        residue_seq=residue_seq
                    )
                    atoms.append(atom)
                    atom_id_map[atom_id] = len(atoms) - 1
                except (ValueError, IndexError):
                    continue
            
            # Parse CONECT records for bonds
            elif line.startswith("CONECT"):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        atom1 = int(parts[1])
                        for i in range(2, len(parts)):
                            atom2 = int(parts[i])
                            if atom1 in atom_id_map and atom2 in atom_id_map:
                                bond = Bond(atom1_id=atom1, atom2_id=atom2)
                                bonds.append(bond)
                    except ValueError:
                        continue
        
        # If no CONECT records, infer bonds from distances
        if not bonds:
            bonds = self._infer_bonds(atoms)
        
        return atoms, bonds
    
    def _infer_bonds(self, atoms: List[Atom], max_distance: float = 2.0) -> List[Bond]:
        """Infer bonds based on atomic distances"""
        bonds = []
        
        for i, atom1 in enumerate(atoms):
            for j, atom2 in enumerate(atoms[i+1:], i+1):
                # Calculate distance
                dx = atom1.position.x - atom2.position.x
                dy = atom1.position.y - atom2.position.y
                dz = atom1.position.z - atom2.position.z
                distance = (dx**2 + dy**2 + dz**2) ** 0.5
                
                # Check if within bonding distance
                if distance <= max_distance:
                    bond = Bond(atom1_id=atom1.atom_id, atom2_id=atom2.atom_id)
                    bonds.append(bond)
        
        return bonds
    
    async def create_symptom_map(
        self,
        disease_name: str,
        symptoms: List[Dict[str, Any]]
    ) -> SymptomMap:
        """Create an interactive symptom map"""
        map_id = f"symptom_map_{uuid.uuid4().hex[:8]}"
        
        symptom_map = SymptomMap(
            map_id=map_id,
            disease_name=disease_name
        )
        
        # Body region positions (normalized coordinates)
        body_positions = {
            "head": Vector3(0, 1.7, 0),
            "neck": Vector3(0, 1.5, 0),
            "chest": Vector3(0, 1.2, 0),
            "abdomen": Vector3(0, 0.9, 0),
            "pelvis": Vector3(0, 0.6, 0),
            "left_arm": Vector3(-0.4, 1.2, 0),
            "right_arm": Vector3(0.4, 1.2, 0),
            "left_leg": Vector3(-0.15, 0.3, 0),
            "right_leg": Vector3(0.15, 0.3, 0),
            "spine": Vector3(0, 1.0, -0.1),
        }
        
        # Add symptoms
        for symptom_data in symptoms:
            region = symptom_data.get("body_region", "chest")
            base_pos = body_positions.get(region, Vector3(0, 1.0, 0))
            
            # Add some random offset for visual separation
            offset = Vector3(
                random.uniform(-0.1, 0.1),
                random.uniform(-0.1, 0.1),
                random.uniform(-0.05, 0.05)
            )
            
            # Determine color based on severity
            severity = symptom_data.get("severity", 0.5)
            color = Color(
                r=min(1.0, 0.3 + severity * 0.7),
                g=max(0.0, 0.7 - severity * 0.7),
                b=0.0,
                a=0.8
            )
            
            symptom = SymptomNode(
                node_id=symptom_data.get("id", f"symptom_{uuid.uuid4().hex[:6]}"),
                name=symptom_data.get("name", "Unknown Symptom"),
                body_region=region,
                position=Vector3(
                    base_pos.x + offset.x,
                    base_pos.y + offset.y,
                    base_pos.z + offset.z
                ),
                severity=severity,
                frequency=symptom_data.get("frequency", 0.5),
                color=color,
                size=0.5 + severity * 0.5,
                description=symptom_data.get("description", ""),
                affected_systems=symptom_data.get("affected_systems", [])
            )
            
            symptom_map.add_symptom(symptom)
        
        # Auto-connect related symptoms
        await self._connect_related_symptoms(symptom_map)
        
        # Cache the map
        self.symptom_map_cache[map_id] = symptom_map
        
        logger.info(
            f"Created symptom map {map_id}",
            symptoms=len(symptom_map.symptoms),
            connections=len(symptom_map.symptom_connections)
        )
        
        return symptom_map
    
    async def _connect_related_symptoms(self, symptom_map: SymptomMap):
        """Automatically connect related symptoms"""
        symptoms = list(symptom_map.symptoms.values())
        
        for i, symptom1 in enumerate(symptoms):
            for symptom2 in symptoms[i+1:]:
                # Connect if same body region
                if symptom1.body_region == symptom2.body_region:
                    symptom_map.connect_symptoms(
                        symptom1.node_id,
                        symptom2.node_id,
                        strength=0.8
                    )
                
                # Connect if shared affected systems
                shared_systems = set(symptom1.affected_systems) & set(symptom2.affected_systems)
                if shared_systems:
                    symptom_map.connect_symptoms(
                        symptom1.node_id,
                        symptom2.node_id,
                        strength=len(shared_systems) * 0.3
                    )
    
    async def create_scene(
        self,
        name: str,
        visualization_type: VisualizationType,
        **kwargs
    ) -> VisualizationScene:
        """Create a complete visualization scene"""
        scene_id = f"scene_{uuid.uuid4().hex[:8]}"
        
        scene = VisualizationScene(
            scene_id=scene_id,
            name=name,
            visualization_type=visualization_type,
            render_engine=kwargs.get("render_engine", self.default_engine),
            output_format=kwargs.get("output_format", FileFormat.GLTF)
        )
        
        # Add proteins if provided
        if "proteins" in kwargs:
            scene.proteins = kwargs["proteins"]
        
        # Add symptom maps if provided
        if "symptom_maps" in kwargs:
            scene.symptom_maps = kwargs["symptom_maps"]
        
        # Auto-configure camera
        await self._configure_camera(scene)
        
        # Store scene
        self.scenes[scene_id] = scene
        
        logger.info(f"Created visualization scene {scene_id}")
        
        return scene
    
    async def _configure_camera(self, scene: VisualizationScene):
        """Automatically configure camera for scene"""
        # Calculate scene bounds
        min_pos = Vector3(float('inf'), float('inf'), float('inf'))
        max_pos = Vector3(float('-inf'), float('-inf'), float('-inf'))
        
        for protein in scene.proteins:
            bb_min, bb_max = protein.bounding_box
            min_pos = Vector3(
                min(min_pos.x, bb_min.x),
                min(min_pos.y, bb_min.y),
                min(min_pos.z, bb_min.z)
            )
            max_pos = Vector3(
                max(max_pos.x, bb_max.x),
                max(max_pos.y, bb_max.y),
                max(max_pos.z, bb_max.z)
            )
        
        # Calculate center and distance
        if min_pos.x != float('inf'):
            center = Vector3(
                (min_pos.x + max_pos.x) / 2,
                (min_pos.y + max_pos.y) / 2,
                (min_pos.z + max_pos.z) / 2
            )
            
            # Calculate camera distance
            dx = max_pos.x - min_pos.x
            dy = max_pos.y - min_pos.y
            dz = max_pos.z - min_pos.z
            size = max(dx, dy, dz)
            distance = size * 2.5
            
            scene.camera_target = center
            scene.camera_position = Vector3(center.x, center.y, center.z + distance)
    
    async def export_scene(
        self,
        scene_id: str,
        output_format: Optional[FileFormat] = None
    ) -> str:
        """Export scene to file"""
        if scene_id not in self.scenes:
            raise ValueError(f"Scene {scene_id} not found")
        
        scene = self.scenes[scene_id]
        format_ = output_format or scene.output_format
        
        # Create output path
        output_path = self.output_dir / f"{scene.name}_{scene_id}.{format_.value}"
        
        # Export based on format
        if format_ == FileFormat.GLTF:
            await self._export_gltf(scene, output_path)
        elif format_ == FileFormat.FBX:
            await self._export_fbx(scene, output_path)
        elif format_ == FileFormat.USD:
            await self._export_usd(scene, output_path)
        else:
            await self._export_json(scene, output_path)
        
        scene.output_path = str(output_path)
        
        logger.info(f"Exported scene {scene_id} to {output_path}")
        
        return str(output_path)
    
    async def _export_gltf(self, scene: VisualizationScene, output_path: Path):
        """Export scene to glTF format"""
        # Create glTF structure
        gltf = {
            "asset": {
                "version": "2.0",
                "generator": "Singularity Engine Visualization Bridge"
            },
            "scene": 0,
            "scenes": [{"nodes": []}],
            "nodes": [],
            "meshes": [],
            "materials": [],
            "accessors": [],
            "bufferViews": [],
            "buffers": []
        }
        
        # Add proteins as nodes
        node_index = 0
        for protein in scene.proteins:
            gltf["scenes"][0]["nodes"].append(node_index)
            gltf["nodes"].append({
                "name": protein.name,
                "translation": [protein.center.x, protein.center.y, protein.center.z],
                "extras": {
                    "pdb_id": protein.pdb_id,
                    "atom_count": len(protein.atoms)
                }
            })
            node_index += 1
        
        # Add symptom maps
        for symptom_map in scene.symptom_maps:
            gltf["scenes"][0]["nodes"].append(node_index)
            gltf["nodes"].append({
                "name": f"SymptomMap_{symptom_map.disease_name}",
                "extras": {
                    "symptom_count": len(symptom_map.symptoms),
                    "affected_regions": list(symptom_map.affected_regions.keys())
                }
            })
            node_index += 1
        
        # Write file
        with open(output_path, "w") as f:
            json.dump(gltf, f, indent=2)
    
    async def _export_fbx(self, scene: VisualizationScene, output_path: Path):
        """Export scene to FBX format (placeholder)"""
        # FBX export would require fbx-python or similar
        # For now, create a metadata file
        metadata = {
            "format": "fbx_placeholder",
            "scene_id": scene.scene_id,
            "proteins": len(scene.proteins),
            "symptom_maps": len(scene.symptom_maps)
        }
        with open(output_path.with_suffix(".json"), "w") as f:
            json.dump(metadata, f, indent=2)
    
    async def _export_usd(self, scene: VisualizationScene, output_path: Path):
        """Export scene to USD format (placeholder)"""
        # USD export would require pxr (OpenUSD)
        metadata = {
            "format": "usd_placeholder",
            "scene_id": scene.scene_id,
            "proteins": len(scene.proteins),
            "symptom_maps": len(scene.symptom_maps)
        }
        with open(output_path.with_suffix(".json"), "w") as f:
            json.dump(metadata, f, indent=2)
    
    async def _export_json(self, scene: VisualizationScene, output_path: Path):
        """Export scene to JSON format"""
        export_data = {
            "scene_id": scene.scene_id,
            "name": scene.name,
            "visualization_type": scene.visualization_type.value,
            "camera": {
                "position": scene.camera_position.to_dict(),
                "target": scene.camera_target.to_dict(),
                "fov": scene.camera_fov
            },
            "lighting": {
                "preset": scene.lighting_preset,
                "ambient": scene.ambient_color.to_list()
            },
            "proteins": [
                {
                    "model_id": p.model_id,
                    "name": p.name,
                    "pdb_id": p.pdb_id,
                    "atom_count": len(p.atoms),
                    "center": p.center.to_dict()
                }
                for p in scene.proteins
            ],
            "symptom_maps": [
                {
                    "map_id": m.map_id,
                    "disease_name": m.disease_name,
                    "symptom_count": len(m.symptoms),
                    "affected_regions": m.affected_regions
                }
                for m in scene.symptom_maps
            ]
        }
        
        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)
    
    async def generate_unreal_blueprint(self, scene_id: str) -> str:
        """Generate Unreal Engine blueprint for scene"""
        if scene_id not in self.scenes:
            raise ValueError(f"Scene {scene_id} not found")
        
        scene = self.scenes[scene_id]
        
        # Generate blueprint pseudocode (would be actual UE blueprint in production)
        blueprint = f"""
// Unreal Engine 5 Blueprint for {scene.name}
// Auto-generated by Singularity Engine

Begin Object Class=/Script/BlueprintGraph.K2Node_CustomEvent Name="Initialize_{scene.scene_id}"
   EventReference=(MemberName="Initialize",MemberGuid=...)
   EventSignatureClass=None
   bOverrideFunction=True
End Object

// Camera Setup
CameraComponent.SetRelativeLocation({scene.camera_position.to_list()})
CameraComponent.SetRelativeRotation(LookAt({scene.camera_target.to_list()}))
CameraComponent.FieldOfView = {scene.camera_fov}

// Load Proteins
{chr(10).join([f'// Load Protein: {p.name} (PDB: {p.pdb_id})' for p in scene.proteins])}

// Load Symptom Maps
{chr(10).join([f'// Load Symptom Map: {m.disease_name}' for m in scene.symptom_maps])}

// Lighting
SetLightingPreset("{scene.lighting_preset}")
SetAmbientLight({scene.ambient_color.to_list()})
"""
        
        # Save blueprint
        blueprint_path = self.output_dir / f"{scene.name}_blueprint.txt"
        with open(blueprint_path, "w") as f:
            f.write(blueprint)
        
        return str(blueprint_path)
    
    async def generate_unity_script(self, scene_id: str) -> str:
        """Generate Unity C# script for scene"""
        if scene_id not in self.scenes:
            raise ValueError(f"Scene {scene_id} not found")
        
        scene = self.scenes[scene_id]
        
        # Generate C# script
        script = f"""
using UnityEngine;

// Auto-generated by Singularity Engine
public class {scene.name.replace(' ', '')}Scene : MonoBehaviour
{{
    public Camera mainCamera;
    
    void Start()
    {{
        // Camera Setup
        mainCamera.transform.position = new Vector3({scene.camera_position.x}f, {scene.camera_position.y}f, {scene.camera_position.z}f);
        mainCamera.transform.LookAt(new Vector3({scene.camera_target.x}f, {scene.camera_target.y}f, {scene.camera_target.z}f));
        mainCamera.fieldOfView = {scene.camera_fov}f;
        
        // Load proteins
        LoadProteins();
        
        // Load symptom maps
        LoadSymptomMaps();
    }}
    
    void LoadProteins()
    {{
        // {len(scene.proteins)} proteins to load
        {chr(10).join([f'        // Load {p.name} (PDB: {p.pdb_id})' for p in scene.proteins])}
    }}
    
    void LoadSymptomMaps()
    {{
        // {len(scene.symptom_maps)} symptom maps to load
        {chr(10).join([f'        // Load {m.disease_name} map' for m in scene.symptom_maps])}
    }}
}}
"""
        
        # Save script
        script_path = self.output_dir / f"{scene.name.replace(' ', '')}Scene.cs"
        with open(script_path, "w") as f:
            f.write(script)
        
        return str(script_path)
    
    async def get_visualization_stats(self) -> Dict[str, Any]:
        """Get visualization statistics"""
        return {
            "total_scenes": len(self.scenes),
            "cached_proteins": len(self.protein_cache),
            "cached_symptom_maps": len(self.symptom_map_cache),
            "output_directory": str(self.output_dir),
            "default_engine": self.default_engine.value,
            "scenes_by_type": {
                vt.value: len([s for s in self.scenes.values() if s.visualization_type == vt])
                for vt in VisualizationType
            }
        }
