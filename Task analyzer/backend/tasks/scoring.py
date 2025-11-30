from datetime import date

def calculate_task_score(task, all_tasks):
    """
    Calculate priority score for a single task.
    Returns: (score, explanation)
    """

    today = date.today()

    # --- 1. Urgency Score (0 to 10) ---
    days_left = (task['due_date'] - today).days
    if days_left < 0:
        urgency = 10  # overdue tasks are highest urgency
    else:
        urgency = max(0, 10 - days_left)

    # --- 2. Importance Score (1 to 10) ---
    importance = task['importance']

    # --- 3. Effort Score (higher for small tasks) ---
    estimated_hours = task['estimated_hours']
    effort_score = 10 / (1 + estimated_hours)

    # --- 4. Dependency Score ---
    # tasks that block others rank higher
    task_id = task['id']
    dependency_score = sum(
        1 for t in all_tasks if task_id in t.get('dependencies', [])
    )

    # --- Final Weighted Score ---
    final_score = (
        0.40 * urgency
        + 0.35 * importance
        + 0.15 * effort_score
        + 0.10 * dependency_score
    )

    # --- Explanation ---
    explanation = {
        "urgency_score": urgency,
        "importance_score": importance,
        "effort_score": round(effort_score, 2),
        "dependency_score": dependency_score,
        "final_score": round(final_score, 2),
        "reason": (
            f"Urgency {urgency}, Importance {importance}, "
            f"Effort Score {round(effort_score,2)}, "
            f"Dependency Score {dependency_score}"
        )
    }

    return final_score, explanation
