# -*- coding: utf-8 -*-

import datetime

import typing

from mehdi_lib.tools import tools


# ===========================================================================
class Shamsi:
    # ===========================================================================
    weekday_names = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']
    days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    month_names = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان',
                   'آذر', 'دی', 'بهمن', 'اسفند']

    # ===========================================================================
    @staticmethod
    def from_gregorian(date_time: datetime.datetime) -> 'ShamsiDate':
        [year, month, day] = [date_time.year, date_time.month, date_time.day]

        # Convert date to Jalali
        d_4 = year % 4
        g_a = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        doy_g = g_a[month] + day
        if d_4 == 0 and month > 2:
            doy_g += 1
        d_33 = int(((year - 16) % 132) * .0305)
        a = 286 if (d_33 == 3 or d_33 < (d_4 - 1) or d_4 == 0) else 287
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 10) / 63) == 30:
            a -= 1
            b += 1
        if doy_g > b:
            jy = year - 621
            doy_j = doy_g - b
        else:
            jy = year - 622
            doy_j = doy_g + a
        if doy_j < 187:
            jm = int((doy_j - 1) / 31)
            jd = doy_j - (31 * jm)
            jm += 1
        else:
            jm = int((doy_j - 187) / 30)
            jd = doy_j - 186 - (jm * 30)
            jm += 7

        return ShamsiDate(jy, jm, jd)

    # ===========================================================================
    @staticmethod
    def today():
        return Shamsi.from_gregorian(datetime.datetime.today())

    # ===========================================================================
    @staticmethod
    def month_begin(year: int, month: int) -> 'ShamsiDate':
        return ShamsiDate(year, month, 1)

    # ===========================================================================
    @staticmethod
    def month_end(year: int, month: int) -> 'ShamsiDate':
        if year < 0:
            tools.Tools.warning('year is not acceptable {}'.format(year))
            # noinspection PyTypeChecker
            return None
        if not (1 <= month <= 12):
            tools.Tools.warning('month is not acceptable {}'.format(month))
            # noinspection PyTypeChecker
            return None
        if 1 <= month <= 6:
            return ShamsiDate(year, month, 31)
        if 7 <= month <= 11:
            return ShamsiDate(year, month, 30)
        if month == 12:
            if Shamsi.is_leap(year):
                return ShamsiDate(year, month, 30)
            else:
                return ShamsiDate(year, month, 29)

    # ===========================================================================
    @staticmethod
    def month_days_separated_by_weekdays(year: int, month: int, reverse: bool = False) -> typing.Dict[int, int]:
        # beginning and end of the month
        month_begin = Shamsi.month_begin(year, month)
        month_end = Shamsi.month_end(year, month)
        # initialize the dict
        days_separated_by_weekdays = dict()
        for weekday in range(7):
            days_separated_by_weekdays[weekday] = []
        # fill incipient days of the week with None
        for weekday in range(0, month_begin.weekday()):
            days_separated_by_weekdays[weekday].append(None)
        # start filling days
        for day in range(month_begin.day - 1, month_end.day):
            weekday = (month_begin.weekday() + day) % 7
            days_separated_by_weekdays[weekday].append(day + 1)
        # fill ending days of the week with None
        day = month_end.day
        while True:
            weekday = (month_begin.weekday() + day) % 7
            # any days remained in the last week?
            if weekday > 0:
                days_separated_by_weekdays[weekday].append(None)
                day += 1
            # ok nothing else
            else:
                break
        if reverse:
            reversed_days = dict()
            for weekday in days_separated_by_weekdays:
                reversed_days[len(days_separated_by_weekdays) - weekday - 1] = days_separated_by_weekdays[weekday]
            return reversed_days
        return days_separated_by_weekdays

    # ===========================================================================
    @staticmethod
    def is_leap(year) -> bool:
        return year % 33 in (1, 5, 9, 13, 17, 22, 26, 30)

    # ===========================================================================
    @staticmethod
    def is_valid(year, month, day):
        # check year
        if year <= 0:
            return False
        # check month
        if not (1 <= month <= 12):
            return False
        # check day
        if (day < 1) or (day > 31) or \
                (month > 6 and day > 30) or \
                (month == 12 and day > 29 and not Shamsi.is_leap(year)):
            return False

        return True

    # ===========================================================================
    @staticmethod
    def force_a_date(year: int, month: int, day: int):
        # first correct totally invalid values
        if year < 1:
            year = 1
        if month < 1:
            month = 1
        if month > 12:
            month = 12
        if day < 1:
            day = 1
        # first six months
        if month < 7 and day > 31:
            day = 31
        # second five months
        elif month < 12 and day > 30:
            day = 30
        # now the last month
        elif Shamsi.is_leap(year):
            if day > 30:
                day = 30
        elif day > 29:
            day = 29

        return ShamsiDate(year, month, day)


