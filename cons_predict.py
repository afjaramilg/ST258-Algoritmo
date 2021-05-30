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



consumo_por_hora = obtener_consumo(individuo) 
score = 0
use = 0  

for h in 0..24:
    if consumo_por_hora[h] > 0:
        score += PRODUCCION_POR_HORA[h] / consumo_por_hora[h]  
        use += 1

return (score / 24) + (use / 24)