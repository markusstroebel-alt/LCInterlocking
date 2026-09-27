from PySide import QtCore, QtGui


PLANAR_SURFACE_TYPE = "Part::GeomPlane"
OPPOSING_NORMAL_LIMIT = -0.9999


def _is_planar(face):
    surface = getattr(face, "Surface", None)
    return getattr(surface, "TypeId", None) == PLANAR_SURFACE_TYPE


def _normal_at_center(face):
    parameter_range = getattr(face, "ParameterRange", (0.0, 1.0, 0.0, 1.0))
    u_value = (parameter_range[0] + parameter_range[1]) / 2.0
    v_value = (parameter_range[2] + parameter_range[3]) / 2.0
    return face.normalAt(u_value, v_value)


def _normal_dot_product(first_normal, second_normal):
    normal_length = first_normal.Length * second_normal.Length
    if normal_length == 0.0:
        return 1.0
    return first_normal.dot(second_normal) / normal_length


def _faces_overlap(first_face, second_face, first_normal, plane_distance, tolerance):
    try:
        projected_second_face = second_face.copy()
        projected_second_face.translate(first_normal * -plane_distance)
        overlap = first_face.common(projected_second_face)
        return overlap.Area > tolerance * tolerance
    except Exception:
        return False


def _face_record(part, face, face_index):
    return {"freecad_object": part, "face": face, "name": "Face%d" % face_index}


def find_contact_faces(parts, tolerance):
    candidates = []
    for first_part_index, first_part in enumerate(parts):
        first_faces = getattr(first_part.Shape, "Faces", [])
        for second_part in parts[first_part_index + 1:]:
            second_faces = getattr(second_part.Shape, "Faces", [])
            for first_face_index, first_face in enumerate(first_faces, 1):
                if not _is_planar(first_face):
                    continue
                first_normal = _normal_at_center(first_face)
                for second_face_index, second_face in enumerate(second_faces, 1):
                    if not _is_planar(second_face):
                        continue
                    second_normal = _normal_at_center(second_face)
                    if _normal_dot_product(first_normal, _normal_at_center(second_face)) > OPPOSING_NORMAL_LIMIT:
                        continue
                    plane_distance = second_face.CenterOfMass.sub(first_face.CenterOfMass).dot(first_normal)
                    if abs(plane_distance) > tolerance:
                        continue
                    if not _faces_overlap(first_face, second_face, first_normal,
                                          plane_distance, tolerance):
                        continue
                    candidates.append({
                        "first": _face_record(first_part, first_face, first_face_index),
                        "second": _face_record(second_part, second_face, second_face_index),
                    })
    return candidates


class ContactFacesDialog(QtGui.QDialog):
    def __init__(self, candidates, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.candidates = candidates
        self.setWindowTitle("Contact faces")

        layout = QtGui.QVBoxLayout(self)
        self.table = QtGui.QTableWidget(len(candidates), 3, self)
        self.table.setHorizontalHeaderLabels(["Add", "Contact pair", "Connection on"])
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table.verticalHeader().hide()
        for row_index, candidate in enumerate(candidates):
            self._add_candidate_row(row_index, candidate)
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                         QtGui.QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _add_candidate_row(self, row_index, candidate):
        enabled_item = QtGui.QTableWidgetItem()
        enabled_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        enabled_item.setCheckState(QtCore.Qt.Checked)
        self.table.setItem(row_index, 0, enabled_item)

        first_label = self._face_label(candidate["first"])
        second_label = self._face_label(candidate["second"])
        self.table.setItem(row_index, 1, QtGui.QTableWidgetItem(
            "%s / %s" % (first_label, second_label)))

        direction_combo = QtGui.QComboBox(self.table)
        direction_combo.addItem(first_label)
        direction_combo.addItem(second_label)
        self.table.setCellWidget(row_index, 2, direction_combo)

    def _face_label(self, face):
        return "%s.%s" % (face["freecad_object"].Label, face["name"])

    def selected_faces(self):
        faces = []
        for row_index, candidate in enumerate(self.candidates):
            enabled_item = self.table.item(row_index, 0)
            if enabled_item.checkState() != QtCore.Qt.Checked:
                continue
            direction_combo = self.table.cellWidget(row_index, 2)
            candidate_key = "first" if direction_combo.currentIndex() == 0 else "second"
            faces.append(candidate[candidate_key])
        return faces