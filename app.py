def get_signal_time(count):

    if count < 10:
        return "LOW",20

    elif count < 30:
        return "MEDIUM",40

    else:
        return "HIGH",60