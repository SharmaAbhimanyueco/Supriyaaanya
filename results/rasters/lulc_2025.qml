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
    <paletteEntry value="1" color="#b03a2e" alpha="255" label="Built-up"/>
    <paletteEntry value="2" color="#8db63c" alpha="255" label="Cropland"/>
    <paletteEntry value="3" color="#2e6b3f" alpha="255" label="Trees/vegetation"/>
    <paletteEntry value="5" color="#d9a441" alpha="255" label="Bare/fallow"/>
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
