import datetime
import re
from typing import Callable, Dict, Optional, Union

status_emoji: Dict[str, str] = {
    "onc": "<:checkboxon:1199756987471241346>",
    "noc": "<:checkboxoff:1199756988410777610>",
    "emptyc": "<:checkboxempty:1199756989887172639>",
    "edit": "<:edit:1199769314929164319>",
    "add": "<:add:1199770854112890890>",
    "automaton": "<:bots:1241748819620659332>",
    "terminids": "<:bugs:1241748834632208395>",
    "humans": "<:superearth:1275126046869557361>",
    "illuminate": "<:squid:1274752443246448702>",
    "hdi": "<:hdi:1240695940965339136>",
    "medal": "<:Medal:1241748215087235143>",
    "req": "<:rec:1274481505611288639>",
    "credits": "<:supercredit:1274728715175067681>",
}


def default_fdt(dt: datetime.datetime, *args, **kwargs) -> str:
    """Return the ISO 8601 string representation of a datetime object."""
    return dt.isoformat()


set_fdt_callable: Callable = default_fdt


def set_fdt(func: Callable) -> None:
    """Set a custom formatting function for datetime objects."""
    global set_fdt_callable
    set_fdt_callable = func


def format_datetime(*args, **kwargs) -> str:
    """Format datetime using the currently set callable."""
    if set_fdt_callable:
        return set_fdt_callable(*args, **kwargs)
    raise RuntimeError("fdt callable is not set")


def seconds_to_time_stamp(seconds_init: Union[int, float]) -> str:
    """Convert seconds into a timestamp string of format d:h:m:s."""
    return_string = ""
    seconds_start = int(round(seconds_init))
    seconds = seconds_start % 60
    minutes_r = (seconds_start - seconds) // 60
    minutes = minutes_r % 60
    hours_r = (minutes_r - minutes) // 60
    hours = hours_r % 24
    days = (hours_r - hours) // 24
    years = days // 365
    if years > 1:
        return_string += f"{years}:"
    if days > 1:
        return_string += f"{days%365}:"
    if hours > 1:
        return_string += "{:02d}:".format(hours)
    return_string += "{:02d}:{:02d}".format(minutes, seconds)
    return return_string


def extract_timestamp(timestamp: str) -> datetime.datetime:
    """Extract datetime object from a given timestamp string."""
    try:
        # Attempt to parse using fromisoformat if it is an isoformat timestamp
        return datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        # Define the format of the timestamp string (with 7-digit fractional seconds)
        format_string = "%Y-%m-%dT%H:%M:%S.%fZ"

        # Extract the fractional seconds (up to 6 digits) and Z separately
        timestamp_parts = timestamp.split(".")
        timestamp_adjusted = timestamp
        if len(timestamp_parts) >= 2:
            timestamp_adjusted = timestamp_parts[0] + "." + timestamp_parts[1][:6]
            if not timestamp_adjusted.endswith("Z"):
                timestamp_adjusted += "Z"
        else:
            format_string = "%Y-%m-%dT%H:%M:%SZ"
            if not timestamp_adjusted.endswith("Z"):
                timestamp_adjusted += "Z"
        # Convert the adjusted timestamp string to a datetime object
        datetime_obj = datetime.datetime.strptime(timestamp_adjusted, format_string).replace(
            tzinfo=datetime.timezone.utc
        )
        return datetime_obj


def human_format(num: float) -> str:
    """Format a large number with appropriate suffixes."""
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    suffixes = ["", "K", "M", "B", "T", "Q", "Qi"]
    return "{}{}".format("{:f}".format(num).rstrip("0").rstrip("."), suffixes[magnitude])


def changeformatif(value: Optional[str]) -> str:
    """Return formatted string if value is not None or empty."""
    if value:
        return f"({value})"
    return ""


def select_emoji(key: str) -> str:
    """Select an emoji from the status emoji dictionary."""
    if key in status_emoji:
        return status_emoji.get(key)
    return status_emoji["emptyc"]


pattern = r"<i=1>(.*?)<\/i>"
pattern3 = r"<i=3>(.*?)<\/i>"


def hdml_parse(input_str: str) -> str:
    """Parse a given string to replace custom HTML-like tags."""
    mes = re.sub(pattern, r"**\1**", input_str)
    mes = re.sub(pattern3, r"***\1***", mes)
    return mes
