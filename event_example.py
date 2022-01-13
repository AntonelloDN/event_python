from pydantic import BaseModel
from typing import List, Optional

# models
class EventArgs(BaseModel):
    name: Optional[str] = "Args"

class Handler(BaseModel):
    s: object
    e: EventArgs

# hook
class EventHook:
    def __init__(self):
        self._handlers = []

    def __iadd__(self, 
        handler: Handler) -> List[Handler]:
        self._handlers.append(handler)
        return self

    def __isub__(self, 
        handler: Handler) -> List[Handler]:
        if handler in self._handlers:
            self._handlers.remove(handler)
        return self

    def invoke(self, 
        obj: object, 
        e: EventArgs) -> None:
        for handler in self._handlers:
            handler(obj, e)

    def clear_hendler(self, 
        in_handler: Handler) -> None:
        for handler in self._handlers:
            if handler == in_handler:
                self -= handler

# sample class
class RacingCar(object):
    def __init__(self, 
        laps: int =10):
        self.LapCompleted = EventHook()
        self.laps = laps
        self.name = "BMW"

    def decrease_lap(self) -> None:
        if self.laps > 0:
            self.laps -= 1

if __name__ == "__main__":

    def on_first_lap_completed(s: object, 
        e: EventArgs) -> None:
        if isinstance(s, RacingCar):
            print(f'1st lap... {e.name}')
            s.decrease_lap()

    def on_second_lap_completed(s: object, 
        e: EventArgs) -> None:
        if isinstance(s, RacingCar):
            print(f'1st lap... {e.name}')
            s.decrease_lap()

    def on_third_lap_completed(s: object, 
        e: EventArgs) -> None:
        if isinstance(s, RacingCar):
            print(f'1st lap... {e.name}')
            s.decrease_lap()
    
    # create a RacingCar
    car = RacingCar(laps=5)

    # add subscribers
    car.LapCompleted += on_first_lap_completed
    car.LapCompleted += on_second_lap_completed
    car.LapCompleted += on_third_lap_completed

    # clear a subscriber
    car.LapCompleted.clear_hendler(on_third_lap_completed)

    # run the event
    car.LapCompleted.invoke(obj=car, e=EventArgs(name=car.name))

    # remove subscribers
    car.LapCompleted -= on_first_lap_completed
    car.LapCompleted -= on_second_lap_completed
    car.LapCompleted -= on_third_lap_completed

    print (f'{car.laps} laps to go!')
    # 1st lap... BMW
    # 1st lap... BMW
    # 3 laps to go!