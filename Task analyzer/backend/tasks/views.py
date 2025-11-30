from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from uuid import uuid4

# Import your Task model
from .models import Task

# Helper to detect circular dependencies
def has_circular_dep(tasks):
    graph = {t['id']: t.get('dependencies', []) for t in tasks}
    visited = set()
    rec_stack = set()

    def dfs(v):
        visited.add(v)
        rec_stack.add(v)
        for neighbor in graph.get(v, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(v)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False

# Core logic for scoring tasks
def analyze_logic(tasks, strategy="smart"):
    analyzed = []

    for task in tasks:
        task_id = task.get("id") or str(uuid4())
        title = task.get("title", "Untitled")
        importance = int(task.get("importance", 5))
        estimated_hours = int(task.get("estimated_hours", 5))
        dependencies = task.get("dependencies", [])

        due_date_str = task.get("due_date", datetime.now().strftime("%Y-%m-%d"))
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        today = datetime.now()
        days_left = (due_date - today).days

        score = 0
        reasons = []

        if strategy == "fastest":
            score += max(1, 10 - estimated_hours)
            reasons.append(f"Fastest Wins score: {max(1,10-estimated_hours)}")

        elif strategy == "highimpact":
            score += importance
            reasons.append(f"High Impact importance: {importance}")

        elif strategy == "deadline":
            urgency = max(0, 10 - max(days_left, 0))
            score += urgency
            reasons.append(f"Deadline Driven urgency: {urgency}")

        else:  # Smart (default)
            urgency = max(0, 10 - max(days_left,0))
            effort_bonus = max(1, 10 - estimated_hours)
            dep_bonus = len(dependencies) * 2

            score = urgency + importance + effort_bonus + dep_bonus

            reasons.extend([
                f"Urgency: {urgency}",
                f"Importance: {importance}",
                f"Effort bonus: {effort_bonus}",
                f"Dependencies bonus: {dep_bonus}",
            ])

        analyzed.append({
            "id": task_id,
            "title": title,
            "importance": importance,
            "estimated_hours": estimated_hours,
            "due_date": due_date_str,
            "dependencies": dependencies,
            "score": score,
            "reason": reasons,
        })

    return analyzed

# API endpoint: Analyze tasks
@api_view(["POST"])
def analyze_tasks(request):
    tasks = request.data.get("tasks", [])
    strategy = request.data.get("strategy", "smart")

    if not tasks:
        return Response({"error": "No tasks provided"}, status=400)

    if has_circular_dep(tasks):
        return Response({"error": "Circular dependencies detected"}, status=400)

    analyzed = analyze_logic(tasks, strategy)
    return Response(analyzed, status=200)

# API endpoint: Suggest top 3 tasks
@api_view(["POST"])
def suggest_tasks(request):
    tasks = request.data.get("tasks", [])
    strategy = request.data.get("strategy", "smart")

    if not tasks:
        return Response({"error": "No tasks provided"}, status=400)

    if has_circular_dep(tasks):
        return Response({"error": "Circular dependencies detected"}, status=400)

    analyzed = analyze_logic(tasks, strategy)
    top_3 = sorted(analyzed, key=lambda x: x["score"], reverse=True)[:3]

    return Response(top_3, status=200)

# API endpoint: List and create tasks
@api_view(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        data = []
        for t in tasks:
            # Ensure due_date is string for JSON response
            if isinstance(t.due_date, str):
                due_date_str = t.due_date
            else:
                due_date_str = t.due_date.strftime("%Y-%m-%d")
            data.append({
                "id": t.id,
                "title": t.title,
                "estimated_hours": t.estimated_hours,
                "due_date": due_date_str,
                "importance": t.importance,
                "dependencies": [],
            })
        return Response(data)

    if request.method == "POST":
        title = request.data.get("title")
        estimated_hours = request.data.get("estimated_hours")
        due_date = request.data.get("due_date")
        importance = request.data.get("importance", 5)

        # Convert due_date string to datetime
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")

        task = Task.objects.create(
            title=title,
            estimated_hours=estimated_hours,
            due_date=due_date_obj,
            importance=importance
        )

        return Response({
            "id": task.id,
            "title": task.title,
            "estimated_hours": task.estimated_hours,
            "due_date": task.due_date.strftime("%Y-%m-%d"),
            "importance": task.importance,
        })
