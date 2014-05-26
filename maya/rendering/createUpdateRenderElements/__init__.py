
"""
Create/Update Render Elements Package
==========================================

Automatic setup of VRay Render Elements in Maya.
Modules of this package set up light, framebuffer, data and shadow passes automatically.
Light is split into light select render elements.
This is the initial automatic setup which sets up multichannel .exrs
that should automatically rebuild in comp using :mod:`helga.nuke.reconstruction.renderReconstructVRay`

-----------------------

*Author:* `Timm Wagener <mailto:wagenertimm@gmail.com>`_
*Version:* 0.1
"""