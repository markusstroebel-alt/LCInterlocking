# LCInterlocking - Laser cut interlocking workbench for FreeCAD
Current version 1.5.0 - [release notes](CHANGELOG.md).

![Illustration](docs/imgs/illustration.png)

## Goal
This experimental FreeCAD workbench is used to create interlocking cut parts from 3D to 2D SVG. 
It was created for laser cutting but can work with CNC router.  

**Important Note:**  
**This is still experimental and as a consequence, not reliable. You must check parts before doing the laser cut.**  
**Please double check the results of this module!**

## Panel
This panel appears when "Laser cut Interlocking" workbench is selected:
![Illustration](docs/imgs/panel.png)

## Tools

 * ![Illustration](docs/imgs/box_generator.png) [Generate box without connection.](docs/box_generator.md)
 * ![Illustration](docs/imgs/interlocking.png) [Create tabs/slots connection.](docs/interlocking.md) (Interlocking tool)
 * ![Illustration](docs/imgs/crosspiece.png) [Create node for cross connection.](docs/crosspiece.md) (Crosspiece tool)
 * ![Illustration](docs/imgs/roundedboxgenerator.png) [Generate rounded box without connection.](docs/rounded_box_generator.md)
 * ![Illustration](docs/imgs/living_hinges.png) [Create bend surface with living hinges.](docs/living_hinges.md)
 * [Create hole templates from assembly hardware.](docs/hole_templates.md) (Hole templates tool)
 * ![Illustration](docs/imgs/export.png) [Project parts to 2D plan in order to export in SVG format.](docs/export.md) (Export tool)
 * [Export visible model-tree parts as labelled, layered DXF files for Estlcam, grouped by identical geometry.](docs/export.md)

## Connection Guide

Use the **Interlocking** tool to create a `MultiJoin` object and define the parts and faces that
must connect. Select a connection type in the task panel, add the faces, adjust the properties,
then use **Preview** to inspect the generated parts before confirming the dialog. The generated
parts should always be checked before cutting.

### Tab and Pocket Connections

Standard **Tab** connections create matching tabs and slots. Disable **Through tabs** to make a
blind pocket instead of a through-slot. In this mode, set **Tab length** to the tab depth and
**Tab length tolerance** to the additional clearance at the pocket bottom.

### Screw Connections

Choose **Screw** for a conventional screw, washer, and nut pocket. The nut shape is controlled by
**Nut flat to flat** and **Nut height**. Enable **Use washer** to add the matching washer pocket.
Use **Nut slot overhang** for extra space behind the nut and **Thread clearance** for the
protruding screw thread.

Choose **WoodScrew** when the screw threads directly into the second part. It only creates the
tabs and the screw-shaft hole; it does not create a nut or washer pocket.

### Screw-In Nuts

Choose **ScrewInNut** for an insert or screw-in nut. Set the screw diameter and length, the nut
outer diameter and nut depth, and optionally the washer dimensions. The screw channel length is:

```text
screw channel = screw length - washer thickness - nut depth
```

The screw head is not part of the entered screw length. **Thread clearance** adds reserve behind
the insert nut but does not change the screw channel length. **Head clearance** creates a
screw-width access channel for an Allen key without moving the screw channel.

Enable **Use nut flange pocket** for insert nuts with a collar or flange. Enter a larger
**Flange pocket diameter** and its **Flange pocket depth**. This concentric step pocket is made on
the same face as the insert-nut pocket and does not change the screw length, screw channel,
washer pocket, nut depth, thread clearance, or head clearance.

### Defaults and Presets

Open **Edit -> Preferences -> LCInterlocking** to set default material tolerances, screw values,
ScrewInNut values, and optional flange-pocket values for new connections. Existing connections
keep their own dimensions.

Use the **Preset** selector in a connection panel to apply saved values. **Save as...** stores the
current connection settings for its connection type, and **Delete** removes the selected preset.
Global presets can also be reviewed and edited in the **Global connection presets** table in the
same preferences page.

### Contact Face Detection

After adding the involved parts to a MultiJoin, use **Detect contact faces** to find planar,
opposing faces that overlap within the configured contact tolerance. The dialog lists every
candidate pair and lets you choose which side creates the connection. Only one side should be
used for a pair, because the selected side creates the tabs while the opposite part receives the
matching pockets.

The new face is added to the usual connection list. Change its **Connection type** there at any
time to choose Tab, Screw, WoodScrew, ScrewInNut, or Continuous. Faces created by **Add same
faces** keep following their master face. Set **Contact detection tolerance (mm)** under
**Edit -> Preferences -> LCInterlocking**. The default is `0.01 mm`.

### Multiple Connections per Face

A face may be added more than once. Each entry is an independent connection, so for example a
`TongueGroove` and a `Screw` connection can be combined on `Wall.Face1`. The MultiJoin tree
lists them separately as `Face1 (TongueGroove)` and `Face1 (Screw)`. Removing or editing one
entry leaves the other entries on that face unchanged.

