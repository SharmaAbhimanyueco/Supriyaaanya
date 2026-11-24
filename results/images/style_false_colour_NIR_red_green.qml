<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34.0-Prizren" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0">
 <pipe>
  <provider>
   <resampling enabled="false" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour" maxOversampling="2"/>
  </provider>
  <rasterrenderer type="multibandcolor" redBand="4" greenBand="3" blueBand="2" opacity="1" alphaBand="-1" nodataColor="">
   <rasterTransparency/>
   <minMaxOrigin>
    <limits>None</limits>
    <extent>WholeRaster</extent>
    <statAccuracy>Estimated</statAccuracy>
    <cumulativeCutLower>0.02</cumulativeCutLower>
    <cumulativeCutUpper>0.98</cumulativeCutUpper>
    <stdDevFactor>2</stdDevFactor>
   </minMaxOrigin>
   <redContrastEnhancement>
    <minValue>1544</minValue>
    <maxValue>4048</maxValue>
    <algorithm>StretchToMinimumMaximum</algorithm>
   </redContrastEnhancement>
   <greenContrastEnhancement>
    <minValue>301</minValue>
    <maxValue>1582</maxValue>
    <algorithm>StretchToMinimumMaximum</algorithm>
   </greenContrastEnhancement>
   <blueContrastEnhancement>
    <minValue>456</minValue>
    <maxValue>1333</maxValue>
    <algorithm>StretchToMinimumMaximum</algorithm>
   </blueContrastEnhancement>
  </rasterrenderer>
  <brightnesscontrast brightness="0" contrast="0" gamma="1"/>
  <huesaturation saturation="0" grayscaleMode="0" colorizeOn="0" colorizeRed="255" colorizeGreen="128" colorizeBlue="128" colorizeStrength="100" invertColors="0"/>
  <rasterresampler maxOversampling="2"/>
  <resamplingStage>resamplingFilter</resamplingStage>
 </pipe>
 <blendMode>0</blendMode>
</qgis>
