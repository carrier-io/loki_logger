import re
import logging
from typing import Iterable, Union

from centry_loki.constants import LOG_SECRETS_REPLACER, FormatterMethods, FORMATTER_METHOD, LOG_FORMAT, LOG_DATE_FORMAT


class SecretFormatter(logging.Formatter):
    REPLACER = LOG_SECRETS_REPLACER
    RESTRICTED_STOP_WORDS = {'', REPLACER}

    def __init__(self, secrets: Iterable, formatter_method: Union[FormatterMethods, str] = FORMATTER_METHOD):
        super().__init__(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        self.formatter_method = formatter_method
        self.secrets = set(map(str, secrets))
        self.__censor_stop_words()

        try:
            self.formatter = getattr(self, self.formatter_method)
        except AttributeError:
            logging.warning('Formatter method %s not found. Falling back to %s', self.formatter_method,
                            FormatterMethods.RE)
            self.formatter = self.replacer_re

    def __censor_stop_words(self) -> None:
        for i in self.RESTRICTED_STOP_WORDS:
            try:
                self.secrets.remove(i)
            except KeyError:
                ...

    @property
    def re_pattern(self):
        return re.compile(r'\b(?:{})\b'.format('|'.join(map(re.escape, self.secrets))))

    def replacer_re(self, text: str) -> str:
        # replaces only separate words
        return re.sub(self.re_pattern, self.REPLACER, text)

    def replacer_iter(self, text: str) -> str:
        # replaces every occurrence
        for i in self.secrets:
            text = text.replace(i, self.REPLACER)
        return text

    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)
        return self.formatter(formatted)

    def patch_logger(self, logger_: logging.Logger) -> None:
        for handler_ in logger_.handlers:
            if isinstance(handler_.formatter, self.__class__):
                self.secrets.update(handler_.formatter.secrets)
                self.__censor_stop_words()
            handler_.setFormatter(self)
