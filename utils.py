from aeac_controls_2022.constants import COUNT_SIZE, CENTER_POS

# calculate OFF count from duty cycle and delay %
def getCounterValues(delay, dc):
    on_count = round(delay*COUNT_SIZE/100)
    off_count = on_count + round(dc*COUNT_SIZE/100)

    return on_count, off_count

def pwmToDc(range):
    return (100*(range + 1)/256)

# rescale joystick range to -1 to 1
def remap_range(vrx, vry):
    scaled_vrx = vrx*1/CENTER_POS - 1
    scaled_vry = (vry*1/CENTER_POS - 1) * -1
    return scaled_vrx, scaled_vry