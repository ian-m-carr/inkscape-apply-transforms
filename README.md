# inkscape-apply-transforms
Simple plugin to recursively apply transforms to an inkscape 'group' or 'layer'

Two options enable:
apply-to-paths: applying transforms to path elements, which will result in trasform free paths
apply-to_shapes: replaces circles, ellipses, rectangles etc with path elements and applies the transforms to these.

The resultant document will then contain 'clean' groups and optionally paths with no transforms, but in the same location as previously.

The code is equivalent to the inkex.elements._groups.GroupBase.bake_transforms_recursively documented as new in version 1.4 (shipped with the 1.3 beta release?) 
But with the addition of the shape to path substitution and transforms. The code should be useable with version 1.2. and 1.3.x
