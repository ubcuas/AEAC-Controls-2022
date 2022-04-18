# mecanum wheel control interface

def setMotorTargets(left_vrx, left_vry, right_vrx, target_pololu, debug=False):
    # from https://www.vexforum.com/t/programming-mecanum-wheels/21606/5
    
    FLMotor = left_vry + right_vrx + left_vrx
    FRMotor = left_vry - right_vrx - left_vrx
    BLMotor = left_vry + right_vrx - left_vrx
    BRMotor = left_vry - right_vrx + left_vrx

    if debug:
        print(f"FL: {FLMotor}, FR: {FRMotor}, BL: {BLMotor}, BR: {BRMotor}")

    target_pololu[1] += FLMotor
    target_pololu[2] += FRMotor
    target_pololu[3] += BLMotor
    target_pololu[4] += BRMotor

    return target_pololu

def setSpinMotorTargets(trigger_l, trigger_r, target_pololu):
    if trigger_l > 0.2:
        print("spin left")
        # spin left (-+-+)
        target_pololu[1] -= trigger_l
        target_pololu[2] += trigger_l
        target_pololu[3] -= trigger_l
        target_pololu[4] += trigger_l
    elif trigger_r > 0.2:
        print("spin right")
        # spin left (+-+-)
        target_pololu[1] += trigger_r
        target_pololu[2] -= trigger_r
        target_pololu[3] += trigger_r
        target_pololu[4] -= trigger_r

    return target_pololu