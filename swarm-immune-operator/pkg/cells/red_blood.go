// Package cells provides cell type implementations for the immune system
package cells

import (
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/util/intstr"
)

// NewRedBloodCellDeployment creates a Redis transport layer deployment
// Red blood cells carry oxygen (data) throughout the body (cluster)
func NewRedBloodCellDeployment(namespace, transport string, replicas int32) *appsv1.Deployment {
	labels := map[string]string{
		"cell-type":  "red-blood",
		"transport":  transport,
		"managed-by": "immune-operator",
	}

	// Determine image based on transport type
	image := "redis:7-alpine"
	port := int32(6379)
	switch transport {
	case "kafka":
		image = "bitnami/kafka:3.6"
		port = 9092
	case "nats":
		image = "nats:2.10"
		port = 4222
	}

	return &appsv1.Deployment{
		ObjectMeta: metav1.ObjectMeta{
			Name:      "rbc-" + transport + "-transport",
			Namespace: namespace,
			Labels:    labels,
		},
		Spec: appsv1.DeploymentSpec{
			Replicas: &replicas,
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
							Name:  transport,
							Image: image,
							Ports: []corev1.ContainerPort{
								{
									ContainerPort: port,
									Name:          "transport",
								},
							},
							Resources: corev1.ResourceRequirements{
								Requests: corev1.ResourceList{
									corev1.ResourceMemory: resource.MustParse("64Mi"),
									corev1.ResourceCPU:    resource.MustParse("50m"),
								},
								Limits: corev1.ResourceList{
									corev1.ResourceMemory: resource.MustParse("256Mi"),
									corev1.ResourceCPU:    resource.MustParse("200m"),
								},
							},
							LivenessProbe: &corev1.Probe{
								ProbeHandler: corev1.ProbeHandler{
									TCPSocket: &corev1.TCPSocketAction{
										Port: intOrString(port),
									},
								},
								InitialDelaySeconds: 30,
								PeriodSeconds:       10,
							},
							ReadinessProbe: &corev1.Probe{
								ProbeHandler: corev1.ProbeHandler{
									TCPSocket: &corev1.TCPSocketAction{
										Port: intOrString(port),
									},
								},
								InitialDelaySeconds: 5,
								PeriodSeconds:       5,
							},
						},
					},
				},
			},
		},
	}
}

// intOrString creates an IntOrString from an int32
func intOrString(port int32) intstr.IntOrString {
	return intstr.FromInt32(port)
}
