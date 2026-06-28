"""devclean — scan and remove node_modules / venvs to reclaim disk space."""

from devclean.models import CleanableItem, DeleteFailure, DeleteResult

__version__ = "1.1.0"

__all__ = ["CleanableItem", "DeleteFailure", "DeleteResult", "__version__"]
