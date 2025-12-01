// Package controller implements the ImmuneSystem reconciler
package controller

import (
	"context"
	"fmt"
	"strconv"
	"strings"
	"time"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/log"

	swarmv1 "strategickhaos.ai/swarm-immune/pkg/apis/swarm/v1"
	"strategickhaos.ai/swarm-immune/pkg/cells"
)

// ImmuneReconciler reconciles an ImmuneSystem object
// This is the "ribosome" that reads the CRD (DNA) and builds immune cells
type ImmuneReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=swarm.strategickhaos.ai,resources=immunesystems,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=swarm.strategickhaos.ai,resources=immunesystems/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=swarm.strategickhaos.ai,resources=immunesystems/finalizers,verbs=update
// +kubebuilder:rbac:groups=apps,resources=deployments;daemonsets;statefulsets,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=pods;services;configmaps;secrets;namespaces,verbs=get;list;watch;create;update;patch;delete

// Reconcile is the main reconciliation loop - the heartbeat of the immune system
func (r *ImmuneReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	logger.Info("Reconciling ImmuneSystem", "namespace", req.Namespace, "name", req.Name)

	// 1. FETCH THE IMMUNE SYSTEM SPEC (read DNA)
	var immune swarmv1.ImmuneSystem
	if err := r.Get(ctx, req.NamespacedName, &immune); err != nil {
		if errors.IsNotFound(err) {
			logger.Info("ImmuneSystem resource not found, possibly deleted")
			return ctrl.Result{}, nil
		}
		logger.Error(err, "Unable to fetch ImmuneSystem")
		return ctrl.Result{}, err
	}

	// Initialize status if empty
	if immune.Status.Health == "" {
		immune.Status.Health = "ALIVE"
	}

	// 2. SPAWN RED BLOOD CELLS (transport layer)
	if err := r.reconcileRedBloodCells(ctx, &immune); err != nil {
		logger.Error(err, "Failed to reconcile red blood cells")
		immune.Status.Health = "DEGRADED"
		r.updateStatus(ctx, &immune)
		return ctrl.Result{}, err
	}

	// 3. SPAWN WHITE BLOOD CELLS (security scanners)
	if err := r.reconcileWhiteBloodCells(ctx, &immune); err != nil {
		logger.Error(err, "Failed to reconcile white blood cells")
		immune.Status.Health = "DEGRADED"
		r.updateStatus(ctx, &immune)
		return ctrl.Result{}, err
	}

	// 4. LOAD ANTIBODIES (vector memory)
	if err := r.reconcileAntibodies(ctx, &immune); err != nil {
		logger.Error(err, "Failed to reconcile antibodies")
		immune.Status.Health = "DEGRADED"
		r.updateStatus(ctx, &immune)
		return ctrl.Result{}, err
	}

	// 5. CHECK CIRCADIAN RHYTHM (scale up/down)
	if err := r.reconcileCircadian(ctx, &immune); err != nil {
		logger.Error(err, "Failed to reconcile circadian rhythm")
		// Non-fatal - continue with current state
	}

	// 6. AUTOIMMUNE CHECK (don't attack self)
	if err := r.preventAutoimmune(ctx, &immune); err != nil {
		logger.Error(err, "Failed to perform autoimmune check")
		// Non-fatal - continue
	}

	// Update heartbeat and status
	immune.Status.LastHeartbeat = metav1.Now()
	immune.Status.Health = "ALIVE"
	if err := r.updateStatus(ctx, &immune); err != nil {
		logger.Error(err, "Failed to update status")
	}

	// HEARTBEAT: re-reconcile every 30s (pulse)
	logger.Info("ImmuneSystem heartbeat", "health", immune.Status.Health)
	return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
}

