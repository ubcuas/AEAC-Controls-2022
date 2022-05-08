# mecanum wheel control interface
import sys
sys.path.append('./aeac_controls_2022/')
from constants import ACCEL_MULTIPLIER

def setMotorTargets(left_vrx, left_vry, right_vrx, target_pololu, debug=False):
    # VRY = Throttle
    # VRX = Steering

    # set target forward/back for throttle
    target_pololu[1] -= left_vry * ACCEL_MULTIPLIER
    target_pololu[2] += left_vry * ACCEL_MULTIPLIER
    target_pololu[3] -= left_vry * ACCEL_MULTIPLIER
    target_pololu[4] -= left_vry * ACCEL_MULTIPLIER
    
    if left_vrx > 0.0:
        # move right - decrease right motors speed, increase left
        target_pololu[1] += left_vrx * ACCEL_MULTIPLIER #FR
        target_pololu[2] -= left_vrx * ACCEL_MULTIPLIER #RR
        target_pololu[3] -= left_vrx * ACCEL_MULTIPLIER #FL
        target_pololu[4] -= left_vrx * ACCEL_MULTIPLIER #RL
    if left_vrx < 0.0:
        # move left - decrease left motors speed, increase right
        target_pololu[1] += left_vrx * ACCEL_MULTIPLIER #FR
        target_pololu[2] -= left_vrx * ACCEL_MULTIPLIER #RR
        target_pololu[3] -= left_vrx * ACCEL_MULTIPLIER #FL
        target_pololu[4] -= left_vrx * ACCEL_MULTIPLIER #RL

    # DIFFERENTIAL DRIVE TEST
    # if left_vry >= 0.0:
    #     if left_vrx > 0.0:
    #         # move right - decrease right motors speed, increase left
    #         target_pololu[1] += (1.0 - left_vrx) * ACCEL_MULTIPLIER #FR
    #         target_pololu[2] -= (1.0 - left_vrx) * ACCEL_MULTIPLIER #RR
    #         target_pololu[3] -= 1.0 * ACCEL_MULTIPLIER #FL
    #         target_pololu[4] -= 1.0 * ACCEL_MULTIPLIER #RL
    #     if left_vrx < 0.0:
    #         # move left - decrease left motors speed, increase right
    #         target_pololu[1] += 1.0 * ACCEL_MULTIPLIER #FR
    #         target_pololu[2] -= 1.0 * ACCEL_MULTIPLIER #RR
    #         target_pololu[3] -= (1.0 + left_vrx) * ACCEL_MULTIPLIER #FL
    #         target_pololu[4] -= (1.0 + left_vrx) * ACCEL_MULTIPLIER #RL
    # else:
    #     if left_vrx > 0.0:
    #         # move right - decrease right motors speed, increase left
    #         target_pololu[1] += 1.0 * ACCEL_MULTIPLIER #FR
    #         target_pololu[2] -= 1.0 * ACCEL_MULTIPLIER #RR
    #         target_pololu[3] -= (1.0 - left_vrx) * ACCEL_MULTIPLIER #FL
    #         target_pololu[4] -= (1.0 - left_vrx) * ACCEL_MULTIPLIER #RL
    #     if left_vrx < 0.0:
    #         # move left - decrease left motors speed, increase right
    #         target_pololu[1] += (1.0 + left_vrx) * ACCEL_MULTIPLIER #FR
    #         target_pololu[2] -= (1.0 + left_vrx) * ACCEL_MULTIPLIER #RR
    #         target_pololu[3] -= 1.0 * ACCEL_MULTIPLIER #FL
    #         target_pololu[4] -= 1.0 * ACCEL_MULTIPLIER #RL

    return target_pololu

# def setSpinMotorTargets(trigger_l, trigger_r, target_pololu):
#     if trigger_l > 0.2:
#         print("spin left")
#         # spin left (-+-+)
#         target_pololu[1] -= trigger_l
#         target_pololu[2] += trigger_l
#         target_pololu[3] -= trigger_l
#         target_pololu[4] += trigger_l
#     elif trigger_r > 0.2:
#         print("spin right")
#         # spin left (+-+-)
#         target_pololu[1] += trigger_r
#         target_pololu[2] -= trigger_r
#         target_pololu[3] += trigger_r
#         target_pololu[4] -= trigger_r

#     return target_pololu