#!/usr/bin/env -S uv run

"""
Possible use:

import monitor

@app.get("/asdf")
async def asdf():
    return monitor.endpoint()


call the functions with curl:

curl localhost:8080/asdf

"""

import gc
import sys
import tracemalloc
from collections import Counter
from tracemalloc import Snapshot
from typing import ClassVar

# Start tracemalloc to track memory allocation
tracemalloc.start()


class Monitor:
    LIMIT: ClassVar[int] = 16
    previous_snapshot: ClassVar[Snapshot] = tracemalloc.take_snapshot()


def get_memory_snapshot() -> str:
    out: str = ""
    gc.collect()
    """Capture a snapshot of current memory usage by type."""
    snapshot: Snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")
    out += "[Top memory usage]\n"

    for stat in top_stats[: Monitor.LIMIT]:  # Show top memory-consuming lines
        out += str(stat) + "\n"

    deltas = snapshot.compare_to(Monitor.previous_snapshot, "lineno")

    # Display the top 10 changes in memory usage
    out += "Top memory differences by type:\n"
    for delta in deltas[:10]:
        out += f"delta: {str(delta)}\n"

    Monitor.previous_snapshot = snapshot
    del top_stats
    del deltas
    return out


def show_top_garbage_objects(limit: int = Monitor.LIMIT) -> str:
    # Enable garbage collection and inspect `gc.garbage`
    out: str = ""
    if not gc.garbage:
        out += "No uncollectable garbage found.\n"
        return out

    # Get objects in `gc.garbage` and their sizes
    garbage_info = [(obj, sys.getsizeof(obj)) for obj in gc.garbage]

    # Sort by size (descending) to get the largest objects first
    garbage_info.sort(key=lambda x: x[1], reverse=True)

    # Log the top `limit` objects by size
    out += "Top {limit} uncollectable objects in garbage:\n"
    for i, (obj, size) in enumerate(garbage_info[:limit], start=1):
        # Use repr(obj)[:100] to truncate object representation to 100 characters for readability
        out += (
            f"{i}. Type: {type(obj)}, Size: {size} bytes, Object: {repr(obj)[:100]}..."
        )
    return out


def show_top_garbage_objects_by_count(limit: int = Monitor.LIMIT) -> str:
    out: str = ""
    # Force garbage collection to ensure we get the latest data
    gc.collect()

    # Check for uncollectable garbage objects
    if not gc.garbage:
        out += "No uncollectable garbage found.\n"

    return out

    # Count objects by type in gc.garbage
    type_counts = Counter(type(obj) for obj in gc.garbage)

    # Sort by count (descending) and get the top `limit` types
    top_types = type_counts.most_common(limit)

    # Log the top types by count
    out += f"Top {limit} uncollectable object types in garbage by count:"
    for i, (obj_type, count) in enumerate(top_types, start=1):
        out += f"{i}. Type: {obj_type}, Count: {count}\n"

    return out


def count_objects_by_type() -> str:
    """Count objects in memory by type."""

    out: str = ""
    out += f"total obj: {str(len(gc.get_objects()))}\n"
    obj_counts: Counter[str] = Counter(type(obj).__name__ for obj in gc.get_objects())
    out += "[Object counts by type]\n"
    obj_type: str
    count: int
    for obj_type, count in obj_counts.most_common(
        Monitor.LIMIT
    ):  # Show top object types
        out += f"{obj_type}: {count}\n"

    return out


def endpoint() -> str:
    """endpoint handler"""
    out: str = ""
    out += get_memory_snapshot() + "\n"
    out += count_objects_by_type() + "\n"
    out += show_top_garbage_objects_by_count() + "\n"
    out += "Total: " + str(len(gc.get_objects())) + " objects. \n"
    return out + "\n\n"


def main():
    print(endpoint())


if __name__ == "__main__":
    main()
