# KnowledgePod Directory

This directory contains KnowledgePod custom resource instances. Each file represents one question from the 100 Bloom's Taxonomy questions mapped to its corresponding educational pod.

## Structure

```
k8s/knowledgepods/
├── example_pod_q001.yaml    # Example pod for Question #1
├── pod_q002.yaml            # (Generated) Pod for Question #2
├── ...
└── pod_q100.yaml            # (Generated) Pod for Question #100
```

## Generating Pods

Use the `strategickhaos_product_build.yaml` mission file with Claude/LLM to generate all KnowledgePod instances.

---

*StrategicKhaos Educational Swarm*
