from misc import *
X = ["./L8_vernon/LC08_L2SP_045025_20210803_20210811_02_T1/LC08_L2SP_045025_20210803_20210811_02_T1.bin_spectral_interp.bin_active.bin",
     "./L8_vernon/LC08_L2SP_045025_20210718_20210729_02_T1/LC08_L2SP_045025_20210718_20210729_02_T1.bin_spectral_interp.bin_active.bin",
     "./L8_vernon/LC08_L2SP_046025_20210725_20210803_02_T1/LC08_L2SP_046025_20210725_20210803_02_T1.bin_spectral_interp.bin_active.bin",
     "./L8_vernon/LC08_L2SP_046024_20210725_20210803_02_T1/LC08_L2SP_046024_20210725_20210803_02_T1.bin_spectral_interp.bin_active.bin",
     "./L8_vernon/LC08_L2SP_046024_20210810_20210819_02_T1/LC08_L2SP_046024_20210810_20210819_02_T1.bin_spectral_interp.bin_active.bin",
     "./L8_vernon/LC08_L2SP_046025_20210810_20210819_02_T1/LC08_L2SP_046025_20210810_20210819_02_T1.bin_spectral_interp.bin_active.bin",
     "./L7_vernon/LE07_L2SP_045025_20210811_20210906_02_T1/LE07_L2SP_045025_20210811_20210906_02_T1.bin_spectral_interp.bin_active.bin",
     "./L7_vernon/LE07_L2SP_046024_20210717_20210812_02_T1/LE07_L2SP_046024_20210717_20210812_02_T1.bin_spectral_interp.bin_active.bin",
     "./L7_vernon/LE07_L2SP_046024_20210802_20210828_02_T1/LE07_L2SP_046024_20210802_20210828_02_T1.bin_spectral_interp.bin_active.bin",
     "./L7_vernon/LE07_L2SP_045025_20210726_20210821_02_T1/LE07_L2SP_045025_20210726_20210821_02_T1.bin_spectral_interp.bin_active.bin",
     "./L7_vernon/LE07_L2SP_046025_20210818_20210913_02_T1/LE07_L2SP_046025_20210818_20210913_02_T1.bin_spectral_interp.bin_active.bin",
     "./L7_vernon/LE07_L2SP_046025_20210802_20210828_02_T1/LE07_L2SP_046025_20210802_20210828_02_T1.bin_spectral_interp.bin_active.bin",
     "./L7_vernon/LE07_L2SP_046025_20210717_20210812_02_T1/LE07_L2SP_046025_20210717_20210812_02_T1.bin_spectral_interp.bin_active.bin",
     "./L7_vernon/LE07_L2SP_046024_20210818_20210913_02_T1/LE07_L2SP_046024_20210818_20210913_02_T1.bin_spectral_interp.bin_active.bin"]

for x in X:
    run(['python3 ' + pd + 'raster_project_onto.py',
         x,
         'footprint3.bin',
         x + '_coreg.bin'])


