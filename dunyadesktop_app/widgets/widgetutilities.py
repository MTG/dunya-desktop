import numpy as np


def convert_str(string):
    return u''.join(string).encode('utf-8').strip()


def set_css(widget, css_path):
    try:
        with open(css_path) as f:
            css = f.read()
        widget.setStyleSheet(css)
    except IOError:
        pass


def downsample_plot(plot_array, limit, start, stop, hop_size, fs):
    start *= 1 / (hop_size / fs)
    stop *= 1 / (128. / 44100.)
    start = int(start)
    stop = int(stop)
    # Decide by how much we should downsample
    ds = int((stop - start) / limit) + 1

    if ds == 1:
        # Small enough to display with no intervention.
        plot_y = plot_array[start:stop]
    else:
        # Here convert data into a down-sampled array suitable for
        # visualizing.
        # Must do this piecewise to limit memory usage.
        samples = 1 + ((stop - start) // ds)
        visible = np.zeros(samples * 2, dtype=plot_array.dtype)
        source_ptr = start
        target_ptr = 0

        # read data in chunks of ~1M samples
        chunk_size = (1000000 // ds) * ds
        while source_ptr < stop - 1:
            chunk = plot_array[source_ptr:min(stop, source_ptr + chunk_size)]
            source_ptr += len(chunk)

            # reshape chunk to be integral multiple of ds
            chunk = chunk[:(len(chunk) // ds) * ds].reshape(
                len(chunk) // ds, ds)

            # compute max and min
            chunk_max = chunk.max(axis=1)
            chunk_min = chunk.min(axis=1)

            # interleave min and max into plot data to preserve
            # envelope shape
            visible[target_ptr:target_ptr + chunk.shape[0] * 2:2] = chunk_min
            visible[1 + target_ptr:
            1 + target_ptr + chunk.shape[0] * 2:2] = chunk_max
            target_ptr += chunk.shape[0] * 2

        plot_y = visible[:target_ptr]
        plot_y[-1] = np.nan

    start = (start * hop_size) / fs
    stop = (stop * hop_size) / fs
    step = (stop - start) / (len(plot_y))
    plot_x = np.arange(start, stop, step)

    return plot_x, plot_y
