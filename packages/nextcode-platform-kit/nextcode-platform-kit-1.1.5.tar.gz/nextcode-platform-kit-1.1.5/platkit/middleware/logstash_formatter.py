"""
This library is provided to allow standard python
logging to output log data as JSON formatted strings
ready to be shipped out to logstash.

WUXI: Grabbed from here: https://github.com/ulule/python-logstash-formatter
      Replacing copy() with deepcopy() on defaults because of incorrect
      log output
"""
import logging
import socket
import datetime
import traceback as tb
import json
from copy import deepcopy


def _default_json_default(obj):
    """
    Coerce everything to strings.
    All objects representing time get output as ISO8601.
    """
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    else:
        return str(obj)


class LogstashFormatterV1(logging.Formatter):
    """
    A custom formatter to prepare logs to be
    shipped out to logstash V1 format.
    """

    def __init__(
        self, fmt=None, datefmt=None, style="%", json_cls=None, json_default=_default_json_default
    ):
        """
        :param fmt: Config as a JSON string, allowed fields;
               extra: provide extra fields always present in logs
               source_host: override source host name
        :param datefmt: Date format to use (required by logging.Formatter
            interface but not used)
        :param json_cls: JSON encoder to forward to json.dumps
        :param json_default: Default JSON representation for unknown types,
                             by default coerce everything to a string
        """

        if fmt is not None:
            self._fmt = json.loads(fmt)
        else:
            self._fmt = {}
        self.json_default = json_default
        self.json_cls = json_cls
        if "extra" not in self._fmt:
            self.defaults = {}
        else:
            self.defaults = self._fmt["extra"]
        if "source_host" in self._fmt:
            self.source_host = self._fmt["source_host"]
        else:
            try:
                self.source_host = socket.gethostname()
            except:
                self.source_host = ""

    def format(self, record):
        """
        Format a log record to JSON, if the message is a dict
        assume an empty message and use the dict as additional
        fields.
        """
        fields = record.__dict__.copy()

        if "msg" in fields and isinstance(fields["msg"], dict):
            msg = fields.pop("msg")
            fields.update(msg)

        elif "msg" in fields and "message" not in fields:
            msg = record.getMessage()
            fields.pop("msg")

            try:
                msg = msg.format(**fields)
            except (KeyError, IndexError):
                pass
            except:
                # in case we can not format the msg properly we log it as is instead of crashing
                msg = msg
            fields["message"] = msg

        if "exc_info" in fields:
            if fields["exc_info"]:
                formatted = tb.format_exception(*fields["exc_info"])
                fields["exception"] = formatted
            fields.pop("exc_info")

        if "exc_text" in fields and not fields["exc_text"]:
            fields.pop("exc_text")

        now = datetime.datetime.utcnow()
        base_log = {
            "@timestamp": now.strftime("%Y-%m-%dT%H:%M:%S")
            + ".%03d" % (now.microsecond / 1000)
            + "Z",
            "@version": 1,
            "source_host": self.source_host,
        }
        base_log.update(fields)

        #
        # wuxi: We need to deepcopy the defaults since we have subdicts
        #
        logr = deepcopy(self.defaults)
        logr.update(base_log)

        return json.dumps(logr, default=self.json_default, cls=self.json_cls)