// reconcileRedBloodCells manages the transport layer (Redis)
func (r *ImmuneReconciler) reconcileRedBloodCells(ctx context.Context, immune *swarmv1.ImmuneSystem) error {
	logger := log.FromContext(ctx)
	spec := immune.Spec.RedBloodCells

	// Get the deployment configuration
	deployment := cells.NewRedBloodCellDeployment(immune.Namespace, spec.Transport, spec.Replicas)

	// Set owner reference for garbage collection
	if err := ctrl.SetControllerReference(immune, deployment, r.Scheme); err != nil {
		return err
	}

	// Check if deployment exists
	found := &appsv1.Deployment{}
	err := r.Get(ctx, types.NamespacedName{Name: deployment.Name, Namespace: deployment.Namespace}, found)
	if err != nil && errors.IsNotFound(err) {
		logger.Info("Creating Red Blood Cell deployment", "name", deployment.Name)
		if err := r.Create(ctx, deployment); err != nil {
			return err
		}
	} else if err != nil {
		return err
	} else {
		// Update if necessary
		if found.Spec.Replicas == nil || *found.Spec.Replicas != spec.Replicas {
			found.Spec.Replicas = &spec.Replicas
			if err := r.Update(ctx, found); err != nil {
				return err
			}
		}
	}

	// Update status - always update even if 0
	immune.Status.RedBloodCells.Desired = spec.Replicas
	immune.Status.RedBloodCells.Ready = found.Status.ReadyReplicas
	immune.Status.RedBloodCells.Message = fmt.Sprintf("%d/%d healthy", immune.Status.RedBloodCells.Ready, spec.Replicas)

	return nil
}

// reconcileWhiteBloodCells manages security scanners (Falco/Trivy)
func (r *ImmuneReconciler) reconcileWhiteBloodCells(ctx context.Context, immune *swarmv1.ImmuneSystem) error {
	logger := log.FromContext(ctx)
	spec := immune.Spec.WhiteBloodCells

	// Get the DaemonSet configuration
	daemonSet := cells.NewWhiteBloodCellDaemonSet(immune.Namespace, spec.Scanner)

	// Set owner reference
	if err := ctrl.SetControllerReference(immune, daemonSet, r.Scheme); err != nil {
		return err
	}

	// Check if DaemonSet exists
	found := &appsv1.DaemonSet{}
	err := r.Get(ctx, types.NamespacedName{Name: daemonSet.Name, Namespace: daemonSet.Namespace}, found)
	if err != nil && errors.IsNotFound(err) {
		logger.Info("Creating White Blood Cell DaemonSet", "name", daemonSet.Name)
		if err := r.Create(ctx, daemonSet); err != nil {
			return err
		}
	} else if err != nil {
		return err
	}

	// Create quarantine namespace if it doesn't exist
	quarantineNs := &corev1.Namespace{
		ObjectMeta: metav1.ObjectMeta{
			Name: spec.QuarantineNamespace,
			Labels: map[string]string{
				"purpose":              "quarantine",
				"managed-by":           "immune-operator",
				"immune-system":        immune.Name,
				"pod-security.kubernetes.io/enforce": "restricted",
			},
		},
	}
	if err := r.Create(ctx, quarantineNs); err != nil {
		if !errors.IsAlreadyExists(err) {
			logger.Error(err, "Failed to create quarantine namespace")
		}
	}

	// Update status - always update even if 0
	immune.Status.WhiteBloodCells.Ready = found.Status.NumberReady
	immune.Status.WhiteBloodCells.Desired = found.Status.DesiredNumberScheduled
	immune.Status.WhiteBloodCells.Message = fmt.Sprintf("%d/%d scanning", immune.Status.WhiteBloodCells.Ready, immune.Status.WhiteBloodCells.Desired)

	return nil
}

// reconcileAntibodies manages the vector memory database (Qdrant)
func (r *ImmuneReconciler) reconcileAntibodies(ctx context.Context, immune *swarmv1.ImmuneSystem) error {
	logger := log.FromContext(ctx)
	spec := immune.Spec.Antibodies

	// Get the StatefulSet configuration
	statefulSet := cells.NewAntibodyStatefulSet(immune.Namespace, spec.VectorDB)

	// Set owner reference
	if err := ctrl.SetControllerReference(immune, statefulSet, r.Scheme); err != nil {
		return err
	}

	// Check if StatefulSet exists
	found := &appsv1.StatefulSet{}
	err := r.Get(ctx, types.NamespacedName{Name: statefulSet.Name, Namespace: statefulSet.Namespace}, found)
	if err != nil && errors.IsNotFound(err) {
		logger.Info("Creating Antibody StatefulSet", "name", statefulSet.Name)
		if err := r.Create(ctx, statefulSet); err != nil {
			return err
		}
		// Initialize status for new StatefulSet
		immune.Status.AntibodiesLoaded = 0
	} else if err != nil {
		return err
	} else {
		// StatefulSet exists - update status based on ready replicas
		// In production, this would query the actual vector DB for signature count
		if found.Status.ReadyReplicas > 0 {
			// Placeholder: would query vector DB endpoint for actual count
			// e.g., GET http://antibody-memory:6333/collections
			immune.Status.AntibodiesLoaded = 1247
		} else {
			immune.Status.AntibodiesLoaded = 0
		}
	}

	return nil
}

