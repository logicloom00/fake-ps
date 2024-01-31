from models import SystemState


def get_system_state(request_made: int):
    desigion = {
        10: SystemState.NORMAL,
        20: SystemState.OVERLOADING,
        30: SystemState.FAILING,
        40: SystemState.UNAVAILABLE,
        50: SystemState.RECOVERING
    }
    choise = SystemState.NORMAL
    for k, v in desigion.items():
        if k > request_made:
            choise = v
            break
    return choise
