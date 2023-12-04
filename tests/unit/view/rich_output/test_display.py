from crm.view.cli.terminal.display import console, display_panel, display_table, notification
from crm.view.log import LogStatus


def test_display_table():
    title = "title test"
    data = [{"ID": "1", "Full name": "John Doe"}, {"ID": "2", "Full name": "Monique Tesla"}]
    with console.capture() as capture:
        display_table(colors={}, title=title, data=data)
    to_find = [key for key in data[0].keys()]
    to_find.append(title)
    to_find.extend([value for i in range(len(data)) for value in data[i].values()])
    for item in to_find:
        assert item in capture.get()


def test_display_panel():
    title = "title test"
    data = {"ID": "1", "Full name": "John Doe"}
    subtitle = "subtitle test"
    with console.capture() as capture:
        display_panel(colors={}, title=title, data=data, subtitle=subtitle, focus=None)
    to_find = [key for key in data.keys()]
    to_find.append(title)
    to_find.append(subtitle)
    to_find.extend([value for value in data.values()])
    for item in to_find:
        assert item in capture.get()


def test_notification():
    message = "message test"
    with console.capture() as capture:
        notification(status=LogStatus.INFO, message=message)
    assert message in capture.get()
    assert "✅ " in capture.get()
    with console.capture() as capture:
        notification(status=LogStatus.WARNING, message=message)
    assert message in capture.get()
    assert "⚠️ " in capture.get()
