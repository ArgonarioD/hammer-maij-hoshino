def format_local_date_time(time) -> str:
    if len(time) < 6:
        time.append(0)
    # return f'{(24 if time[3] <= 4 else 0) + time[3]}:{time[4]:02}:{time[5]:02}'
    return f'{time[0]}年{time[1]}月{time[2]}日 {time[3]}:{time[4]:02}:{time[5]:02}'
