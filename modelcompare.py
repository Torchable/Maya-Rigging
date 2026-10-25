# Model Compare
#
# A window that checks whether a referenced model is up to date with an imported model by comparing
# the vertex count of every piece of geometry, and transfers skin weights from the imported model
# onto the referenced model.
#
# Written for Maya 2026 (Python 3). To use, drag the .py file into your Maya scene or run it from the Script Editor.
#   1. Select the group that holds the referenced geometry and press "Load Selected" next to Referenced Group.
#   2. Select the group that holds the imported geometry and press "Load Selected" next to Imported Group.
#   3. Press "Compare Vertex Count". Results show in the window and print to the Script Editor.
#   4. Press "Transfer Skin Weights" to copy the skin from each imported mesh onto the referenced mesh with the same name.
#
# Geometry is matched by name with namespaces ignored, so "charRig:body_GEO" matches "body_GEO".

import maya.cmds as cmds
import maya.mel as mm

WINDOW = 'modelCompareWin'
REF_FIELD = 'mc_refGroupField'
IMP_FIELD = 'mc_impGroupField'
SURFACE_MENU = 'mc_surfaceMenu'
OUTPUT = 'mc_outputField'

# Option menu label : copySkinWeights surfaceAssociation value
SURFACE_OPTIONS = {
    'Closest Point': 'closestPoint',
    'Closest Component': 'closestComponent',
    'Ray Cast': 'rayCast',
}


#Removes the DAG path and any namespaces from a node name ("|grp|rig:body_GEO" -> "body_GEO")
def strip_namespace(name):
    return name.split('|')[-1].split(':')[-1]


#Writes results to the window and the Script Editor
def log(lines):
    for line in lines:
        print(line)
    if cmds.scrollField(OUTPUT, exists=True):
        cmds.scrollField(OUTPUT, edit=True, text='\n'.join(lines))


#Puts the selected group into a text field
def load_selected(field):
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.warning('Select the group that holds the geometry first.')
        return
    cmds.textField(field, edit=True, text=selection[0])


#Reads both group fields and makes sure they are usable
def get_groups():
    ref_group = cmds.textField(REF_FIELD, query=True, text=True).strip()
    imp_group = cmds.textField(IMP_FIELD, query=True, text=True).strip()

    for label, group in (('Referenced', ref_group), ('Imported', imp_group)):
        if not group:
            cmds.warning('Load a group into the {} Group field.'.format(label))
            return None
        if not cmds.objExists(group):
            cmds.warning('{} group "{}" does not exist.'.format(label, group))
            return None
        if len(cmds.ls(group)) > 1:
            cmds.warning('More than one node is named "{}". Reload the {} group.'.format(group, label))
            return None

    if cmds.ls(ref_group, long=True) == cmds.ls(imp_group, long=True):
        cmds.warning('The Referenced and Imported groups are the same node.')
        return None

    return ref_group, imp_group


#Finds every mesh under a group. Returns {name without namespace: transform} and any names found twice
def get_meshes(group):
    meshes = {}
    duplicates = []
    shapes = cmds.listRelatives(group, allDescendents=True, type='mesh', noIntermediate=True, fullPath=True) or []
    for shape in shapes:
        transform = cmds.listRelatives(shape, parent=True, fullPath=True)[0]
        name = strip_namespace(transform)
        if name in meshes:
            if meshes[name] != transform and name not in duplicates:
                duplicates.append(name)
            continue
        meshes[name] = transform
    return meshes, duplicates


#Collects the geometry from both groups, plus any warnings worth showing
def collect_geometry(ref_group, imp_group):
    ref_meshes, ref_dupes = get_meshes(ref_group)
    imp_meshes, imp_dupes = get_meshes(imp_group)

    notes = []
    if not cmds.referenceQuery(ref_group, isNodeReferenced=True):
        notes.append('Note: "{}" is not from a reference.'.format(ref_group))
    if cmds.referenceQuery(imp_group, isNodeReferenced=True):
        notes.append('Note: "{}" is from a reference, not imported.'.format(imp_group))
    for name in ref_dupes:
        notes.append('Note: more than one "{}" in the referenced group, only the first was used.'.format(name))
    for name in imp_dupes:
        notes.append('Note: more than one "{}" in the imported group, only the first was used.'.format(name))

    return ref_meshes, imp_meshes, notes


def vertex_count(transform):
    return cmds.polyEvaluate(transform, vertex=True)


#Compares the vertex count of every matching piece of geometry
def compare_models(*args):
    groups = get_groups()
    if not groups:
        return
    ref_meshes, imp_meshes, notes = collect_geometry(*groups)

    matching_names = sorted(set(ref_meshes) & set(imp_meshes))
    only_in_ref = sorted(set(ref_meshes) - set(imp_meshes))
    only_in_imp = sorted(set(imp_meshes) - set(ref_meshes))

    mismatched = []
    for name in matching_names:
        ref_count = vertex_count(ref_meshes[name])
        imp_count = vertex_count(imp_meshes[name])
        if ref_count != imp_count:
            mismatched.append('    {}  (Referenced: {}  |  Imported: {})'.format(name, ref_count, imp_count))

    lines = []
    if not ref_meshes or not imp_meshes:
        lines.append('No geometry found in the {} group.'.format('referenced' if not ref_meshes else 'imported'))
    elif not mismatched and not only_in_ref and not only_in_imp:
        lines.append('Model is up to date')
    else:
        lines.append('Model is NOT up to date')
        if mismatched:
            lines.append('')
            lines.append('Vertex count does not match ({}):'.format(len(mismatched)))
            lines.extend(mismatched)
        if only_in_ref:
            lines.append('')
            lines.append('Only in the referenced model ({}):'.format(len(only_in_ref)))
            lines.extend('    ' + name for name in only_in_ref)
        if only_in_imp:
            lines.append('')
            lines.append('Only in the imported model ({}):'.format(len(only_in_imp)))
            lines.extend('    ' + name for name in only_in_imp)

    if notes:
        lines.append('')
        lines.extend(notes)
    log(lines)


