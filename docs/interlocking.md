Interlocking
===========

This is the main tool of the LCInterlocking module. It allows to define connections between parts to create tabs and slots.

Parts can come from the Freecad Part/Part Design workshops or from the box generator tool of this module for example. To create a connection, the faces must stick.

There are four type of connections : tab, continuous tab, screw and wood screw. <br>
![Illustration](imgs/interlocking/tab.png) <br>
![Illustration](imgs/interlocking/continuous.png) <br>
![Illustration](imgs/interlocking/screw.png)<br>

Procedure
-------------
For this example, we start from parts generated from Box generator tool to make an 3mm thickness box. We remove three panels to simplify example.

 * Click on Interlocking tool to create a "MultiJoin" group in the treeview and go to edit mode.
 * All involved parts have to be defined in tool. Select all the parts and click on "Add same parts". All parts share the same material properties and appear as items in the treeview. Gray items means they are linked to the black item. Parts can be added with "Add part" but they will have different material properties.<br><br>
  ![Illustration](imgs/interlocking/add_parts.png)
  * Specify material properties:
    * Name of the generated part
    * Thickness and tolerance of the material
    * Slot width tolerance: add tolerance on slot
    * Laser beam diameter: diameter of the material destroyed by the laser.
  * Hide the longest side panel (select from the tool list view and use space key)
  * Select the lateral face of the bottom part, select screw in the list instead of tab.
  * Click on "Add same faces" and adjust parameters as number of tabs, screw dimensions...<br>
  
  ![Illustration](imgs/interlocking/add_screw.png)
  
  * Select the lateral face of the short side and choose "Tab" in the list.
  * Click on "Add same faces" or "Add faces" and adjust parameters<br>
  
![Illustration](imgs/interlocking/add_conti.png)

  * With the same method, create a "tab" connection between the bottom and the short side.<br>
  
  ![Illustration](imgs/interlocking/add_tab.png)
 
  * Click on OK to create a "MultiJoin" group. Origin parts are represented inside a "MultiJoin_origin_parts" group. Interlocking parts are below this group.<br>
   
   ![Illustration](imgs/interlocking/interlocking_final.png)
  
<br>
Now, parts can be exported via the "Export tool" in order to obtain a 2D file (SVG).
  
Additional Information
----------------------------
  * Interlocking properties can be edited again clicking on "MultiJoin" group item.
  * In editing mode, parts and faces can can be visualized by selecting the in the treview of the tools. Then they can be displayed/hidden by tapping in the key "space".
  * Preview button allow to create a new document with interlocking parts without exiting tool. It's convenient to adjust connection parameters.
  * "Add same faces" works as "Add same parts", faces while share the same connection properties.
  * For "screw" connections, the nut pocket shape is defined by "Nut flat to flat" and "Nut height",
    both freely editable (suggested values are pre-filled from the screw dimensions, or from the
    last values used in the current session).
  * Optionally, check "Use washer" to add a rectangular through-cut pocket for a washer, handled
    just like the nut pocket and positioned directly after it. Its width and length ("Washer
    diameter"/"Washer thickness") are also freely editable, with a suggested default.
  * A "Preset" dropdown is available above the connection properties. Selecting a preset fills in
    all matching fields at once; "Save as..." stores the current values under a name, "Delete"
    removes the selected preset. Presets are stored globally (available in every project) and are
    filtered by connection type.
  * The default values for "Thickness tolerance", "Laser beam diameter" and "Slot width tolerance"
    can be configured under Edit → Preferences → LCInterlocking. New materials use these values
    automatically; existing materials can be updated with the "Reset tolerances to defaults"
    button in the material properties.
  * "WoodScrew" is a lighter alternative to "Screw": it only creates the tabs and a round hole for
    the screw shaft in the other part, without the pocket for a nut/washer — useful when the screw
    threads directly into the material. Parameters: "Half tab ratio" and "Screw diameter".

