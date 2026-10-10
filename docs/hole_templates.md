# Hole templates

The **Hole templates** tool creates machining-ready copies of selected parts. It removes the
exact volume where selected hardware intersects a target part. This is useful for screw and bolt
holes, hinge recesses, drawer-slide cut-outs, and other assembly hardware.

## Workflow

1. In the FreeCAD 3D view, select all hardware and parts involved in the operation.
2. Start **Hole templates** from the **Templates** toolbar in the Laser Cut Interlocking
   workbench.
3. In the task panel, select bodies in **Selected bodies** and assign them to one of these roles:
   - **Template bodies**: hardware or a dedicated cutter solid.
   - **Target bodies**: parts that receive holes or pockets.
4. Use **Preview** to open a separate document containing the resulting target shapes.
5. Confirm with **OK** to add the final parts to the source document.

Each confirmed operation appears as one editable `Hole template` node in the document tree.
Generated parts appear as its children and record the names of their source target and template
bodies. The original target bodies remain in the document but are hidden while their generated
counterparts are shown; template bodies remain visible.

## Editing an operation

Right-click a `Hole template` node and choose **Edit**. Its existing template and target roles
are restored in the task panel. Move a body back to **Selected bodies** before assigning it to a
different role. Confirming recalculates the operation and reuses the existing generated parts
where possible, so the document tree does not accumulate duplicate result groups.

To add more components, select them in the 3D view while the dialog is open, then click
**Add selected bodies**. The new components appear under **Selected bodies** and can be assigned
to either role. Existing entries are not added a second time.

## Assembly support

The tool accepts FreeCAD Assembly `App::Link` components. When a linked component is selected,
its placed shape is used for the boolean operation, so holes and pockets are created at the
assembly position.

## Limits

Only template volumes that overlap a target are removed. Touching faces and non-overlapping
bodies create no result. The first version uses the exact hardware volume, without an additional
clearance or drilling-diameter offset. Add clearance directly to a dedicated cutter body when
needed.