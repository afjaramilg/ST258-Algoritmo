import dev_info as di


def get_hourly_cons(sol):
    hour = 0
    retval = [0] * 24

    for hour in range(24):
        ind = di.DEVICES_PER_HOUR * hour
        for i in range(di.DEVICES_PER_HOUR):
            dev = int(sol[ind + i])
            retval[hour] += di.KW_DEVICES[dev]
        
    return retval
