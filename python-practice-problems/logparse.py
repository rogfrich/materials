""" log parser
    Accepts a filename on the command line.  The file is a linux-like log file
    from a system you are debugging.  Mixed in among the various statements are
    messages indicating the state of the device.  They look like:
        Jul 11 16:11:51:490 [139681125603136] dut: Device State: ON
    The device state message has many possible values, but this program only
    cares about three: ON, OFF, and ERR.

    Your program will parse the given log file and print out a report giving
    how long the device was ON, and the time stamp of any ERR conditions.
"""
import datetime, unittest


def find_err_status(line, timestamp):
    if "ERR" in line:
        return f"ERROR at timestamp: {timestamp}"


def convert_string_to_date_time_obj(timestamp):
    timestamp_obj = datetime.datetime.strptime(timestamp, "%b %d %H:%M:%S:%f")
    return timestamp_obj


def calculate_uptime(on_events, off_events):
    uptime = datetime.timedelta(0)
    for on, off in zip(on_events, off_events):
        uptime += (off - on)
    return uptime


class TestLogParse(unittest.TestCase):
    def test_find_err_status(self):
        err_status = find_err_status("Jul 11 16:11:54:661 [139681125603136] dut: Device State: ERR",
                                     "Jul 11 16:11:54:661")
        self.assertEqual(err_status, "ERROR at timestamp: Jul 11 16:11:54:661")

    def test_convert_string_to_time(self):
        time = convert_string_to_date_time_obj("Jul 11 16:11:51:490")
        test_time = datetime.datetime.strptime("Jul 11 16:11:51:490", "%b %d %H:%M:%S:%f")
        self.assertEqual(time, test_time)

    def test_calculate_uptime(self):
        on = convert_string_to_date_time_obj("Jul 11 16:11:51:490")
        off = convert_string_to_date_time_obj("Jul 11 16:11:53:490")
        uptime = calculate_uptime([on], [off])
        self.assertEqual(uptime, off - on)


if __name__ == "__main__":

    with open("test.log") as fin:
        on_events = []
        off_events = []
        for line in fin.readlines():
            full_date_time_stamp = line[0:19]

            # Check whether there is an error code ("ERR") in the report line and print it if there is.
            err_status = find_err_status(line, full_date_time_stamp)
            if err_status:
                print(err_status)

            # Check if the report line is for an ON or OFF event, and build a list for each event type.

            if "Device State: ON" in line or "Device State: OFF" in line:
                datetime_obj = convert_string_to_date_time_obj(full_date_time_stamp[0:19])
                if "Device State: ON" in line:
                    on_events.append(datetime_obj)
                elif "Device State: OFF" in line:
                    off_events.append(datetime_obj)
                else:
                    print("No ON or OFF events in log file")

        uptime = calculate_uptime(on_events, off_events)
        print(f"The device was ON for: {uptime}")
