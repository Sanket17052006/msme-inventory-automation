def stock_color(stock: int, reorder_point: int) -> str:
    if stock <= reorder_point * 0.5:
        return "🔴"  # critical
    if stock <= reorder_point:
        return "🟡"  # warning
    return "🟢"  # healthy
