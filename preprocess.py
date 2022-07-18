from astropy.table import Table
from astropy.io import ascii
import numpy as np

data = Table.read("S2_relAST_unprocessed.txt", format="ascii")
processed = Table(
    names=("Date", "Sep", "Err_sep", "PA", "Err_PA", "Corr_Sep_PA", "PlanetID")
)


def to_sep(ra, dec, ra_err, dec_err):
    # this is exact, assuming 0 correlation between ra and dec.
    sf = (10 ** (4.0/3))
    sep = np.sqrt(ra ** 2 + dec ** 2) / sf
    sep_err = (np.sqrt((ra * ra_err) ** 2 + (dec * dec_err) ** 2) / sep)/sf
    return sep, sep_err


def to_pa(ra, dec, ra_err, dec_err):
    pa = np.arctan2(ra, dec)
    # this pa error is approximate, but wayyy simpler than the full fledged solution.
    pa_err = (np.arctan2((ra_err + dec_err) / 2, np.sqrt(ra ** 2 + dec ** 2)))
    return (pa * 180 / np.pi + 360) % 360, (pa_err * 180 / np.pi + 360) % 360


for row in data:
    date = row["Date"]
    delta_ra = row["DeltaR.A."]
    delta_dec = row["DeltaDecl."]
    delta_ra_err = row["DeltaR.A.Error"]
    delta_dec_err = row["DeltaDecl.Error"]

    sep, sep_err = to_sep(delta_ra, delta_dec, delta_ra_err, delta_dec_err)
    pa, pa_err = to_pa(delta_ra, delta_dec, delta_ra_err, delta_dec_err)

    corr_sep_pa = 0
    planetID = 0

    processed.add_row([date, sep, sep_err, pa, pa_err, corr_sep_pa, planetID])

# print(processed)
ascii.write(
    processed, "output/data/S2_relAST.txt", format="commented_header", overwrite=True
)