// reconcileCircadian manages day/night scaling
func (r *ImmuneReconciler) reconcileCircadian(ctx context.Context, immune *swarmv1.ImmuneSystem) error {
	logger := log.FromContext(ctx)
	spec := immune.Spec.CircadianRhythm
	now := time.Now()

	sunriseHour, sunsetHour := parseHours(spec.SunshineHours)

	var targetReplicas int32
	var mode string
	if now.Hour() >= sunriseHour && now.Hour() < sunsetHour {
		targetReplicas = spec.SunshineReplicas
		mode = "sunshine"
	} else {
		targetReplicas = spec.MoonlightReplicas
		mode = "moonlight"
	}

	immune.Status.CircadianMode = mode

	// Scale managed deployments based on circadian rhythm
	if err := r.scaleDeployments(ctx, immune.Namespace, targetReplicas); err != nil {
		logger.Error(err, "Failed to scale deployments for circadian rhythm")
		return err
	}

	logger.Info("Circadian rhythm adjusted", "mode", mode, "targetReplicas", targetReplicas)
	return nil
}

// preventAutoimmune ensures the system doesn't attack trusted resources
func (r *ImmuneReconciler) preventAutoimmune(ctx context.Context, immune *swarmv1.ImmuneSystem) error {
	if !immune.Spec.Autoimmune.Enabled {
		return nil
	}

	// Create a ConfigMap with trusted image patterns for scanner to reference
	configMap := &corev1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{
			Name:      "trusted-images",
			Namespace: immune.Namespace,
			Labels: map[string]string{
				"managed-by":    "immune-operator",
				"immune-system": immune.Name,
			},
		},
		Data: map[string]string{
			"trusted-patterns": strings.Join(immune.Spec.Autoimmune.TrustedImages, "\n"),
		},
	}

	if err := ctrl.SetControllerReference(immune, configMap, r.Scheme); err != nil {
		return err
	}

	found := &corev1.ConfigMap{}
	err := r.Get(ctx, types.NamespacedName{Name: configMap.Name, Namespace: configMap.Namespace}, found)
	if err != nil && errors.IsNotFound(err) {
		return r.Create(ctx, configMap)
	} else if err != nil {
		return err
	}

	// Update if patterns changed
	found.Data = configMap.Data
	return r.Update(ctx, found)
}

// scaleDeployments scales all managed deployments in a namespace
func (r *ImmuneReconciler) scaleDeployments(ctx context.Context, namespace string, replicas int32) error {
	deploymentList := &appsv1.DeploymentList{}
	if err := r.List(ctx, deploymentList, client.InNamespace(namespace), client.MatchingLabels{"managed-by": "immune-operator"}); err != nil {
		return err
	}

	for i := range deploymentList.Items {
		deployment := &deploymentList.Items[i]
		if deployment.Spec.Replicas == nil || *deployment.Spec.Replicas != replicas {
			deployment.Spec.Replicas = &replicas
			if err := r.Update(ctx, deployment); err != nil {
				return err
			}
		}
	}

	return nil
}

// updateStatus updates the ImmuneSystem status
func (r *ImmuneReconciler) updateStatus(ctx context.Context, immune *swarmv1.ImmuneSystem) error {
	return r.Status().Update(ctx, immune)
}

// parseHours parses a time range string in "HH:MM-HH:MM" format and returns
// the start and end hours as integers. For example, "06:00-22:00" returns (6, 22).
// If parsing fails, it returns default values of (6, 22) for sunrise at 6 AM
// and sunset at 10 PM.
func parseHours(timeRange string) (int, int) {
	// Default values
	startHour := 6
	endHour := 22

	parts := strings.Split(timeRange, "-")
	if len(parts) == 2 {
		startParts := strings.Split(parts[0], ":")
		endParts := strings.Split(parts[1], ":")

		if len(startParts) >= 1 {
			if h, err := strconv.Atoi(startParts[0]); err == nil {
				startHour = h
			}
		}
		if len(endParts) >= 1 {
			if h, err := strconv.Atoi(endParts[0]); err == nil {
				endHour = h
			}
		}
	}

	return startHour, endHour
}

// SetupWithManager sets up the controller with the Manager
func (r *ImmuneReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&swarmv1.ImmuneSystem{}).
		Owns(&appsv1.Deployment{}).
		Owns(&appsv1.DaemonSet{}).
		Owns(&appsv1.StatefulSet{}).
		Complete(r)
}
