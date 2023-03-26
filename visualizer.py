import dearpygui.dearpygui as dpg
import numpy as np
import math
import csv

from datetime import datetime, timedelta

date_time_str = "180919 015519"


initial_date = None
time_delta = None
time = []
power = []
with open("data.csv", newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
    i = -1
    print("Reading...")
    for row in spamreader:
        i += 1
        if i == 0:
            continue
        if initial_date is not None and time_delta is None:
            second_date = datetime.strptime(f"{row[0]} {row[1]}", "%d/%m/%Y %H:%M:%S")
            time_delta = abs((second_date - initial_date).seconds)
        if initial_date is None:
            initial_date = datetime.strptime(f"{row[0]} {row[1]}", "%d/%m/%Y %H:%M:%S")
        time.append(i)
        try:
            value = float(row[2])
        except:
            value = 0
        power.append(value)
        if i > 14400:
            break

assert initial_date is not None
assert time_delta is not None
print(time_delta)
dpg.create_context()

width = 1000
height = 500
MAX_DOTS = 10000
bottom_padding = 20
left_padding = 35
plot_height = height - bottom_padding
plot_width = width - left_padding

length = len(power)
offset = 0
last_offset = -1
max_value = np.amax(power)
is_mouse_pressed = False
previous_pos = None
resolution = max(int(length / MAX_DOTS), 1)

possible_divisions = {
    "90days": 7776000,
    "30days": 2592000,
    "10days": 864000,
    "5days": 432000,
    "day": 86400,
    "6hour": 21600,
    "3hour": 10800,
    "1hour": 3600,
    "10minutes": 600,
    "5minutes": 300,
    "1minutes": 60,
}


def clamp(min_val, max_val, value):
    return max(min_val, min(max_val, value))


def increment_offset(delta):
    global offset
    offset = clamp(0, len(power) - length, offset + delta)


def zooming(sender, app_data):
    global length, resolution
    delta_length = clamp(-length, len(power) - length, -int(length * (app_data / 10)))
    length = clamp(0, len(power), length + delta_length)
    increment_offset(-int(delta_length / 2))
    resolution = max(int(length / MAX_DOTS), 1)


def setPanning(value, pos):
    global is_mouse_pressed, previous_pos
    if value != is_mouse_pressed:
        is_mouse_pressed = value
        if is_mouse_pressed:
            previous_pos = None


def panning(sender, pos):
    global previous_pos
    if is_mouse_pressed:
        if previous_pos is not None:
            global length
            delta = previous_pos - int(pos[0])
            proportion_of_screen = delta / plot_width
            increment_offset(int(proportion_of_screen * length))
        previous_pos = int(pos[0])


with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=zooming)
    dpg.add_mouse_drag_handler(callback=lambda sender, pos: setPanning(True, pos))
    dpg.add_mouse_release_handler(callback=lambda: setPanning(False, None))
    dpg.add_mouse_move_handler(callback=panning)


dpg.create_viewport(title="Custom Title", width=width, height=height + 200)
dpg.setup_dearpygui()
dpg.show_viewport()

TARGET_NUMBER_OF_DIVISIONS = 10

while dpg.is_dearpygui_running():
    if last_offset != offset:
        last_offset = offset
        with dpg.window(label="Tutorial"):
            with dpg.drawlist(width=width, height=height):
                plot = power[offset : offset + length]
                plot = (
                    np.average(
                        np.reshape(
                            plot[: int(length / resolution) * resolution],
                            (
                                int(length / resolution),
                                resolution,
                            ),
                        ),
                        axis=1,
                    )
                    .astype(int)
                    .tolist()
                )
                if len(plot) == 0:
                    continue
                last_value = 0.0

                x_delta = plot_width / len(plot)
                y_delta = plot_height / max_value
                for i, value in enumerate(plot):
                    if i > 0:
                        dpg.draw_line(
                            (
                                left_padding + (i - 1) * x_delta,
                                plot_height - last_value * y_delta,
                            ),
                            (left_padding + i * x_delta, plot_height - value * y_delta),
                            color=(255, 0, 0, 255),
                            thickness=1,
                        )
                    last_value = value

                # Drawing horizontal legend
                dpg.draw_line(
                    (left_padding, plot_height),
                    (left_padding + plot_width, plot_height),
                    color=(0, 255, 0, 255),
                    thickness=1,
                )
                initial_date_with_offset = initial_date + timedelta(
                    0, offset * time_delta
                )
                previous_division = None
                previous_value = None
                for _, value in possible_divisions.items():
                    division = length / (value / time_delta)
                    if division > TARGET_NUMBER_OF_DIVISIONS:
                        break
                    previous_value = value
                    previous_division = division

                if previous_division is not None:
                    if abs(division - TARGET_NUMBER_OF_DIVISIONS) > abs(
                        previous_division - TARGET_NUMBER_OF_DIVISIONS
                    ):
                        value = previous_value

                plot_value = value / time_delta
                dates = []
                total = 0
                i = 0
                previous_day = initial_date_with_offset.replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                seconds_since_beginning_of_day = (
                    initial_date_with_offset - previous_day
                ).total_seconds()
                legend_offset = value - (seconds_since_beginning_of_day % value)
                first_date = previous_day + timedelta(
                    0,
                    seconds_since_beginning_of_day + legend_offset,
                )

                while total + plot_value < length:
                    dates.append(first_date + timedelta(0, i * value))
                    total += plot_value
                    i += 1
                date_span = dates[len(dates) - 1] - dates[0]

                legend_offset_adjusted = (
                    left_padding + ((legend_offset / time_delta) / length) * plot_width
                )
                increment = length / plot_value
                for i in range(len(dates)):
                    dpg.draw_line(
                        (
                            legend_offset_adjusted + i * plot_width / increment,
                            plot_height - 5,
                        ),
                        (
                            legend_offset_adjusted + i * plot_width / increment,
                            plot_height + 5,
                        ),
                        color=(0, 255, 0, 255),
                        thickness=1,
                    )
                    if i == 0 or date_span.days > 0:
                        date = (
                            dates[i].strftime("%d/%m %H")
                            if dates[i].hour > 0
                            else dates[i].strftime("%d/%m")
                        )
                    else:
                        date = dates[i].strftime("%H:%M")
                    dpg.draw_text(
                        (
                            legend_offset_adjusted + i * plot_width / increment,
                            plot_height + 7,
                        ),
                        date,
                        color=(250, 250, 250, 255),
                        size=13,
                    )

                # Drawing vertical legend
                vertical_legend_center = left_padding - 5
                dpg.draw_line(
                    (vertical_legend_center, 0),
                    (vertical_legend_center, plot_height),
                    color=(0, 255, 0, 255),
                    thickness=1,
                )
                for i in range(math.ceil(max_value)):

                    dpg.draw_line(
                        (
                            vertical_legend_center - 5,
                            plot_height - (plot_height * i / 10),
                        ),
                        (
                            vertical_legend_center + 5,
                            plot_height - (plot_height * i / 10),
                        ),
                        color=(0, 255, 0, 255),
                        thickness=1,
                    )
                    dpg.draw_text(
                        (
                            5,
                            plot_height - (plot_height * i / 10),
                        ),
                        math.ceil(max_value) * i / math.ceil(max_value),
                        color=(250, 250, 250, 255),
                        size=13,
                    )

    dpg.render_dearpygui_frame()

dpg.destroy_context()
