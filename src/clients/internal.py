from typing import Optional

from .base import ClientBase


class InternalClient(ClientBase):
    def __init__(self, timeout: Optional[int] = 10):
        """
        Initializes the Local client.

        Args:
            timeout (int, optional): Timeout for the HTTP requests. Default is 10 seconds.
        """
        super(InternalClient, self).__init__(None, timeout)
