# python/main.py
from datetime import datetime
from commute_algorithm import CommuteAlgorithm, CommuteContext, Coordinates

def main() -> None:
    # In your real setup, you'd load this from your "brain" config.
    home = Coordinates(29.4241, -98.4936)  # example: San Antonio
    work = Coordinates(29.7604, -95.3698)  # example: Houston
    departure = datetime.now()

    commute_algo = CommuteAlgorithm()
    result = commute_algo.estimate_commute(
        CommuteContext(home=home, work=work, departure_time=departure)
    )

    print("=== Commute ===")
    print(result.note)
    print(f"Duration: {result.estimated_duration}")

    # TODO:
    # - call sleep_initiate_shutdown.run(context)
    # - call review_bills.run(context)
    # - call review_todos.run(context)
    # - etc...

if __name__ == "__main__":
    main()
