import datetime as dt
import calendar
from collections import defaultdict


def generate_events(year=2025):
    """Generate FX economic indicator events for the given year."""
    events = []

    # Monthly CPI around 20th
    for month in range(1, 13):
        events.append({"name": "CPI", "date": dt.date(year, month, 20), "category": "monthly"})

    # Quarterly GDP at end of Feb, May, Aug, Nov
    for m in [2, 5, 8, 11]:
        last_day = calendar.monthrange(year, m)[1]
        events.append({"name": "GDP", "date": dt.date(year, m, last_day), "category": "non-monthly"})

    # BoJ Policy Rate decisions
    for m in [1, 3, 6, 7, 10, 12]:
        events.append({"name": "BoJ Policy Rate", "date": dt.date(year, m, 15), "category": "non-monthly"})

    return events


def print_reminders(events):
    """Print reminders for events happening tomorrow."""
    today = dt.date.today()
    tomorrow = today + dt.timedelta(days=1)
    for ev in events:
        if ev["date"] == tomorrow:
            print(f"Reminder: {ev['name']} is released tomorrow ({tomorrow})")


def export_to_ics(events, filename="fx_events.ics"):
    """Export events to a simple iCalendar file."""
    with open(filename, "w") as f:
        f.write("BEGIN:VCALENDAR\nVERSION:2.0\n")
        for ev in events:
            d = ev['date'].strftime('%Y%m%d')
            f.write("BEGIN:VEVENT\n")
            f.write(f"SUMMARY:{ev['name']}\n")
            f.write(f"DTSTART;VALUE=DATE:{d}\n")
            f.write(f"DTEND;VALUE=DATE:{d}\n")
            f.write("END:VEVENT\n")
        f.write("END:VCALENDAR\n")


def generate_html_calendar(events, year=2025, filename="fx_calendar.html"):
    """Generate an HTML calendar with events color-coded."""
    event_map = defaultdict(list)
    for ev in events:
        event_map[ev['date']].append(ev)

    style = (
        '<style>'
        'table {border-collapse: collapse; margin-bottom: 30px;}'
        'th, td {border: 1px solid #999; padding: 5px; text-align: left;}'
        '.monthly {background-color: lightblue;}'
        '.non-monthly {background-color: lightcoral;}'
        '</style>'
    )

    html = [f'<html><head>{style}</head><body>']
    for month in range(1, 13):
        html.append(f'<h2>{year} {calendar.month_name[month]}</h2>')
        html.append('<table>')
        html.append('<tr>' + ''.join(f'<th>{d}</th>' for d in calendar.day_abbr) + '</tr>')
        month_days = calendar.monthcalendar(year, month)
        for week in month_days:
            html.append('<tr>')
            for day in week:
                if day == 0:
                    html.append('<td></td>')
                    continue
                date = dt.date(year, month, day)
                day_events = event_map.get(date, [])
                if day_events:
                    names = '<br>'.join(ev['name'] for ev in day_events)
                    cls = 'monthly' if any(ev['category'] == 'monthly' for ev in day_events) else 'non-monthly'
                    html.append(f'<td class="{cls}">{day}<br>{names}</td>')
                else:
                    html.append(f'<td>{day}</td>')
            html.append('</tr>')
        html.append('</table>')
    html.append('</body></html>')

    with open(filename, 'w') as f:
        f.write('\n'.join(html))


if __name__ == "__main__":
    events = generate_events()
    print_reminders(events)
    generate_html_calendar(events)
    export_to_ics(events)
