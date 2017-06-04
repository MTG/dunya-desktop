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


def downsample_plot(plot_array, ds_limit):
    # Decide by how much we should downsample
    """
    Downsamples the given pitch array according to the given downsample limit.
    :param plot_array: (numpy array) A sequence of pitch values
                       [440.4, 442.3, 440.0, ...]
    :param ds_limit: (int) Maximum number of samples to be plotted.
    :return: (numpy array) A sequence of pitch values
    """
    size_array = np.size(plot_array)
    ds = int(size_array / ds_limit) + 1

    if ds == 1:
        # Small enough to display with no intervention.
        return plot_array
    else:
        # Here convert data into a down-sampled array suitable for
        # visualizing. Must do this piecewise to limit memory usage.
        samples = 1 + (size_array // ds)
        visible = np.zeros(samples * 2, dtype=plot_array.dtype)
        source_ptr = 0
        target_ptr = 0

        # read data in chunks of ~1M samples
        chunk_size = (1000000 // ds) * ds
        while source_ptr < size_array - 1:
            chunk = plot_array[source_ptr:min(size_array,
                                              source_ptr+chunk_size)]
            size_chunk = np.size(chunk)
            source_ptr += size_chunk
            # reshape chunk to be integral multiple of ds
            chunk = chunk[:(size_chunk // ds) * ds].reshape(size_chunk//ds, ds)

            # compute max and min
            chunk_max = chunk.max(axis=1)
            chunk_min = chunk.min(axis=1)

            # interleave min and max into plot data to preserve
            # envelope shape
            visible[target_ptr:target_ptr + chunk.shape[0] * 2:2] = chunk_min
            visible[1+target_ptr:1+target_ptr+chunk.shape[0] * 2:2] = chunk_max
            target_ptr += chunk.shape[0] * 2
        plot_y = visible[:target_ptr]
    return plot_y
