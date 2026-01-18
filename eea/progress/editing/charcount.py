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

    Mirrors frontend serializeNodesToText() from volto-slate.
    Slate value is structured like:
    [{"type": "p", "children": [{"text": "Hello"}, {"text": " world"}]}]
    """
    if not value or not isinstance(value, list):
        return ""

    texts = []

    def traverse(node):
        if isinstance(node, dict):
            if "text" in node:
                texts.append(node["text"])
            if "children" in node:
                for child in node["children"]:
                    traverse(child)
        elif isinstance(node, list):
            for item in node:
                traverse(item)

    traverse(value)
    return "".join(texts)


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


def get_blocks_with_char_limits(blocks):
    """Find all group blocks that have maxChars defined

    Args:
        blocks: Dict of blocks from content

    Returns:
        list: List of dicts with block info including maxChars
    """
    results = []
    for block_id, block in (blocks or {}).items():
        if block.get("@type") == "group" and block.get("maxChars"):
            results.append(
                {
                    "block_id": block_id,
                    "title": block.get("title", block_id),
                    "maxChars": int(block.get("maxChars", 0)),
                    "ignoreSpaces": block.get("ignoreSpaces", True),
                    "block": block,
                }
            )
    return results


def validate_all_char_limits(context):
    """Validate all blocks with maxChars in content

    Finds all group blocks with maxChars defined and validates
    that their character count is within the limit.

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
        is_valid = current_count <= max_chars

        results.append(
            {
                "block_id": item["block_id"],
                "title": item["title"],
                "current_count": current_count,
                "max_chars": max_chars,
                "is_valid": is_valid,
            }
        )

    return results