When `TongueGroove` and `Screw` or `ScrewInNut` use the same face and counter part, each
`Tab - screw - Tab` group interrupts both the tongue and the groove. The Screw tabs, slots, and
bore remain intact, so multiple screw positions create separate accessible interruptions.

### Tongue and Groove Connections

Choose **TongueGroove** to extend the selected face as one continuous tongue over its full width
and cut a matching groove into the intersecting part. The selected face always belongs to the
part that receives the extension. Use **Groove depth** for the tongue length and matching groove
depth, for example `10 mm` for a drawer bottom.

The connection first follows the selected face normal and automatically uses the opposite direction
when that is the only direction that reaches an intersecting counter part. This allows multiple
faces on a part to form connections even when their normals point in opposite directions.

Set **Height mode** to **Full material thickness** for a full-height tongue, or **Custom height**
to enter a smaller tongue height. **Height alignment** positions a custom tongue at the material
center or at **Side A** / **Side B** of the selected face. Use Preview to verify the side in the
current part orientation. **Groove bottom clearance** makes the groove deeper than the tongue;
the existing slot-width tolerance provides fit clearance around the full tongue cross-section.
For **Side A** and **Side B**, the tongue remains flush at its selected material side; the
slot-width tolerance expands only the matching groove around its nominal cross-section.

Global TongueGroove defaults are available under **Edit -> Preferences -> LCInterlocking** and
can be saved in connection presets.

### Assembly Workflow

When working with the FreeCAD Assembly workbench, add the Assembly components (the `App::Link`
instances) to Interlocking. The original components remain in the Assembly after generating a
MultiJoin. A generated result such as `Base_tab` can then be selected with another Assembly
component such as `Wall001` to create a further connection.

Nested Assembly components are supported as well. Select the visible component or face at the
depth where it is used in the outer Assembly. LCInterlocking keeps the full selection path, so
MultiJoin, Crosspiece, Living Hinge, Hole templates, and Export use the placed nested instance
after a recompute instead of a similarly named source body. When several instances share a
source body, select the concrete visible instance; ambiguous source-body selections are not
guessed.

### Hole Templates

Use **Hole templates** to create new target bodies with the overlapping geometry of screws,
bolts, hinges, slides, or other hardware removed. Select all involved bodies before starting the
tool. In the task panel, move the hardware to **Template bodies** and the parts to machine to
**Target bodies**, then inspect **Preview** and confirm the result.

The source bodies remain unchanged. Each operation creates one editable `Hole template` node;
its children are the generated target parts that actually intersect a template. Right-click the
node and choose **Edit** to revise the roles and update its existing results. A body cannot have
both roles, which prevents unintentional all-against-all boolean cuts. Assembly links are
resolved to their placed components.

While the dialog is open, select additional components in the 3D view and use
**Add selected bodies**. New components are added to **Selected bodies**, where they can be
assigned as templates or targets. Bodies already present in the operation are not duplicated.

## Installation

### Recommended Install
[![FreeCAD Addon manager status](https://img.shields.io/badge/FreeCAD%20addon%20manager-available-brightgreen)](https://github.com/FreeCAD/FreeCAD-addons)

Install this Addon via the builtin [FreeCAD Addon Manager](https://github.com/FreeCAD/FreeCAD-addons#1-builtin-addon-manager).  
1. Locate LCInterlocking in the Addon Manager
2. Install
3. Restart FreeCAD  
**Result**: 'Laser cut Interlocking' will be available via the workbench dropdown menu.

### Manual Install
<details>
<summary><i>Expand this to read more about manual installation of LCInterlocking FreeCAD Addon</i></summary>
  
1. Download the repository as zip via the Github interface or use `git` to clone the repo via the command line using:  
```bash
  git clone https://github.com/execuc/LCInterlocking .
```
2. After the download completes, the module must be moved to the `Mod` subfolder of the Freecad install directory.  
 - On Linux: `/home/<username>/.local/share/FreeCAD/Mod`
 - On Windows: `C:\Users\<username>\Appdata\Roaming\FreeCAD\Mod\`
 - On macOS: `/Users/<username>/Library/Application Support/FreeCAD/Mod/`

3. Restart Freecad and the LCInterlocking module should be detected.
</details>

## Troubleshooting Tip
It is advisable to show the FreeCAD report view and to redirect the python errors to show module warning/error.

## Feedback
If you encounter a bug please participate in the [dedicated FreeCAD discussion thread](https://forum.freecadweb.org/viewtopic.php?f=8&t=41196) and open a ticket in this repo's issue queue.

## Some videos previous versions
 * Box generator/interlocking/inkscape: https://youtu.be/YGFIdLpdWXE
 * Box tool: https://www.youtube.com/watch?v=wuu_lRsXGd0
 * Rounded box tool:  https://www.youtube.com/watch?v=lEOgZ6k9Vxw
 * Crosspiece: https://www.youtube.com/watch?v=tIchogx5BLE
 * Rounded corner: https://www.youtube.com/watch?v=KSnMxqjA_-Q
 
## Gallery
![Illustration](docs/imgs/illustration2.png)  
![Illustration](docs/imgs/illustration3.png)

## License
LGPL v2.1
