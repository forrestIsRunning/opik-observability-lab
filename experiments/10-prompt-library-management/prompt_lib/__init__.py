"""Opik connection settings (single source of truth)."""

import os
from dataclasses import dataclass, field

import opik


@dataclass(frozen=True)
class OpikSettings:
    """Opik connection parameters, loaded from environment with sensible defaults."""

    host: str = "http://localhost:5173/api"
    workspace: str = "default"
    project: str = "prompt-library-demo"

    @classmethod
    def from_env(cls) -> "OpikSettings":
        return cls(
            host=os.getenv("OPIK_HOST", "http://localhost:5173/api"),
            workspace=os.getenv("OPIK_WORKSPACE", "default"),
            project=os.getenv("OPIK_PROJECT", "prompt-library-demo"),
        )

    def make_client(self, project_name: str | None = None) -> opik.Opik:
        """Create an Opik client and set it as the global client.

        Call once at process start so ``@opik.track`` and ``evaluate()``
        automatically reuse the same connection.
        """
        client = opik.Opik(
            project_name=project_name or self.project,
            host=self.host,
            workspace=self.workspace,
        )
        opik.set_global_client(client)
        return client


settings = OpikSettings.from_env()