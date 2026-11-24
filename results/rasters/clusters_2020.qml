<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34.0-Prizren" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">
 <pipe>
  <provider>
   <resampling enabled="false" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour" maxOversampling="2"/>
  </provider>
  <rasterrenderer type="paletted" band="1" opacity="1" alphaBand="-1" nodataColor="">
   <rasterTransparency/>
   <minMaxOrigin>
    <limits>None</limits>
    <extent>WholeRaster</extent>
    <statAccuracy>Estimated</statAccuracy>
    <cumulativeCutLower>0.02</cumulativeCutLower>
    <cumulativeCutUpper>0.98</cumulativeCutUpper>
    <stdDevFactor>2</stdDevFactor>
   </minMaxOrigin>
   <colorPalette>
    <paletteEntry value="1" color="#d9a441" alpha="255" label="1 · Bare/fallow"/>
    <paletteEntry value="2" color="#b03a2e" alpha="255" label="2 · Built-up"/>
    <paletteEntry value="3" color="#2e6b3f" alpha="255" label="3 · Trees/vegetation"/>
    <paletteEntry value="4" color="#6f9a2c" alpha="255" label="4 · Cropland"/>
    <paletteEntry value="5" color="#4f8a5c" alpha="255" label="5 · Trees/vegetation"/>
    <paletteEntry value="6" color="#80aa35" alpha="255" label="6 · Cropland"/>
    <paletteEntry value="7" color="#8db63c" alpha="255" label="7 · Cropland"/>
    <paletteEntry value="8" color="#a2c55a" alpha="255" label="8 · Cropland"/>
    <paletteEntry value="9" color="#b6d27a" alpha="255" label="9 · Cropland"/>
    <paletteEntry value="10" color="#c9df9c" alpha="255" label="10 · Cropland"/>
   </colorPalette>
   <colorramp type="randomcolors" name="[source]"><Option/></colorramp>
  </rasterrenderer>
  <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
  <huesaturation saturation="0" grayscaleMode="0" colorizeOn="0" colorizeRed="255" colorizeGreen="128" colorizeBlue="128" colorizeStrength="100" invertColors="0"/>
  <rasterresampler maxOversampling="2"/>
  <resamplingStage>resamplingFilter</resamplingStage>
 </pipe>
 <blendMode>0</blendMode>
</qgis>
