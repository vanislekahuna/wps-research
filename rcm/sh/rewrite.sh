# rewrite the data to overcome an error encountered in reprojecting
gdal_translate 5MCP13_20210715.bin -of GTiff -ot Float32 -co "TILED=YES" 5MCP13_20210715.tif &
gdal_translate 5MCP13_20210719.bin -of GTiff -ot Float32 -co "TILED=YES" 5MCP13_20210719.tif &
gdal_translate 5MCP18_20210718.bin -of GTiff -ot Float32 -co "TILED=YES" 5MCP18_20210718.tif &
gdal_translate 5MCP19_20210710.bin -of GTiff -ot Float32 -co "TILED=YES" 5MCP19_20210710.tif &
gdal_translate 5MCP19_20210714.bin -of GTiff -ot Float32 -co "TILED=YES" 5MCP19_20210714.tif &
gdal_translate 5MCP19_20210722.bin -of GTiff -ot Float32 -co "TILED=YES" 5MCP19_20210722.tif &
 gdal_translate 5MCP7_20210708.bin  -of GTiff -ot Float32 -co "TILED=YES" 5MCP7_20210708.tif & 
 gdal_translate 5MCP7_20210716.bin  -of GTiff -ot Float32 -co "TILED=YES" 5MCP7_20210716.tif &
 gdal_translate 5MCP7_20210720.bin  -of GTiff -ot Float32 -co "TILED=YES" 5MCP7_20210720.tif &