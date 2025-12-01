// Package cells provides cell type implementations for the immune system
package cells

import (
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// NewAntibodyStatefulSet creates a vector database StatefulSet for threat signature memory
// Antibodies remember past threats and recognize patterns
func NewAntibodyStatefulSet(namespace, vectorDB string) *appsv1.StatefulSet {
	labels := map[string]string{
		"cell-type":  "antibody",
		"vector-db":  vectorDB,
		"managed-by": "immune-operator",
	}

	// Determine image and ports based on vector DB type
	image := "qdrant/qdrant:latest"
	port := int32(6333)
	grpcPort := int32(6334)
	switch vectorDB {
	case "milvus":
		image = "milvusdb/milvus:latest"
		port = 19530
		grpcPort = 19530
	case "pinecone":
		// Pinecone is a cloud service, use a placeholder
		image = "alpine:latest"
		port = 8080
		grpcPort = 8080
	}

	replicas := int32(1)
	storageSize := resource.MustParse("10Gi")

	return &appsv1.StatefulSet{
		ObjectMeta: metav1.ObjectMeta{
			Name:      "antibody-" + vectorDB,
			Namespace: namespace,
			Labels:    labels,
		},
		Spec: appsv1.StatefulSetSpec{
			ServiceName: vectorDB + "-headless",
			Replicas:    &replicas,
			Selector: &metav1.LabelSelector{
				MatchLabels: labels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: labels,
				},
				Spec: corev1.PodSpec{
					Containers: []corev1.Container{
						{
							Name:  vectorDB,
							Image: image,
							Ports: []corev1.ContainerPort{
								{
									ContainerPort: port,
									Name:          "http",
								},
								{
									ContainerPort: grpcPort,
									Name:          "grpc",
								},
							},
							VolumeMounts: []corev1.VolumeMount{
								{
									Name:      "antibody-storage",
									MountPath: "/qdrant/storage",
								},
							},
							Resources: corev1.ResourceRequirements{
								Requests: corev1.ResourceList{
									corev1.ResourceMemory: resource.MustParse("512Mi"),
									corev1.ResourceCPU:    resource.MustParse("100m"),
								},
								Limits: corev1.ResourceList{
									corev1.ResourceMemory: resource.MustParse("2Gi"),
									corev1.ResourceCPU:    resource.MustParse("1"),
								},
							},
						},
					},
				},
			},
			VolumeClaimTemplates: []corev1.PersistentVolumeClaim{
				{
					ObjectMeta: metav1.ObjectMeta{
						Name: "antibody-storage",
					},
					Spec: corev1.PersistentVolumeClaimSpec{
						AccessModes: []corev1.PersistentVolumeAccessMode{
							corev1.ReadWriteOnce,
						},
						Resources: corev1.VolumeResourceRequirements{
							Requests: corev1.ResourceList{
								corev1.ResourceStorage: storageSize,
							},
						},
					},
				},
			},
		},
	}
}
