from typing import List
import os
import yaml
import re

from models import Event, Period, Build

FINALIZED_PERIOD = re.compile(r"^\d{4}-.*$")


def load_event(event_path: str) -> Event:
    """
    """
    with open(os.path.join(event_path, "event.yaml"), "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return Event(
            id=data["id"],
            title=data["title"].strip(),
            overview=data["overview"].strip(),
        )


def load_events(period_path: str) -> List[Event]:
    """
    """
    events = []

    events_path = os.path.join(period_path, "events")
    if not os.path.exists(events_path):
        return events

    for data in os.listdir(events_path):
        event_path = os.path.join(events_path, data)
        if os.path.isdir(event_path):
            events.append(load_event(event_path))

    return sorted(events, key=lambda event: event.id)


def load_period(period_path: str) -> Period:
    """
    """
    events = load_events(period_path)

    return _load_period(os.path.join(period_path, "period.yaml"), events)


def _load_period(full_period_path: str, events) -> Period:
    with open(full_period_path, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return Period(
            id=data["id"],
            title=data["title"].strip(),
            overview=data["overview"].strip(),
            events=events,
        )


def load_periods(build_path: str) -> List[Period]:
    """
    """
    periods = []

    periods_path = os.path.join(build_path, "periods")
    for period in os.listdir(periods_path):
        period_path = os.path.join(periods_path, period)
        if os.path.isdir(period_path) and FINALIZED_PERIOD.match(period):
            periods.append(load_period(period_path))

    return sorted(periods, key=lambda period: period.id)


def load_build(build_path: str) -> Build:
    """
    Main Loader
    """
    periods = load_periods(build_path)
    overview_path = os.path.join(build_path, "build.yaml")
    with open(overview_path, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return Build(
            id=data["id"],
            title=data["title"].strip(),
            overview=data["overview"].strip(),
            periods=periods,
        )
