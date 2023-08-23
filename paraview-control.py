#!/usr/bin/env python3

import glob
import os
import time

from paraview import collaboration
from paraview.simple import *


def load_data(dataset):
    pathname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

    files_raw = sorted(glob.glob(os.path.join(pathname, '{0}/droplets_raw_{0}.vtr'.format(dataset))))
    files_poly = sorted(glob.glob(os.path.join(pathname, '{0}/droplets_poly_{0}.vtu'.format(dataset))))
    files_point = sorted(glob.glob(os.path.join(pathname, '{0}/droplets_point_{0}.vtu'.format(dataset))))

    # Reset time to prevent crash
    animationScene1 = GetAnimationScene()
    animationScene1.AnimationTime = 0.0
    time.sleep(0.5)

    # Delete everything
    for f in GetSources().values():
        Delete(f)

    source_raw = XMLRectilinearGridReader(FileName=files_raw)
    source_poly = XMLUnstructuredGridReader(FileName=files_poly)
    source_point = XMLUnstructuredGridReader(FileName=files_point)
    RenameSource(dataset + '_raw', source_raw)
    RenameSource(dataset + '_poly', source_poly)
    RenameSource(dataset + '_point', source_point)

    renderView1 = GetActiveViewOrCreate('RenderView')

    display_raw = Show(source_raw, renderView1)
    display_poly = Show(source_poly, renderView1)
    display_point = Show(source_point, renderView1)

    display_raw.Representation = 'Outline'
    display_poly.Representation = 'Surface'
    display_point.Representation = 'Surface'

    glyph1 = Glyph(Input=source_point, GlyphType='Arrow')
    glyph1.OrientationArray = ['POINTS', 'velocity']
    glyph1.ScaleFactor = 0.07
    glyph1.GlyphType.TipResolution = 128
    glyph1.GlyphType.ShaftResolution = 128

    glyph1Display = Show(glyph1, renderView1)
    glyph1Display.Representation = 'Surface'
    glyph1Display.Specular = 0.7
    glyph1Display.SpecularPower = 25.0

    display_poly.Opacity = 0.3
    display_poly.Specular = 0.7
    display_poly.SpecularPower = 25.0

    calculator1 = Calculator(Input=source_raw)
    calculator1.AttributeType = 'Cell Data'
    calculator1.ResultArrayName = 'Log_Mag'
    calculator1.Function = 'ln(sqrt(v_X*v_X+v_Y*v_Y+v_Z*v_Z)+1)'

    calculator1Display = Show(calculator1, renderView1)

    glyph2 = Glyph(Input=calculator1, GlyphType='Arrow')
    glyph2.OrientationArray = ['CELLS', 'v']
    glyph2.ScaleArray = ['CELLS', 'Log_Mag']
    glyph2.ScaleFactor = 0.004
    glyph2.GlyphMode = 'Every Nth Point'
    glyph2.Stride = 1
    glyph2.GlyphType.TipResolution = 64
    glyph2.GlyphType.ShaftResolution = 64

    glyph2Display = Show(glyph2, renderView1)

    log_MagLUT = GetColorTransferFunction('Log_Mag')

    glyph2Display.Representation = 'Surface'
    glyph2Display.ColorArrayName = ['POINTS', 'Log_Mag']
    glyph2Display.LookupTable = log_MagLUT
    # glyph2Display.SetScalarBarVisibility(renderView1, True)
    glyph2Display.Specular = 0.7
    glyph2Display.SpecularPower = 25.0

    log_MagLUT.ApplyPreset('RdOrYl', True)
    log_MagLUT.InvertTransferFunction()

    Hide(source_raw, renderView1)
    Hide(calculator1, renderView1)
    Hide(source_point, renderView1)

    animationScene1 = GetAnimationScene()
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    time.sleep(0.5)


if __name__ == '__main__':
    print('ParaView Client Demo')

    Connect('localhost', timeout=0)
    time.sleep(1)

    running = True
    while running:
        time.sleep(0.1)

        # Should probably be called in a hot loop, but for simplicity we just use it here in the blocking input loop.
        collaboration.processServerEvents()

        read = input('Type \'1\', \'2\' or \'exit\': ')
        if read == '1':
            print('Data 1')
            load_data('0400_003061')
        elif read == '2':
            print('Data 2')
            load_data('0433_002662')
        elif read == 'exit':
            running = False
        else:
            print('Unknown input \'{}\''.format(read))

    Disconnect()
