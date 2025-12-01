// Package cells provides cell type implementations for the immune system
package cells

import (
	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// NewWhiteBloodCellDaemonSet creates a security scanner DaemonSet
// White blood cells detect and respond to threats in the cluster
func NewWhiteBloodCellDaemonSet(namespace, scanner string) *appsv1.DaemonSet {
	labels := map[string]string{
		"cell-type":  "white-blood",
		"scanner":    scanner,
		"managed-by": "immune-operator",
	}

	// Determine container spec based on scanner type
	var container corev1.Container
	var volumes []corev1.Volume

	switch scanner {
	case "trivy":
		container = corev1.Container{
			Name:  "trivy",
			Image: "aquasec/trivy:latest",
			Args:  []string{"server", "--listen", "0.0.0.0:4954"},
			Ports: []corev1.ContainerPort{
				{
					ContainerPort: 4954,
					Name:          "trivy",
				},
			},
			SecurityContext: &corev1.SecurityContext{
				ReadOnlyRootFilesystem: boolPtr(true),
				RunAsNonRoot:           boolPtr(true),
				RunAsUser:              int64Ptr(10000),
			},
		}
	default: // falco
		container = corev1.Container{
			Name:  "falco",
			Image: "falcosecurity/falco:latest",
			SecurityContext: &corev1.SecurityContext{
				Privileged: boolPtr(true),
			},
			VolumeMounts: []corev1.VolumeMount{
				{
					MountPath: "/host/proc",
					Name:      "proc",
					ReadOnly:  true,
				},
				{
					MountPath: "/host/dev",
					Name:      "dev",
					ReadOnly:  true,
				},
				{
					MountPath: "/host/boot",
					Name:      "boot",
					ReadOnly:  true,
				},
			},
		}
		volumes = []corev1.Volume{
			{
				Name: "proc",
				VolumeSource: corev1.VolumeSource{
					HostPath: &corev1.HostPathVolumeSource{
						Path: "/proc",
					},
				},
			},
			{
				Name: "dev",
				VolumeSource: corev1.VolumeSource{
					HostPath: &corev1.HostPathVolumeSource{
						Path: "/dev",
					},
				},
			},
			{
				Name: "boot",
				VolumeSource: corev1.VolumeSource{
					HostPath: &corev1.HostPathVolumeSource{
						Path: "/boot",
					},
				},
			},
		}
	}

	return &appsv1.DaemonSet{
		ObjectMeta: metav1.ObjectMeta{
			Name:      "wbc-" + scanner,
			Namespace: namespace,
			Labels:    labels,
		},
		Spec: appsv1.DaemonSetSpec{
			Selector: &metav1.LabelSelector{
				MatchLabels: labels,
			},
			Template: corev1.PodTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: labels,
				},
				Spec: corev1.PodSpec{
					Containers:                    []corev1.Container{container},
					Volumes:                       volumes,
					HostPID:                       scanner == "falco",
					HostNetwork:                   scanner == "falco",
					ServiceAccountName:            "wbc-scanner",
					TerminationGracePeriodSeconds: int64Ptr(30),
					Tolerations: []corev1.Toleration{
						{
							// Allow scheduling on all nodes including masters
							Effect:   corev1.TaintEffectNoSchedule,
							Operator: corev1.TolerationOpExists,
						},
					},
				},
			},
			UpdateStrategy: appsv1.DaemonSetUpdateStrategy{
				Type: appsv1.RollingUpdateDaemonSetStrategyType,
			},
		},
	}
}

// boolPtr returns a pointer to a bool
func boolPtr(b bool) *bool {
	return &b
}

// int64Ptr returns a pointer to an int64
func int64Ptr(i int64) *int64 {
	return &i
}
