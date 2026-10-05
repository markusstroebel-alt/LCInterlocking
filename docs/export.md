Export 
===========

![Illustration](imgs/export/overview.png)<br>

Once the connections have been created, parts can be exported to SVG.
Parts have to be selected before clicking to this feature. A new document is created with copied parts and projections on XY plan. Select projections and export it to the Flattened SVG format. 

Assembly components can be selected directly, including components inside nested Assemblys. The
export uses the visible component instance and its assembly placement. When the same source body
is used more than once, select the concrete visible instance instead of the underlying Body or
Pad.

Visible DXF export
------------------

Use **Export visible DXF** to create one DXF file for every part that is visible in the FreeCAD
model tree. The current 3D selection is ignored. Hide construction objects and source parts with
the space key before starting the command, then choose an output folder.

Identical visible finished parts are grouped into one DXF file, even when their instances have
different positions in the model. The outline text states the required quantity as `MENGE 2`, for
example. Parts with different contours, through cuts or pockets remain separate files.

Each DXF contains the required machining views of one part next to each other. A view combines the
outside contour, through cuts and pockets for its machining side. Parts with pockets on opposite
or additional sides receive additional labelled views in the same file. Labels are exported as
outline text and include the part name, machining side, material thickness and pocket depths.

The DXF uses Estlcam-oriented layers:

* `KONTUR` for the outside contour
* `DURCHBRUCH` for through cuts
* `TASCHE_<TIEFE>MM` for each pocket depth, for example `TASCHE_3_00MM`
* `TEXT` for the view labels

Assign the desired tools and milling strategies to these layers in Estlcam. The exporter detects
automatic depth layer.
planar pocket floors. Sloped or curved pockets are not classified automatically and should be
checked manually before machining.

You can use inkscape to remove some unwanted lines (if exist) as line between tab and its parts. To do it, ungroup all, object to path, remove unwanted lines, join curves with very little tolerance and you can regroup all if you want.

Some details are not correctly drawn with Inkscape (i.e. "circle) in contrary to Corel Draw for example.


Note : 

 * Thanks to arkhnchul, ".removeSplitter()" method is used on shape to remove these unwanted lines. If it leads to error,
remove this call in exportPanel.py.

 * The export / inkscape step can be seen on at the end of a video about an older version of the module (https://youtu.be/YGFIdLpdWXE).

**Note (2019-05-21) :**
Some elements of projected parts have problems. For example, a circle may be displayed and exported 
in flatten SVG as hexagon. 
A workaround is to export in Autodesk DXF 2D (.dxf) format. It may be imported as inkscape but elements
can not be ungrouped. To do it, dxf file has to be opened in librecad, then select all (Ctrl+a) and click on Tools ->
Modify -> explode. Save file and re-import with inkscape. Now each segments and curves can be edited.  
