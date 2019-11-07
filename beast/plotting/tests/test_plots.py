import matplotlib.pyplot as plt

import os.path
import pytest

import numpy as np
from astropy.table import Table
from astropy.io import fits
from astropy.utils.data import download_file
from astropy.tests.helper import remote_data

from matplotlib.testing.decorators import image_comparison

from beast.plotting import plot_indiv_fit, plot_cmd, plot_cmd_with_fits, plot_filters

plt.switch_backend("agg")

def _download_rename(filename):
    """
    Download a file and rename it to have the right extension

    Otherwise, downloaded file will not have an extension at all
    """
    url_loc = "http://www.stsci.edu/~kgordon/beast/"
    fname_dld = download_file("%s%s" % (url_loc, filename))
    extension = filename.split(".")[-1]
    fname = "%s.%s" % (fname_dld, extension)
    os.rename(fname_dld, fname)
    return fname

@remote_data
@pytest.mark.mpl_image_compare(tolerance=25)
def test_indiv_plot():

    # download cached version of fitting results
    stats_fname_cache = _download_rename("beast_example_phat_stats.fits")
    pdf1d_fname_cache = _download_rename("beast_example_phat_pdf1d.fits")

    # results_dir = '../../examples/phat_small/beast_example_phat/'
    # stats_fname_cache = results_dir + 'beast_example_phat_stats.fits'
    # pdf1d_fname_cache = results_dir + 'beast_example_phat_pdf1d.fits'

    starnum = 0

    # read in the stats
    stats = Table.read(stats_fname_cache)
    # open 1D PDF file
    pdf1d_hdu = fits.open(pdf1d_fname_cache)

    filters = [
        "HST_WFC3_F275W",
        "HST_WFC3_F336W",
        "HST_ACS_WFC_F475W",
        "HST_ACS_WFC_F814W",
        "HST_WFC3_F110W",
        "HST_WFC3_F160W",
    ]
    waves = np.asarray(
        [
            2722.05531502,
            3366.00507206,
            4763.04670013,
            8087.36760191,
            11672.35909295,
            15432.7387546,
        ]
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    # make the plot!
    plot_indiv_fit.plot_beast_ifit(filters, waves, stats, pdf1d_hdu, starnum)

    return fig

@remote_data
@pytest.mark.mpl_image_compare(tolerance=10)
def test_plot_cmd():

    # Download example data from phat_small
    fitsfile =  _download_rename("b15_4band_det_27_A.fits")

    # Plot CMD using defaults
    fig = plot_cmd.plot(fitsfile)

    return fig

@remote_data
@pytest.mark.mpl_image_compare(tolerance=55)
def test_plot_cmd_with_fits():

    # Download example data from phat_small
    fitsfile =  _download_rename("b15_4band_det_27_A.fits")

    # Download BEAST fits to example data
    beast_fitsfile =  _download_rename("beast_example_phat_stats.fits")

    # Plot CMD using defaults
    fig = plot_cmd_with_fits.plot(fitsfile, beast_fitsfile)

    return fig


@remote_data
@pytest.mark.mpl_image_compare(tolerance=10)
def test_plot_filters():

    filter_names = ['HST_WFC3_F225W', 'HST_WFC3_F275W', 'HST_WFC3_F336W',
                    'HST_ACS_WFC_F475W', 'HST_ACS_WFC_F550M',
                    'HST_ACS_WFC_F814W',
                    'HST_WFC3_F110W', 'HST_WFC3_F160W']

    args = {"tex": True, "savefig": False}

    filters = _download_rename("filters.hd5")

    # Plot filters using above arguments (the defaults)
    fig = plot_filters.plot_filters(args, filter_names)

    return fig
