"""Error handling and retry logic for Tempest pipeline."""

import time
import logging
from typing import Callable, Any, Optional
from functools import wraps


class RetryableError(Exception):
    """Exception raised for errors that should trigger a retry."""
    pass


class NonRetryableError(Exception):
    """Exception raised for errors that should not be retried."""
    pass


def retry_with_exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    logger: Optional[logging.Logger] = None
):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exponential_base: Base for exponential backoff calculation
        logger: Logger instance for logging retry attempts
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retry_count = 0
            delay = base_delay

            while retry_count <= max_retries:
                try:
                    return func(*args, **kwargs)
                except NonRetryableError as e:
                    # Don't retry non-retryable errors
                    if logger:
                        logger.error(f"Non-retryable error in {func.__name__}: {str(e)}")
                    raise
                except Exception as e:
                    retry_count += 1
                    if retry_count > max_retries:
                        if logger:
                            logger.error(f"Max retries exceeded for {func.__name__}: {str(e)}")
                        raise

                    # Log the retry attempt
                    if logger:
                        logger.warning(
                            f"Error in {func.__name__} (attempt {retry_count}/{max_retries}): {str(e)}. "
                            f"Retrying in {delay:.2f}s..."
                        )

                    time.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)

            # Should never reach here
            raise RuntimeError(f"Unexpected error in retry logic for {func.__name__}")

        return wrapper
    return decorator


def safe_json_dump(data: Any, filepath: str, logger: Optional[logging.Logger] = None) -> bool:
    """
    Safely write JSON data to a file with backup.

    Args:
        data: Data to write
        filepath: Path to output file
        logger: Logger instance

    Returns:
        True if successful, False otherwise
    """
    import json
    import os
    import shutil

    try:
        # Create backup if file exists
        if os.path.exists(filepath):
            backup_path = f"{filepath}.backup"
            shutil.copy2(filepath, backup_path)
            if logger:
                logger.debug(f"Created backup: {backup_path}")

        # Write to temporary file first
        temp_path = f"{filepath}.tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Atomic rename
        os.replace(temp_path, filepath)

        if logger:
            logger.debug(f"Successfully wrote to {filepath}")
        return True

    except Exception as e:
        if logger:
            logger.error(f"Error writing to {filepath}: {str(e)}")
        return False


def create_progress_tracker(total: int, checkpoint_interval: int = 10):
    """
    Create a progress tracking context manager.

    Args:
        total: Total number of items to process
        checkpoint_interval: Save checkpoint every N items

    Returns:
        Progress tracker instance
    """
    class ProgressTracker:
        def __init__(self):
            self.current = 0
            self.total = total
            self.checkpoint_interval = checkpoint_interval
            self.start_time = time.time()

        def update(self, n: int = 1):
            """Update progress by n items."""
            self.current += n

        def should_checkpoint(self) -> bool:
            """Check if we should save a checkpoint."""
            return self.current % self.checkpoint_interval == 0

        def get_eta(self) -> str:
            """Get estimated time remaining."""
            if self.current == 0:
                return "Unknown"

            elapsed = time.time() - self.start_time
            rate = self.current / elapsed
            remaining = (self.total - self.current) / rate

            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)

            return f"{hours}h {minutes}m"

        def get_summary(self) -> str:
            """Get progress summary string."""
            percent = (self.current / self.total) * 100 if self.total > 0 else 0
            return f"{self.current}/{self.total} ({percent:.1f}%) - ETA: {self.get_eta()}"

    return ProgressTracker()
