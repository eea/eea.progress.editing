"""Character counting utilities - mirrors volto-group-block logic"""

import re


def count_chars_without_spaces(text):
    """Count characters excluding whitespace

    Mirrors frontend regex /[^\s\\]/g from volto-group-block
    """
    if not text:
        return 0
    return len(re.findall(r"[^\s\\]", text))


def count_chars_with_spaces(text):
    """Count all characters including whitespace"""
    return len(text) if text else 0


def extract_text_from_slate_value(value):
    """Extract plain text from slate value array

    Mirrors frontend serializeNodesToText() from volto-slate exactly.
    Slate value is structured like:
    [{"type": "p", "children": [{"text": "Hello"}, {"text": " world"}]}]

    Frontend logic:
    - Text nodes are trimmed
    - Children are joined with space ' '
    - Top-level nodes are joined with newline '\\n'
    """
    if not value or not isinstance(value, list):
        return ""

    def concatenated_string(node):
        """Mirrors frontend ConcatenatedString function"""
        if isinstance(node, dict):
            # Text node - return trimmed text
            if "text" in node:
                return node["text"].strip()
            # Element node - join children with space
            if "children" in node:
                return " ".join(
                    concatenated_string(child) for child in node["children"]
                )
        return ""

    # Join top-level nodes with newline (like frontend)
    return "\n".join(concatenated_string(node) for node in value)


def count_chars_in_block(block, ignore_spaces=True, countable_types=None):
    """Count characters in a single block

    Args:
        block: Block data dict
        ignore_spaces: Whether to exclude whitespace (default True)
        countable_types: List of block types to count (default: slate, description)

    Returns:
        int: Character count
    """
    if countable_types is None:
        countable_types = ["slate", "description"]

    block_type = block.get("@type", "")
    if block_type not in countable_types:
        return 0

    # Get text from plaintext field or extract from slate value
    text = block.get("plaintext", "")
    if not text and block.get("value"):
        text = extract_text_from_slate_value(block.get("value"))

    if ignore_spaces:
        return count_chars_without_spaces(text)
    return count_chars_with_spaces(text)


def count_chars_in_group_block(group_block, ignore_spaces=True, countable_types=None):
    """Count all characters in a group block's nested blocks

    Recursively counts characters in all nested blocks within a group.

    Args:
        group_block: Group block data dict
        ignore_spaces: Whether to exclude whitespace (default True)
        countable_types: List of block types to count

    Returns:
        int: Total character count
    """
    if countable_types is None:
        countable_types = ["slate", "description"]

    total = 0
    data = group_block.get("data", {})
    blocks = data.get("blocks", {})

    for block in blocks.values():
        total += count_chars_in_block(block, ignore_spaces, countable_types)
        # Recursively handle nested groups
        if block.get("@type") == "group":
            total += count_chars_in_group_block(block, ignore_spaces, countable_types)

    return total


def get_default_over_percent(title, max_chars):
    """Get default maxCharsOverPercent based on section title or maxChars

    Fallback for existing indicators without maxCharsOverPercent field.

    Args:
        title: Block title
        max_chars: Maximum characters limit

    Returns:
        int: Default over percent (0, 10, or 20)
    """
    title_lower = (title or "").lower()

    # Match by title
    if "aggregate" in title_lower and "disaggregate" not in title_lower:
        return 20  # Aggregate level assessment: 20% over
    elif "disaggregate" in title_lower:
        return 10  # Disaggregate level assessment: 10% over
    elif "header" in title_lower or "summary" in title_lower:
        return 0  # Content header/Summary: strict limit

    # Fallback by maxChars value
    if max_chars == 2000:
        return 20  # Aggregate
    elif max_chars == 1000:
        return 10  # Disaggregate
    elif max_chars == 500:
        return 0  # Summary

    return 0  # Default: no over percent


def get_blocks_with_char_limits(blocks):
    """Find all group blocks that have maxChars defined

    Args:
        blocks: Dict of blocks from content

    Returns:
        list: List of dicts with block info including maxChars and maxCharsOverPercent
    """
    results = []
    for block_id, block in (blocks or {}).items():
        if block.get("@type") == "group" and block.get("maxChars"):
            max_chars = int(block.get("maxChars", 0))
            title = block.get("title", block_id)

            # Use maxCharsOverPercent if present, otherwise use fallback
            if "maxCharsOverPercent" in block:
                over_percent = int(block.get("maxCharsOverPercent", 0))
            else:
                over_percent = get_default_over_percent(title, max_chars)

            results.append(
                {
                    "block_id": block_id,
                    "title": title,
                    "maxChars": max_chars,
                    "maxCharsOverPercent": over_percent,
                    "ignoreSpaces": block.get("ignoreSpaces", True),
                    "block": block,
                }
            )
    return results


def validate_all_char_limits(context):
    """Validate all blocks with maxChars in content

    Finds all group blocks with maxChars defined and validates
    that their character count is within the limit (including cap percentage).

    Args:
        context: Plone content object with blocks attribute

    Returns:
        list: List of validation results with is_valid, title, counts
    """
    blocks = getattr(context, "blocks", {}) or {}
    blocks_with_limits = get_blocks_with_char_limits(blocks)

    results = []
    for item in blocks_with_limits:
        ignore_spaces = item.get("ignoreSpaces", True)
        current_count = count_chars_in_group_block(item["block"], ignore_spaces)
        max_chars = item["maxChars"]
        over_percent = item.get("maxCharsOverPercent", 0)

        # Calculate effective max with cap percentage
        # e.g., maxChars=2000, maxCharsOverPercent=20 -> effective_max=2400
        effective_max = int(max_chars * (1 + over_percent / 100))
        is_valid = current_count <= effective_max

        results.append(
            {
                "block_id": item["block_id"],
                "title": item["title"],
                "current_count": current_count,
                "max_chars": max_chars,
                "effective_max": effective_max,
                "is_valid": is_valid,
            }
        )

    return results
