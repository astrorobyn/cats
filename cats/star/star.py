"""Star stuff."""

from __future__ import annotations

# THIRD-PARTY
import numpy as np
from gala.coordinates import GreatCircleICRSFrame

# LOCAL
from cats.pawprint.pawprint import Pawprint

# notes on data types
dtypes_dict = {
    # identifiers
    "sourceID": "u8",  # Gaia DR3 source id, unsigned integer
    # integer representing version of gaia catalog that the source ID refers to
    "sourceID_version": "u2",
    "streamID": "s10",  # 10-char string? check galstreams
    "crossmatches": {},  # dictionary to store IDs in other surveys
    # phase space
    "w": {},  # dict of phase space coordinates
    "w_uncert": {},  # dictionary of uncertainties per coordinate
    # todo: add function to convert w to SkyCoord
    # todo: bring in pyia to account for transformations to uncertainties
    # precompute and store phi1 and phi2 for a desired coordinate frame
    "phi1": "f8",
    "phi2": "f8",
    "rotation": GreatCircleICRSFrame(),  # placeholder
    # flag for variable stars
    "variability": "u2",  # 0 if not variable, 1 if variable
    # photometry from Gaia used for selections in pawprint
    "phot_g_mean_mag": "f4",
    "phot_rp_mean_mag": "f4",
    "phot_g_mean_mag_error": "f4",
    "phot_rp_mean_mag_error": "f4",
    # TODO WG3: how to store extinction?
    # consensus chemistry
    "feh_logeps": "f4",  # sun-independent value
    "feh": "f4",  # iron abundance as [Fe/H]
    "feh_solar": "f4",  # solar value of [Fe/H] for this star
    "alpha_logeps": "f4",  # sun-independent value
    "alpha_fe": "f4",  # alpha abundance as [alpha/Fe]
    "alpha_solar": "f4",  # solar value of [alpha/H] for this star
    # references: assumes that sky position, photometry, and PM are from Gaia
    "refs": {
        # ADS bibcode (or pointer to docs) for distance measurement; can be a list
        "distance": ["s19"],
        "rv": ["s19"],
        "feh": ["s19"],
        "alpha": ["s19"],
        "variability": ["s19"],
        "extinction": ["s19"],
    }
    # TODO: membership likelihoods
}

# functions imported from


def get_phase_space():
    """Query gaia to initialize SkyCoords for phase-space position and uncertainty."""


def get_gaia_photometry(stardata: StarData):
    """Query gaia to get photometry and uncertainties, returned as 32 bit floats."""


def get_abundances(stardata: StarData):
    """Query ancillary data tables for spectroscopy."""

    # TODO:function to return sky coordinates and uncertainties in two skycoord
    # objects by querying Gaia.
    # stardata.w, stardata.w_uncert = phasespace_to_skycoords()


class Star:
    """Star."""

    def __init__(self, streamID, pawprintID):
        # starclass
        self.data = StarData(streamID, pawprintID)
        self.derived = StarDerived(streamID, pawprintID)

    @classmethod
    def from_file(cls, fname):
        ...


class StarData:
    """dictionary class to store __measured__ attributes for one star in the catalog."""

    def __init__(self, streamID, pawprintID):

        self.sourceID_version = np.uint(3)  # default for now is DR3
        self.streamID = np.str_(streamID)
        self.pawprintID = np.str_(pawprintID)
        self.pawprint = Pawprint.from_file(streamID, pawprintID)

        self.sourceID = load_stream(  # noqa: F821
            self.streamID
        )  # read from adrian's initial files

        self.nstars = nstars = len(self.sourceID)

        self.crossmatches = {}  # TODO: how to rept crossmatches to other catalogs

        # # TODO:function to return sky coordinates and uncertainties
        # # in two skycoord objects by querying Gaia
        # self.w, self.w_uncert = phasespace_to_skycoords()

        # flexible magnitudes - pin down standardised naming convention
        # my proposal: [survey]_[filter]
        # uncertainties and extinctions are specified by the same tags
        self.mags = {
            "gaia_g": np.array(nstars, dtype="f4"),
            "gaia_rp": np.array(nstars, dtype="f4"),
        }
        self.mag_uncert = {
            "gaia_g": np.array(nstars, dtype="f4"),
            "gaia_rp": np.array(nstars, dtype="f4"),
        }
        self.ext = {
            "gaia_g": np.array(nstars, dtype="f4"),
            "gaia_rp": np.array(nstars, dtype="f4"),
        }

        self.variability = np.array(nstars, dtype="u2")

        self.feh = np.ma.array(nstars, dtype="f4")
        self.feh_logeps = np.ma.array(nstars, dtype="f4")
        self.feh_solar = np.ma.array(nstars, dtype="f4")
        self.alpha_logeps = np.ma.array(nstars, dtype="f4")
        self.alpha_fe = np.ma.array(nstars, dtype="f4")
        self.alpha_solar = np.ma.array(nstars, dtype="f4")

        self.refs = {
            # ADS bibcode (or pointer to doi) for distance measurement; can be a list
            "distance": np.array(nstars, dtype="s19"),
            "rv": np.array(nstars, dtype="s19"),
            "feh": np.array(nstars, dtype="s19"),
            "alpha": np.array(nstars, dtype="s19"),
            "variability": np.array(nstars, dtype="s19"),
        }

        get_gaia_photometry(self)  # load gaia photometry in from catalog
        get_abundances(self)  # load abundances from detailed spectroscopoc tables


class StarDerived:
    """class to store derived attributes."""

    ...


def makeMask(self, what: str) -> None:
    """Make a mask.

    Take in some data and return masks for stuff in the pawprint (basically by
    successively applying _inside_poly).

    Parameters
    ----------
    what: str
    """
    # returns mask with same dimension as data
    mask = np.zeros(len(self.sourceID))
    if "sky" in what:
        mask += self.pawprint
