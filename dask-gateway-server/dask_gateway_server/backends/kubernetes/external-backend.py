"""
A Kubernetes backend implementation for dask-gateway where scaling is managed externally
by the user/frontend rather than automatically by the controller.
"""

from kubernetes_asyncio import client, config
from .backend import KubeBackend, KubeClusterConfig
from .controller import KubeController


class ExternallyManagedKubeBackend(KubeBackend):
    """A Kubernetes backend implementation where scaling is managed externally.

    This backend maintains all standard configuration but pairs with ExternallyManagedKubeController
    to allow worker scaling to be managed by the user/frontend rather than automatically.
    """

    async def setup(self, app):
        await super().setup(app)
        self.log.info("Externally managed Kubernetes backend initialized")


class ExternallyManagedKubeController(KubeController):
    """A Kubernetes controller that defers scaling decisions to external management.

    This controller disables automatic scaling by making the scale up/down operations
    no-ops, allowing worker scaling to be managed externally by the user/frontend
    while maintaining all other controller functionality.
    """

    async def handle_scale_up(self, cluster, sched_pod, info, replicas, delta):
        """No-op implementation of scale up.

        This effectively disables auto-scaling up of workers.
        """
        self.log.info(
            "Scale up requested but disabled in externally-managed controller (replicas=%d, delta=%d)",
            replicas,
            delta,
        )
        return False

    async def handle_scale_down(self, cluster, sched_pod, info, replicas, delta):
        """No-op implementation of scale down.

        This effectively disables auto-scaling down of workers.
        """
        self.log.info(
            "Scale down requested but disabled in externally-managed controller (replicas=%d, delta=%d)",
            replicas,
            delta,
        )
        return False
