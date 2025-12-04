// Package v1 contains API Schema definitions for the swarm v1 API group
// +kubebuilder:object:generate=true
// +groupName=swarm.strategickhaos.ai
package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
)

// RedBloodCellsSpec defines the transport layer configuration
type RedBloodCellsSpec struct {
	// Transport type (e.g., redis)
	// +kubebuilder:validation:Enum=redis;kafka;nats
	// +kubebuilder:default=redis
	Transport string `json:"transport,omitempty"`

	// Number of replicas
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:default=3
	Replicas int32 `json:"replicas,omitempty"`
}

// WhiteBloodCellsSpec defines the security scanner configuration
type WhiteBloodCellsSpec struct {
	// Scanner type (e.g., falco, trivy)
	// +kubebuilder:validation:Enum=falco;trivy
	// +kubebuilder:default=falco
	Scanner string `json:"scanner,omitempty"`

	// Response time for threat detection
	// +kubebuilder:default="5s"
	ResponseTime string `json:"responseTime,omitempty"`

	// Namespace for quarantined pods
	// +kubebuilder:default=infected
	QuarantineNamespace string `json:"quarantineNamespace,omitempty"`

	// Automatically kill infected pods
	// +kubebuilder:default=true
	AutoKill bool `json:"autoKill,omitempty"`
}

// AntibodiesSpec defines the vector memory configuration
type AntibodiesSpec struct {
	// Vector database type (e.g., qdrant)
	// +kubebuilder:validation:Enum=qdrant;milvus;pinecone
	// +kubebuilder:default=qdrant
	VectorDB string `json:"vectorDB,omitempty"`

	// How long to retain threat signatures
	// +kubebuilder:default="90d"
	SignatureRetention string `json:"signatureRetention,omitempty"`
}

// CircadianRhythmSpec defines the day/night scaling configuration
type CircadianRhythmSpec struct {
	// Sunshine (active) hours in format "HH:MM-HH:MM"
	// +kubebuilder:default="06:00-22:00"
	SunshineHours string `json:"sunshineHours,omitempty"`

	// Moonlight (sleep) hours in format "HH:MM-HH:MM"
	// +kubebuilder:default="22:00-06:00"
	MoonlightHours string `json:"moonlightHours,omitempty"`

	// Number of replicas during sunshine hours
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:default=10
	SunshineReplicas int32 `json:"sunshineReplicas,omitempty"`

	// Number of replicas during moonlight hours
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:default=2
	MoonlightReplicas int32 `json:"moonlightReplicas,omitempty"`
}

// AutoimmuneSpec defines the self-protection configuration
type AutoimmuneSpec struct {
	// Enable autoimmune protection
	// +kubebuilder:default=false
	Enabled bool `json:"enabled,omitempty"`

	// List of trusted image patterns
	TrustedImages []string `json:"trustedImages,omitempty"`
}

// ImmuneSystemSpec defines the desired state of ImmuneSystem
type ImmuneSystemSpec struct {
	// Red blood cells (transport layer)
	RedBloodCells RedBloodCellsSpec `json:"redBloodCells,omitempty"`

	// White blood cells (security scanners)
	WhiteBloodCells WhiteBloodCellsSpec `json:"whiteBloodCells,omitempty"`

	// Antibodies (vector memory)
	Antibodies AntibodiesSpec `json:"antibodies,omitempty"`

	// Circadian rhythm (day/night scaling)
	CircadianRhythm CircadianRhythmSpec `json:"circadianRhythm,omitempty"`

	// Autoimmune protection (don't attack self)
	Autoimmune AutoimmuneSpec `json:"autoimmune,omitempty"`
}

// CellStatus represents the status of a cell type
type CellStatus struct {
	// Ready count
	Ready int32 `json:"ready,omitempty"`

	// Desired count
	Desired int32 `json:"desired,omitempty"`

	// Status message
	Message string `json:"message,omitempty"`
}

// ImmuneSystemStatus defines the observed state of ImmuneSystem
type ImmuneSystemStatus struct {
	// Red blood cells status
	RedBloodCells CellStatus `json:"redBloodCells,omitempty"`

	// White blood cells status
	WhiteBloodCells CellStatus `json:"whiteBloodCells,omitempty"`

	// Antibodies status (number of loaded signatures)
	AntibodiesLoaded int32 `json:"antibodiesLoaded,omitempty"`

	// Current circadian mode (sunshine/moonlight)
	// +kubebuilder:validation:Enum=sunshine;moonlight
	CircadianMode string `json:"circadianMode,omitempty"`

	// Last heartbeat timestamp
	LastHeartbeat metav1.Time `json:"lastHeartbeat,omitempty"`

	// Overall health status
	// +kubebuilder:validation:Enum=ALIVE;DEGRADED;DEAD
	Health string `json:"health,omitempty"`

	// Conditions represent the latest available observations
	Conditions []metav1.Condition `json:"conditions,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:printcolumn:name="Health",type="string",JSONPath=".status.health",description="Overall health status"
// +kubebuilder:printcolumn:name="Mode",type="string",JSONPath=".status.circadianMode",description="Current circadian mode"
// +kubebuilder:printcolumn:name="Age",type="date",JSONPath=".metadata.creationTimestamp"

// ImmuneSystem is the Schema for the immunesystems API
type ImmuneSystem struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   ImmuneSystemSpec   `json:"spec,omitempty"`
	Status ImmuneSystemStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// ImmuneSystemList contains a list of ImmuneSystem
type ImmuneSystemList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []ImmuneSystem `json:"items"`
}

// SchemeGroupVersion is group version used to register these objects
var SchemeGroupVersion = schema.GroupVersion{Group: "swarm.strategickhaos.ai", Version: "v1"}

// Kind takes an unqualified kind and returns a Group qualified GroupKind
func Kind(kind string) schema.GroupKind {
	return SchemeGroupVersion.WithKind(kind).GroupKind()
}

// Resource takes an unqualified resource and returns a Group qualified GroupResource
func Resource(resource string) schema.GroupResource {
	return SchemeGroupVersion.WithResource(resource).GroupResource()
}

var (
	// SchemeBuilder initializes a scheme builder
	SchemeBuilder = runtime.NewSchemeBuilder(addKnownTypes)
	// AddToScheme is a global function that registers this API group & version to a scheme
	AddToScheme = SchemeBuilder.AddToScheme
)

// addKnownTypes adds our types to the API scheme by registering ImmuneSystem and ImmuneSystemList
func addKnownTypes(scheme *runtime.Scheme) error {
	scheme.AddKnownTypes(SchemeGroupVersion,
		&ImmuneSystem{},
		&ImmuneSystemList{},
	)
	metav1.AddToGroupVersion(scheme, SchemeGroupVersion)
	return nil
}
