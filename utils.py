from models import SystemState


def get_system_state(request_made: int):
    desigion = {
        5: SystemState.NORMAL,
        10: SystemState.OVERLOADING,
        15: SystemState.FAILING,
        20: SystemState.UNAVAILABLE,
        25: SystemState.RECOVERING
    }
    choise = SystemState.NORMAL
    for k, v in desigion.items():
        if k > request_made:
            choise = v
            break
    return choise
