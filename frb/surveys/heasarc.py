""" Surveys to be accessed through the HEASARC interface (via astroquery"""

import pdb

from astropy.table import Table
from astropy import units

try:
    from astroquery.heasarc import Heasarc
except ImportError:
    print("Warning:  You need astroquery installed to use the surveys from HEASARC")

from frb.surveys import surveycoord
from frb.surveys import catalog_utils

    
class HEASARC_Survey(surveycoord.SurveyCoord):
    def __init__(self, coord, radius, mission, **kwargs):
        surveycoord.SurveyCoord.__init__(self, coord, radius, **kwargs)
        #
        self.survey = None
        self.mission = mission
        # Instantiate astroquery object
        self.heasarc = Heasarc()
    
    def get_catalog(self):
        try:
            catalog = self.heasarc.query_region(self.coord, mission=self.mission, radius=self.radius)
        except (ValueError, TypeError):  # No table found
            self.catalog = Table()
        else:
            # Clean
            catalog.rename_column("RA", "ra")
            catalog.rename_column("DEC", "dec")
            for key in ['ra', 'dec']:
                catalog[key].unit = units.deg
            # Sort
            self.catalog = catalog_utils.sort_by_separation(catalog, self.coord,
                                                            radec=('ra', 'dec'))
        # Add meta, etc.
        self.catalog.meta['radius'] = self.radius
        self.catalog.meta['survey'] = self.survey
        # Validate
        self.validate_catalog()
        # Return
        return self.catalog
        
        
class NVSS_Survey(HEASARC_Survey):
    def __init__(self, coord, radius, **kwargs):
        HEASARC_Survey.__init__(self, coord, radius, 'nvss', **kwargs)
        self.survey = 'NVSS'
        
class FIRST_Survey(HEASARC_Survey):
    def __init__(self, coord, radius, **kwargs):
        HEASARC_Survey.__init__(self, coord, radius, 'first', **kwargs)
        self.survey = 'FIRST'