"""
RenertPy Python Package
Copyright (C) 2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import warnings
import colorsys

def rgb_to_hsv(r,g,b):
    if not (r>=0 and r<=255):
        raise ValueError("Invalid r (red) value '%s': must be between 0 and 255" % str(r))
    if not (g>=0 and g<=255):
        raise ValueError("Invalid g (green) value '%s': must be between 0 and 255" % str(g))
    if not (b>=0 and b<=255):
        raise ValueError("Invalid b (blue) value '%s': must be between 0 and 255" % str(b))

    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)

    h = int(h * 360) # convert to degrees

    return [h,s,v]

def hsv_to_rgb(h,s,v):
    if not (h>=0 and h<=360):
        raise ValueError("Invalid h (hue) value '%s': must be between 0 and 360" % str(h))
    if not (s>=0.0 and s<=1.0):
        raise ValueError("Invalid s (saturation) value '%s': must be between 0.0 and 1.0" % str(s))
    if not (v>=0 and v<=255):
        raise ValueError("Invalid v (value) value '%s': must be between 0 and 255" % str(v))

    r,g,b = colorsys.hsv_to_rgb(h/360,s,v/255.0)  # normalize v to 0.0-1.0 range

    return [int(r*255), int(g*255), int(b*255)]


def hexcolor_to_rgb(cstr):
    # Python's Turtle has an undocumented function for this
    # ( TBuffer._color(str,cstr) ) which is nice an efficient,
    # but not user-friendly when given invalid input.
    # Since this module is meant for newbies, be less efficient and
    # more verbose with invalid input.
    if not cstr.startswith("#"):
        raise ValueError(f"invalid hex-color string '{cstr}' - must start with '#'")

    # Check if all the characeters (after '#') are hex-digits.
    # Here we don't yet care about the actual length - any length of valid hex-digits will work.
    # This code is less intuitive than standard check (e.g. regex or loop) but is more efficient
    # (as this is expected to be called once per pixel)
    try:
        dummy = int(cstr[1:], 16)
    except ValueError:
        raise ValueError(f"invalid hex-color string '{cstr}' - must start with '#' followed by 0-9,A-F characters")

    if len(cstr)==7:
        # Copied from turtle's _color()
        cl = [int(cstr[i:i+2], 16) for i in (1, 3, 5)]
    elif len(cstr)==4:
        # Copied from turtle's _color()
        cl = [16*int(h, 16) for h in cstr[1:]]
    else:
        raise ValueError(f"invalid hex-color string '{cstr}' - be '#' followed by 3 or 6 characters")

    return tuple(cl)

# LAB color space constants
_LAB_D65_X = 0.95047  # D65 illuminant X
_LAB_D65_Y = 1.0      # D65 illuminant Y
_LAB_D65_Z = 1.08883  # D65 illuminant Z

def rgb_to_lab(r, g, b):
    if not (r >= 0 and r <= 255):
        raise ValueError("Invalid r (red) value '%s': must be between 0 and 255" % str(r))
    if not (g >= 0 and g <= 255):
        raise ValueError("Invalid g (green) value '%s': must be between 0 and 255" % str(g))
    if not (b >= 0 and b <= 255):
        raise ValueError("Invalid b (blue) value '%s': must be between 0 and 255" % str(b))

    # Normalize to 0-1
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # Convert to linear RGB (inverse gamma correction)
    def _linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = _linear(r), _linear(g), _linear(b)

    # Convert to XYZ
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    # Normalize by D65 illuminant
    x, y, z = x / _LAB_D65_X, y / _LAB_D65_Y, z / _LAB_D65_Z

    # Convert to LAB
    def _f(t):
        return t ** (1/3) if t > 0.008856 else (7.787068 * t + 0.137931)

    x, y, z = _f(x), _f(y), _f(z)

    l = min(100.0, max(0.0, 116.0 * y - 16.0))
    a = 500.0 * (x - y)
    b_lab = 200.0 * (y - z)

    return [l, a, b_lab]

def lab_to_rgb(l, a, b_lab):
    if not (l >= 0 and l <= 100):
        raise ValueError("Invalid l (lightness) value '%s': must be between 0 and 100" % str(l))
    if not (a >= -128 and a <= 127):
        raise ValueError("Invalid a value '%s': must be between -128 and 127" % str(a))
    if not (b_lab >= -128 and b_lab <= 127):
        raise ValueError("Invalid b (blue) value '%s': must be between -128 and 127" % str(b_lab))

    # Convert LAB to XYZ
    y = (l + 16.0) / 116.0
    x = y + a / 500.0
    z = y - b_lab / 200.0

    def _f_inv(t):
        return t ** 3 if t ** 3 > 0.008856 else (t - 0.137931) / 7.787068

    x, y, z = _f_inv(x), _f_inv(y), _f_inv(z)

    x *= _LAB_D65_X
    y *= _LAB_D65_Y
    z *= _LAB_D65_Z

    # Convert XYZ to linear RGB
    r = x * 3.2404542 - y * 1.5371385 - z * 0.4985314
    g = -x * 0.9695774 + y * 1.8759675 + z * 0.0415560
    b = x * 0.0556434 - y * 0.2040259 + z * 1.0566141

    # Gamma correction
    def _gamma(c):
        return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1/2.4)) - 0.055

    r, g, b = _gamma(r), _gamma(g), _gamma(b)

    # Clamp to 0-1 and convert to 0-255
    r, g, b = max(0, min(1, r)), max(0, min(1, g)), max(0, min(1, b))

    return [int(r * 255), int(g * 255), int(b * 255)]

