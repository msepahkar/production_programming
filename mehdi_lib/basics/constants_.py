# -*- coding: utf-8 -*-

from PyQt5 import QtGui

import datetime


# ===========================================================================
class Constants:
    max_expert_level = 10

    MAX_INT = 2147483647

    # ===========================================================================
    # CREATING OUTPUT
    # ===========================================================================
    # pens
    SOL_PEN = QtGui.QPen(QtGui.QColor("black"))

    # constants for graphic output
    OPERATION_WIDTH_TO_REQUIRED_TIME = 1
    HORIZONTAL_MARGIN = 10 * OPERATION_WIDTH_TO_REQUIRED_TIME
    VERTICAL_MARGIN = 10 * OPERATION_WIDTH_TO_REQUIRED_TIME
    DAY_TITLE_WIDTH = 50 * OPERATION_WIDTH_TO_REQUIRED_TIME
    DAY_TITLE_HEIGHT = 10 * OPERATION_WIDTH_TO_REQUIRED_TIME
    TIME_AXIS_HEIGHT = 10 * OPERATION_WIDTH_TO_REQUIRED_TIME
    PART_TITLE_HEIGHT = 50 * OPERATION_WIDTH_TO_REQUIRED_TIME
    PART_VERTICAL_DISTANCE = 10 * OPERATION_WIDTH_TO_REQUIRED_TIME
    PART_HORIZONTAL_DISTANCE = 50 * OPERATION_WIDTH_TO_REQUIRED_TIME
    OPERATION_RECT_HEIGHT = 60 * OPERATION_WIDTH_TO_REQUIRED_TIME
    ZERO_TIME_OPERATION_LABEL_WIDTH = 50 * OPERATION_WIDTH_TO_REQUIRED_TIME

    NORMAL_FONT_SIZE = 10 * OPERATION_WIDTH_TO_REQUIRED_TIME

    ZERO_TIME_OPERATION_LABEL_FONT_PEN = QtGui.QPen(QtGui.QColor('white'))
    ZERO_TIME_JOB_BACKGROUND_BRUSH = QtGui.QBrush(QtGui.QColor("gray"))
    IDLE_PERIOD_BACKGROUND_BRUSH = QtGui.QBrush(QtGui.QColor("gray"))

    # fonts
    OPERATION_FONT_PEN = QtGui.QPen(QtGui.QColor('black'))
    OPERATION_FONT_BRUSH = QtGui.QBrush(QtGui.QColor('black'))
    OPERATION_FONT = QtGui.QFont("XB Niloofar", NORMAL_FONT_SIZE)
    OPERATION_X_BORDER = 5 * OPERATION_WIDTH_TO_REQUIRED_TIME
    OPERATION_Y_BORDER = 5 * OPERATION_WIDTH_TO_REQUIRED_TIME
    OPERATION_NAME_HEIGHT = 10 * OPERATION_WIDTH_TO_REQUIRED_TIME
    OPERATION_TIME_HEIGHT = 10 * OPERATION_WIDTH_TO_REQUIRED_TIME

    RESOURCE_FONT_PEN = QtGui.QPen(QtGui.QColor('black'))
    RESOURCE_FONT_BRUSH = QtGui.QBrush(QtGui.QColor('black'))
    RESOURCE_FONT = QtGui.QFont("XB Niloofar", NORMAL_FONT_SIZE)
    RESOURCE_BACKGROUND_BRUSH = QtGui.QBrush(QtGui.QColor("gray"))

    PART_TITLE_FONT_PEN = QtGui.QPen(QtGui.QColor('white'))
    PART_TITLE_FONT_BRUSH = QtGui.QBrush(QtGui.QColor('white'))
    PART_TITLE_FONT = QtGui.QFont("XB Niloofar", NORMAL_FONT_SIZE)
    PART_TITLE_BACKGROUND_BRUSH = QtGui.QBrush(QtGui.QColor("gray"))
    PART_TITLE_X_BORDER = 5 * OPERATION_WIDTH_TO_REQUIRED_TIME
    PART_TITLE_Y_BORDER = 5 * OPERATION_WIDTH_TO_REQUIRED_TIME

    DAY_TITLE_FONT_PEN = QtGui.QPen(QtGui.QColor('black'))
    DAY_TITLE_FONT = QtGui.QFont("XB Niloofar", NORMAL_FONT_SIZE)

    # palette for specialties
    SPECIALTY_BRUSH_PALETTE = [QtGui.QBrush(QtGui.QColor("red")),
                               QtGui.QBrush(QtGui.QColor("blue")),
                               QtGui.QBrush(QtGui.QColor("yellow")),
                               QtGui.QBrush(QtGui.QColor("cyan")),
                               QtGui.QBrush(QtGui.QColor("magenta")),
                               QtGui.QBrush(QtGui.QColor("green"))]

    # thresholds
    MIN_REQUIRED_MINUTES_FOR_AVAILABILITY = 5

    # time
    MAX_DATE_TIME = datetime.datetime(datetime.MAXYEAR, 1, 1)
    MAX_DATE = datetime.date(datetime.MAXYEAR, 1, 1)
    ZERO_DURATION = datetime.timedelta(0)
