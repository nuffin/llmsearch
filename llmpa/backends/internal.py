from typing import Optional

from .base import BackendBase


class InternalBackend(BackendBase):
    def __init__(self, timeout: Optional[int] = 10):
        """
        Initializes the Local client.

        Args:
            timeout (int, optional): Timeout for the HTTP requests. Default is 10 seconds.
        """
        super(InternalBackend, self).__init__(None, timeout)