def find_skin_cluster(transform):
    return mm.eval('findRelatedSkinCluster "{}"'.format(transform))


#Adds any influences the source skin has that the destination skin is missing (matched by name without namespace)
def add_missing_influences(src_skin, dst_skin):
    dst_influences = cmds.skinCluster(dst_skin, query=True, influence=True) or []
    dst_names = [strip_namespace(influence) for influence in dst_influences]
    for influence in cmds.skinCluster(src_skin, query=True, influence=True) or []:
        if influence in dst_influences or strip_namespace(influence) in dst_names:
            continue
        cmds.skinCluster(dst_skin, edit=True, addInfluence=influence, weight=0)


#Binds the referenced mesh to the same joints and settings as the imported mesh's skin
def bind_like(src_skin, transform, name):
    influences = cmds.skinCluster(src_skin, query=True, influence=True) or []
    joints = cmds.ls(influences, type='joint')
    if not joints:
        raise RuntimeError('the imported skinCluster "{}" has no joint influences'.format(src_skin))
    return cmds.skinCluster(
        joints, transform,
        toSelectedBones=True,
        bindMethod=0,
        skinMethod=cmds.skinCluster(src_skin, query=True, skinMethod=True),
        maximumInfluences=cmds.skinCluster(src_skin, query=True, maximumInfluences=True),
        obeyMaxInfluences=cmds.skinCluster(src_skin, query=True, obeyMaxInfluences=True),
        normalizeWeights=1,
        name=name + '_skinCluster')[0]


#Copies skin weights from each imported mesh to the referenced mesh with the same name
def transfer_skin_weights(*args):
    groups = get_groups()
    if not groups:
        return
    ref_meshes, imp_meshes, notes = collect_geometry(*groups)
    surface = SURFACE_OPTIONS[cmds.optionMenu(SURFACE_MENU, query=True, value=True)]

    matching_names = sorted(set(ref_meshes) & set(imp_meshes))
    if not matching_names:
        log(['No geometry with matching names was found, nothing was transferred.'] + notes)
        return

    transferred = []
    skipped = []
    cmds.undoInfo(openChunk=True, chunkName='transferSkinWeights')
    try:
        for name in matching_names:
            src_skin = find_skin_cluster(imp_meshes[name])
            if not src_skin:
                skipped.append('    {}  (imported mesh has no skinCluster)'.format(name))
                continue
            try:
                dst_skin = find_skin_cluster(ref_meshes[name])
                if not dst_skin:
                    dst_skin = bind_like(src_skin, ref_meshes[name], name)
                add_missing_influences(src_skin, dst_skin)
                cmds.copySkinWeights(
                    sourceSkin=src_skin,
                    destinationSkin=dst_skin,
                    noMirror=True,
                    surfaceAssociation=surface,
                    influenceAssociation=['name', 'oneToOne', 'closestJoint'])
                transferred.append('    ' + name)
            except RuntimeError as error:
                skipped.append('    {}  ({})'.format(name, str(error).strip()))
    finally:
        cmds.undoInfo(closeChunk=True)

    lines = ['Transferred skin weights to {} referenced mesh(es):'.format(len(transferred))]
    lines.extend(transferred)
    if skipped:
        lines.append('')
        lines.append('Skipped ({}):'.format(len(skipped)))
        lines.extend(skipped)
    if notes:
        lines.append('')
        lines.extend(notes)
    log(lines)


#Group field with a Load Selected button
def group_row(label, field):
    cmds.text(label=label, align='left', font='boldLabelFont')
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAttach=[(1, 'both', 0), (2, 'left', 4)])
    cmds.textField(field)
    cmds.button(label='Load Selected', width=100, command=lambda *args: load_selected(field))
    cmds.setParent('..')


def model_compare_ui():
    if cmds.window(WINDOW, exists=True):
        cmds.deleteUI(WINDOW)

    cmds.window(WINDOW, title='Model Compare', widthHeight=(440, 480), sizeable=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnAttach=('both', 10))
    cmds.separator(height=4, style='none')
    cmds.text(label='Select the group that holds the geometry, then press Load Selected.', align='left')

    group_row('Referenced Group', REF_FIELD)
    group_row('Imported Group', IMP_FIELD)

    cmds.separator(height=10, style='in')
    cmds.button(label='Compare Vertex Count', height=32, command=compare_models)

    cmds.separator(height=10, style='in')
    cmds.optionMenu(SURFACE_MENU, label='Surface Association ')
    for label in SURFACE_OPTIONS:
        cmds.menuItem(label=label)
    cmds.button(label='Transfer Skin Weights  (Imported -> Referenced)', height=32, command=transfer_skin_weights)

    cmds.separator(height=10, style='in')
    cmds.text(label='Results', align='left', font='boldLabelFont')
    cmds.scrollField(OUTPUT, editable=False, wordWrap=False, height=200)
    cmds.separator(height=4, style='none')

    cmds.showWindow(WINDOW)


model_compare_ui()