# ===========================================================================
class ShamsiDate(Shamsi):
    # ===========================================================================
    def __init__(self, year, month, day):

        # check and set year
        if year <= 0:
            raise ValueError('year is not acceptable {}'.format(month))
        self.year = year

        # check and set month
        if not (1 <= month <= 12):
            raise ValueError('month is not acceptable {}'.format(month))
        self.month = month

        # check and set day
        if (day < 1) or (day > 31) or \
                (month > 6 and day > 30) or \
                (month == 12 and day > 29 and not Shamsi.is_leap(year)):
            raise ValueError('day is not acceptable {}'.format(day))
        self.day = day

    # ===========================================================================
    def to_gregorian(self) -> datetime.datetime:
        # Check validity of date. TODO better check (leap years)

        if self.year < 1 or self.month < 1 or self.month > 12 or self.day < 1 or self.day > 31 or (
                self.month > 6 and self.day == 31):
            raise Exception("Incorrect Date")

        # Convert date
        d_4 = (self.year + 1) % 4
        if self.month < 7:
            doy_j = ((self.month - 1) * 31) + self.day
        else:
            doy_j = ((self.month - 7) * 30) + self.day + 186
        d_33 = int(((self.year - 55) % 132) * .0305)
        a = 287 if (d_33 != 3 and d_4 <= d_33) else 286
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((self.year - 19) / 63) == 20:
            a -= 1
            b += 1
        if doy_j <= a:
            gy = self.year + 621
            gd = doy_j + b
        else:
            gy = self.year + 622
            gd = doy_j - a
        gm = 0
        for gm, v in enumerate([0, 31, 29 if (gy % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
            if gd <= v:
                break
            gd -= v

        return datetime.datetime(gy, gm, gd)

    # ===========================================================================
    # noinspection PyMethodOverriding
    def month_begin(self) -> 'ShamsiDate':
        return Shamsi.month_begin(self.year, self.month)

    # ===========================================================================
    # noinspection PyMethodOverriding
    def month_end(self) -> 'ShamsiDate':
        return Shamsi.month_end(self.year, self.month)

    # ===========================================================================
    def is_leap(self) -> bool:
        return Shamsi.is_leap(self.year)

    # ===========================================================================
    def weekday(self) -> int:
        return (self.to_gregorian().weekday() + 2) % 7

    # ===========================================================================
    # noinspection PyMethodOverriding
    def month_days_separated_by_weekdays(self, reverse: bool = False) -> typing.Dict[int, int]:
        return Shamsi.month_days_separated_by_weekdays(self.year, self.month, reverse=reverse)

    # ===========================================================================
    def weekday_name(self) -> str:
        return Shamsi.weekday_names[self.weekday()]

    # ===========================================================================
    def month_name(self) -> str:
        return Shamsi.month_names[self.month - 1]

    # ===========================================================================
    def next_month(self) -> 'ShamsiDate':
        if self.month == 12:
            return ShamsiDate(self.year + 1, 1, self.day)
        if self.month == 11:
            if self.day <= 29 or self.is_leap():
                return ShamsiDate(self.year, 12, self.day)
            else:
                return ShamsiDate(self.year, 12, 29)
        if self.month == 6 and self.day == 31:
            return ShamsiDate(self.year, 7, 30)
        return ShamsiDate(self.year, self.month + 1, self.day)

    # ===========================================================================
    def previous_month(self) -> 'ShamsiDate':
        if self.month == 1:
            if self.year > 1:
                if self.day <= 29:
                    return ShamsiDate(self.year - 1, 12, self.day)
                if Shamsi.is_leap(self.year - 1):
                    return ShamsiDate(self.year - 1, 12, 30)
                else:
                    return ShamsiDate(self.year - 1, 12, 29)
            else:
                # noinspection PyTypeChecker
                return None
        return ShamsiDate(self.year, self.month - 1, self.day)


class Date:
    # ===========================================================================
    @staticmethod
    def is_same_day(d1: datetime.date, d2: datetime.date):
        if d1.year == d2.year and d1.month == d2.month and d1.day == d2.day:
            return True
        return False

    # ===========================================================================
    @staticmethod
    def combine_time_to_minutes(days: int, hours: int, minutes: int) -> int:
        return days * 24 * 60 + hours * 60 + minutes

    # ===========================================================================
    @staticmethod
    def split_deltatime_to_days_hours_minutes(t: datetime.timedelta) -> (int, int, int):
        total_minutes = int(t.total_seconds() / 60)
        days = int(total_minutes // (24 * 60))
        hours = int(total_minutes // 60 - days * 24)
        minutes = int(total_minutes - days * 24 * 60 - hours * 60)

        return days, hours, minutes

    # ===========================================================================
    @staticmethod
    def convert_duration_to_text(t: datetime.timedelta) -> str:
        days, hours, minutes = Date.split_deltatime_to_days_hours_minutes(t)

        if days == 0:
            return str(hours) + ":" + str(minutes)

        return str(days) + ":" + str(hours) + ":" + str(minutes)
