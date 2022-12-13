"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.
   
    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, pdes, name, diameter, pha):
        """Create a new `NearEarthObject`.

        :param pdes: the primary designation of the NEO. This is a unique identifier in the database, and its "name" to computer systems.
        :param name: the International Astronomical Union (IAU) name of the NEO. This is its "name" to humans.
        :param diameter: the NEO's diameter (from an equivalent sphere) in kilometers
        :param pha: whether NASA has marked the NEO as a "Potentially Hazardous Asteroid," roughly meaning that it's large and can come quite close to Earth.
        """
        self.designation = pdes
        self.name = name if name else None
        self.diameter = float(diameter) if diameter else float('nan')
        self.hazardous = True if pha == 'Y' else False

        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self.designation} ({self.name})'

    def __str__(self):
        """Return `str(self)`."""
        if self.hazardous:
            return f'A NearEarthObject {self.fullname} has a diameter of {self.diameter:.3f} and is potentially hazardous.'
        else:
            return f'A NearEarthObject {self.fullname} has a diameter of {self.diameter:.3f} and is not potentially hazardous.'

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f'NearEarthObject(designation={self.designation!r}, name={self.name!r}, '
                f'diameter={self.diameter:.3f}, hazardous={self.hazardous!r})')


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, des, cd, dist, v_rel):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = des
        self.time = cd_to_datetime(cd)
        self.distance = float(dist)
        self.velocity = float(v_rel)

        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.
        """
        return datetime_to_str(self.time)
        
    @property
    def fullname(self ):
       """Return a representation of the full name of this NEO."""
       return f'{self._designation} ({self.neo.name})'

    def __str__(self):
        """Return `str(self)`."""
        return f'On {self.time_str}, {self.fullname} approaches Earth ata a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s.'

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
