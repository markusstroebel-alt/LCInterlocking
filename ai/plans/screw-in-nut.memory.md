# Memory: screw-in-nut

## Status
- Plan finalized: [impact-nut-connection.md](./impact-nut-connection.md)
- Branch `feature/screw-in-nut` created.

## Decisions
- Type name: `ScrewInNut` (Eindrehmutter).
- Input: screw length, screw diameter, nut outer diameter, nut depth, thread clearance.
- Optional washer uses existing washer diameter/thickness values.
- Derived channel length:
  `screw_channel_length = screw_length - washer_thickness - nut_depth - thread_clearance`.
- Inner screw passage is derived from screw diameter; no separate nut hole diameter.
- Head side reuses `screw_way_on_face` exactly like `Screw` (head pocket/washer parameters).
- Opposite side gets `screw_way_on_plane` plus the round blind insert hole.

## Todo
- [x] TabProperties type and defaults
- [x] ScrewInNut geometry and dispatch
- [x] ScrewInNut UI and dropdown
- [x] FreeCAD preference defaults
- [x] Preset known properties/documentation
- [x] Syntax checks
- [ ] Manual FreeCAD test
