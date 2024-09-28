from typing import List
import datetime as dt
from ..models import Assignment, Assignment2, Reward, Reward2, Task, Task2, DiveharderAll


def build_assignment_2(assignment: Assignment) -> Assignment2:
    """
    Transforms a raw Assignment object into an easier to understand Assignment2 object.

    Args:
        assignment (Assignment): The original assignment object.
        diveharder (DiveharderAll): Contextual object containing additional necessary information.

    Returns:
        Assignment2: The transformed assignment.
    """
    setting = assignment.setting
    reward = setting.reward
    ret = Assignment2(
        retrieved_at=assignment.retrieved_at,
        id=assignment.id32,
        progress=assignment.progress,
        expiration=(
            assignment.retrieved_at + dt.timedelta(seconds=assignment.expiresIn)
        ).isoformat(),
        briefing=setting.overrideBrief,
        title=setting.overrideTitle,
        description=setting.taskDescription,
        reward=Reward2(
            retrieved_at=reward.retrieved_at,
            type=reward.type,
            amount=reward.amount,
            id32=reward.id32,
        ),
        rewards=[Reward2(**r.model_dump()) for r in setting.rewards],
        tasks=[Task2(**t.model_dump()) for t in setting.tasks],
        type=setting.type,
        flags=setting.flags,
    )

    return ret


def build_all_assignments(assignments: List[Assignment]) -> List[Assignment2]:
    """
    Given a list of raw Assignment objects, return a list of Assignment2.

    Args:
        assignments (List[Assignment]):List of raw Assignment objects.

    Returns:
        List[Assignment2]: A list of transformed assignments.
    """
    assignment_2 = []
    if assignments is None:
        return []
    for a in assignments:
        assignment_2.append(build_assignment_2(a))
    return assignment_2
