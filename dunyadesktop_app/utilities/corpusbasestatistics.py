import pyqtgraph as pg
import numpy as np

from cultures.makam.utilities import sort_dictionary

_NUM_CENTS_IN_OCTAVE = 1200.0


class Converter(object):
    @staticmethod
    def hz_to_cent(hz_track, ref_freq, min_freq=20.0):
        """--------------------------------------------------------------------
        Converts an array of Hertz values into cents.
        -----------------------------------------------------------------------
        hz_track : The 1-D array of Hertz values
        ref_freq : Reference frequency for cent conversion
        min_freq : The minimum frequency allowed (exclusive)
        --------------------------------------------------------------------"""
        # The 0 Hz values are removed, not only because they are meaningless,
        # but also logarithm of 0 is problematic.
        assert min_freq >= 0.0, 'min_freq cannot be less than 0'

        hz_track = np.array(hz_track).astype(float)

        # change values less than the min_freq to nan
        hz_track[hz_track <= min_freq] = np.nan

        return np.log2(hz_track / ref_freq) * _NUM_CENTS_IN_OCTAVE

    @staticmethod
    def cent_to_hz(cent_track, ref_freq):
        """--------------------------------------------------------------------
        Converts an array of cent values into Hertz.
        -----------------------------------------------------------------------
        cent_track  : The 1-D array of cent values
        ref_freq    : Reference frequency for cent conversion
        --------------------------------------------------------------------"""
        cent_track = np.array(cent_track).astype(float)

        return 2 ** (cent_track / _NUM_CENTS_IN_OCTAVE) * ref_freq


def compute_overall_histogram(histograms):
    values = {}
    tonic = {}
    bins_in_cent = {}
    new_x_axis_in_cent = {}
    interpolated_values = {}
    curves = {}

    min_bin_value = 0
    max_bin_value = 0

    for mbid in histograms:
        print("Curves: ", mbid)
        # translate histogram in cent
        values[mbid] = histograms[mbid][0][0]
        tonic[mbid] = histograms[mbid][1]
        bins_in_cent[mbid] = Converter.hz_to_cent(histograms[mbid][0][1], tonic[mbid])

        # update the overall minimum and maximum bounds in cents
        if int(bins_in_cent[mbid][0]) < min_bin_value:
            min_bin_value = int(bins_in_cent[mbid][0])

        if int(bins_in_cent[mbid][-1]) > max_bin_value:
            max_bin_value = int(bins_in_cent[mbid][-1])

        print("Min: ", int(bins_in_cent[mbid][0]))
        print("Max: ", int(bins_in_cent[mbid][-1]))

        # create the new x axis interval in cent for every function
        new_x_axis_in_cent[mbid] = range(int(bins_in_cent[mbid][0]), int(bins_in_cent[mbid][-1]), 1)
        print("New x: ", new_x_axis_in_cent[mbid])

        # use interpolation to find all the values on the new x axis
        interpolated_values[mbid] = np.interp(new_x_axis_in_cent[mbid], bins_in_cent[mbid], values[mbid])

        # create a dictionary for the curves
        curves[mbid] = dict(zip(new_x_axis_in_cent[mbid], interpolated_values[mbid]))

    overall_x = range(min_bin_value, max_bin_value)
    overall_y = np.zeros(max_bin_value - min_bin_value)

    overall_hist = dict(zip(overall_x, overall_y))

    for mbid in curves:
        for key in curves[mbid]:
            overall_hist[key] += curves[mbid][key]

    print("Results")
    print("Min: ", min_bin_value)
    print("Max: ", max_bin_value)

    plot_bins = list(overall_hist.keys())
    plot_vals = [overall_hist[key] for key in plot_bins]

    pg.plot(plot_bins, plot_vals)


# def compute_overall_histogram(histograms):
#     overall_hist = {}
#     values = {}
#     bins = {}
#     tonic = {}
#
#     min_bin_value = 0
#     max_bin_value = 0
#
#     for mbid in histograms:
#         values[mbid] = histograms[mbid][0][0]
#         bins[mbid] = histograms[mbid][0][1]
#         tonic[mbid] = histograms[mbid][1]
#
#     # find the minimum and maximum bounds in cents
#     for mbid in bins:
#
#         temp_bounds = [bins[mbid][0], bins[mbid][-1]]
#         cent_temp_bounds = Converter.hz_to_cent(temp_bounds, tonic)
#
#         if cent_temp_bounds[0] < min_bin_value:
#             min_bin_value = cent_temp_bounds[0]
#
#         if cent_temp_bounds[1] > max_bin_value:
#             max_bin_value = cent_temp_bounds[1]
#
#     # create the x-axis array
#     x = arange(min_bin_value, max_bin_value, 1)
#
#
#
#
#     plot_bins = sorted(overall_hist.keys())
#     plot_vals = [overall_hist[key] for key in plot_bins]
#
#     pg.plot(plot_bins, plot_vals)
#
#     # for mbid in histograms:
#     #     valley = histograms[mbid][0][0]
#     #     bins = histograms[mbid][0][1]
#     #     tonic = histograms[mbid][1]
#     #
#     #     for ii in range(len(bins)):
#     #         cent_bin = Converter.hz_to_cent(bins[ii], tonic)[0]
#     #         #cent_bin.astype(int)
#     #
#     #         try:
#     #             overall_hist[cent_bin] = overall_hist[cent_bin] + valley[ii]
#     #         except KeyError:
    #             overall_hist[cent_bin] = valley[ii]
