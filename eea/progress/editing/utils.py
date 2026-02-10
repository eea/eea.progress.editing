"""Character counting utilities - mirrors volto-group-block logic"""

import math
from plone.restapi.blocks import visit_blocks


def validate_all_char_limits(context):
    """Validate all blocks with maxChars in content

    Finds all group blocks with maxChars defined and validates
    that their character count is within the limit (including cap percentage).

    Args:
        context: Plone content object with blocks attribute

    Returns:
        list: List of validation results with is_valid, title, counts
    """
    results = []
    for item in visit_blocks(context, context.blocks):
        try:
            max_chars = int(item.get("maxChars", 0))
        except (ValueError, TypeError):
            # Skip blocks with invalid maxChars
            continue

        # Skip blocks without maxChars or with non-positive maxChars
        if not max_chars:
            continue

        try:
            current_count = int(item.get("charCount", 0))
        except (ValueError, TypeError):
            # Treat invalid charCount as 0
            continue

        # Skip blocks without charCount or with non-positive charCount
        if not current_count:
            continue

        try:
            orphans = int(item.get("maxCharsOverflowPercent", 0))
        except (ValueError, TypeError):
            # Treat invalid overflow percent as 0
            orphans = 0

        # Calculate effective max with overflow percentage
        # e.g., maxChars=2000, maxCharsOverflowPercent=20 -> effective_max=2400
        effective_max = math.ceil((max_chars * (100 + orphans)) / 100)
        is_valid = (current_count <= effective_max) if (effective_max > 0) else True

        results.append(
            {
                "title": item.get("title", "Section"),
                "current_count": current_count,
                "max_chars": max_chars,
                "effective_max": effective_max,
                "is_valid": is_valid,
            }
        )

    return results
