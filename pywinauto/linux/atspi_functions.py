import ctypes
import subprocess
from ctypes import Structure, c_char_p, c_int, POINTER


class CtypesEnum:
    @classmethod
    def from_param(cls, obj):
        return int(obj)


class RECT(Structure):

    """Wrap the RECT structure and add extra functionality"""

    _fields_ = [
        # C:/PROGRA~1/MIAF9D~1/VC98/Include/windef.h 287
        ('left', c_int),
        ('top', c_int),
        ('right', c_int),
        ('bottom', c_int),
    ]

    # ----------------------------------------------------------------
    def __init__(self, otherRect_or_left = 0, top = 0, right = 0, bottom = 0):
        """Provide a constructor for RECT structures

        A RECT can be constructed by:
        - Another RECT (each value will be copied)
        - Values for left, top, right and bottom

        e.g. my_rect = RECT(otherRect)
        or   my_rect = RECT(10, 20, 34, 100)
        """
        if isinstance(otherRect_or_left, RECT):
            self.left = otherRect_or_left.left
            self.right = otherRect_or_left.right
            self.top = otherRect_or_left.top
            self.bottom = otherRect_or_left.bottom
        elif isinstance(otherRect_or_left, AtspiRect):
            self.left = otherRect_or_left.x
            self.right = otherRect_or_left.x + otherRect_or_left.width
            self.top = otherRect_or_left.y
            self.bottom = otherRect_or_left.y + otherRect_or_left.height
        else:
            #if not isinstance(otherRect_or_left, (int, long)):
            #    print type(self), type(otherRect_or_left), otherRect_or_left
            self.left = otherRect_or_left
            self.right = right
            self.top = top
            self.bottom = bottom


#    # ----------------------------------------------------------------
#    def __eq__(self, otherRect):
#        "return true if the two rectangles have the same coordinates"
#
#        try:
#            return \
#                self.left == otherRect.left and \
#                self.top == otherRect.top and \
#                self.right == otherRect.right and \
#                self.bottom == otherRect.bottom
#        except AttributeError:
#            return False

    # ----------------------------------------------------------------
    def __str__(self):
        """Return a string representation of the RECT"""
        return "(L%d, T%d, R%d, B%d)" % (
            self.left, self.top, self.right, self.bottom)

    # ----------------------------------------------------------------
    def __repr__(self):
        """Return some representation of the RECT"""
        return "<RECT L%d, T%d, R%d, B%d>" % (
            self.left, self.top, self.right, self.bottom)

    # ----------------------------------------------------------------
    def __sub__(self, other):
        """Return a new rectangle which is offset from the one passed in"""
        newRect = RECT()

        newRect.left = self.left - other.left
        newRect.right = self.right - other.left

        newRect.top = self.top - other.top
        newRect.bottom = self.bottom - other.top

        return newRect

    # ----------------------------------------------------------------
    def __add__(self, other):
        """Allow two rects to be added using +"""
        newRect = RECT()

        newRect.left = self.left + other.left
        newRect.right = self.right + other.left

        newRect.top = self.top + other.top
        newRect.bottom = self.bottom + other.top

        return newRect

    # ----------------------------------------------------------------
    def width(self):
        """Return the width of the  rect"""
        return self.right - self.left

    # ----------------------------------------------------------------
    def height(self):
        """Return the height of the rect"""
        return self.bottom - self.top

    # ----------------------------------------------------------------
    def mid_point(self):
        """Return a POINT structure representing the mid point"""
        pt = AtspiPoint()
        pt.x = self.left + int(float(self.width())/2.)
        pt.y = self.top + int(float(self.height())/2.)
        return pt


class AtspiCoordType(CtypesEnum):
    ATSPI_COORD_TYPE_SCREEN = 0
    ATSPI_COORD_TYPE_WINDOW = 1


class AtspiRect (Structure):
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
        ('width', c_int),
        ('height', c_int),
    ]


class AtspiPoint (Structure):
    _fields_ = [
        ('x', c_int),
        ('y', c_int),
    ]


class AtspiAccessible (Structure):
    pass


class AtspiComponent (Structure):
    pass


class GError (Structure):
    pass


class AtspiFunctions:
    """ Python wrapper around C functions from atspi library"""
    LIB = "libatspi"
    DEFAULT_LIB_NAME = "libatspi.so"

    def __find_library(self):
        try:
            process = subprocess.Popen(["ldconfig", "-p"], stdout=subprocess.PIPE, universal_newlines=True)
            stdout = process.communicate()
            libraries = stdout[0]
            for lib in libraries.split("\n"):
                if self.LIB in lib:
                    return lib.split()[0]

        except FileNotFoundError:
            # ldconfig not installed will use default lib name
            return self.DEFAULT_LIB_NAME

    def __init__(self):
        try:
            atspi = ctypes.cdll.LoadLibrary(self.__find_library())
            self.get_desktop = atspi.atspi_get_desktop
            self.get_desktop.argtypes = [c_int]
            self.get_desktop.restype = POINTER(AtspiAccessible)

            self.get_name = atspi.atspi_accessible_get_name
            self.get_name.argtypes = [POINTER(AtspiAccessible), POINTER(GError)]
            self.get_name.restype = c_char_p

            self.get_id = atspi.atspi_accessible_get_id
            self.get_id.argtypes = [POINTER(AtspiAccessible), POINTER(GError)]
            self.get_id.restype = c_int

            self.get_process_id = atspi.atspi_accessible_get_process_id
            self.get_process_id.argtypes = [POINTER(AtspiAccessible), POINTER(GError)]
            self.get_process_id.restypes = c_int

            self.get_role_name = atspi.atspi_accessible_get_role_name
            self.get_role_name.argtypes = [POINTER(AtspiAccessible), POINTER(GError)]
            self.get_role_name.restype = c_char_p

            self.get_parent = atspi.atspi_accessible_get_parent
            self.get_parent.artypes = [POINTER(AtspiAccessible), POINTER(GError)]
            self.get_parent.restype = POINTER(AtspiAccessible)

            self.get_child_count = atspi.atspi_accessible_get_child_count
            self.get_child_count.argtypes = [POINTER(AtspiAccessible), POINTER(GError)]
            self.get_child_count.restype = c_int

            self.get_child_at_index = atspi.atspi_accessible_get_child_at_index
            self.get_child_at_index.argtypes = [POINTER(AtspiAccessible), c_int, POINTER(GError)]
            self.get_child_at_index.restype = POINTER(AtspiAccessible)

            self.get_position = atspi.atspi_component_get_position
            self.get_position.argtypes = [POINTER(AtspiComponent), AtspiCoordType, POINTER(GError)]
            self.get_position.restype = POINTER(AtspiPoint)

            self.get_size = atspi.atspi_component_get_size
            self.get_size.argtypes = [POINTER(AtspiComponent), POINTER(GError)]
            self.get_size.restype = POINTER(AtspiPoint)

            self.get_rectangle = atspi.atspi_component_get_extents
            self.get_rectangle.argtypes = [POINTER(AtspiComponent), AtspiCoordType, POINTER(GError)]
            self.get_rectangle.restype = POINTER(AtspiRect)

            self.get_component = atspi.atspi_accessible_get_component
            self.get_component.argtypes = [POINTER(AtspiAccessible)]
            self.get_component.restype = POINTER(AtspiComponent)

        except Exception as e:
            message = "atspi library not installed. Please install at-spi2 library or choose another backend"
            raise Exception(message)


