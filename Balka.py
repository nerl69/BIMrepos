               
"""
Script for IGirderReinforcement.py
"""
import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Reinforcement as AllplanReinf

from PythonPart import View2D3D, PythonPart
from StdReinfShapeBuilder.ReinforcementShapeProperties import ReinforcementShapeProperties
from StdReinfShapeBuilder.RotationAngles import RotationAngles
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder


def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True

def create_element(build_ele, doc):
    """
    Creation of element

    Args:
        build_ele: the building element.
        doc:       input document

    Returns:
            tuple  with created elements and handles
    """
    element = IGirderReinforcment(doc)

    return element.create(build_ele)


class IGirderReinforcment():
    """
    Definiton of class IGirderReinforcement
    """
    def __init__(self, doc):
        """
        Initialisation of class IGirderReinforcement
        """
        self.model_ele_list     = []
        self.handle_list        = []
        self.document           = doc

        # Set a common properties
        self.com_prop               = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()
        self.com_prop.HelpConstruction = True

    def read_geometry_values(self, build_ele):
        """
        Read palette parameter values

        Args:
            build_ele:  building element.
        """
        self.reference_point                    =  1 if build_ele.PlacementDefaultBottom.value else 0
        self.height                             = build_ele.GirderHeight.value
        self.length                             = build_ele.GirderLength.value
        self.top_flange_width                   = build_ele.TopFlangeWidth.value
        self.top_flange_thickness               = build_ele.TopFlangeThickness.value
        self.top_flange_inclination_height      = build_ele.TopFlangeInclinationHeight.value

        self.web_width                          = build_ele.WebWidth.value
        self.bottom_flange_width                = build_ele.BottomFlangeWidth.value
        self.bottom_flange_thickness            = build_ele.BottomFlangeThickness.value
        self.bottom_flange_inclination_height   = build_ele.BottomFlangeInclinationHeight.value
        self.bottom_inclination_angle           = math.atan(self.bottom_flange_inclination_height * 2 / (self.bottom_flange_width - self.web_width))

    def read_reinforcement_values(self, build_ele):
        """
        Read palette parameter values

        Args:
            build_ele:  building element.
        """

        self.concrete_grade                         = build_ele.ConcreteGrade.value
        self.steel_grade                            = build_ele.SteelGrade.value

        self.concrete_cover_start                   = build_ele.ConcreteCoverStart.value
        self.concrete_cover_end                     = build_ele.ConcreteCoverEnd.value
        self.concrete_cover_top_reinf               = build_ele.ConcreteCoverTopReinf.value
        self.concrete_cover_side_top_flange         = build_ele.ConcreteCoverSideTopFlange.value
        self.concrete_cover_web_stirrup             = build_ele.ConcreteCoverWebStirrup.value
        self.concrete_cover_bottom_reinf            = build_ele.ConcreteCoverBottomReinf.value
        self.concrete_cover_side_bottom_flange      = build_ele.ConcreteCoverSideBottomFlange.value

        #-------------------- Stirrup
        self.layer_stirrup                        = build_ele.LayerStirrup.value
        self.mark_num_top_stirrup                 = 1
        self.mark_num_web_stirrup                 = 2
        self.mark_num_bottom_stirrup              = 3

        # regions
        build_ele.RegionSevenLength.value = build_ele.GirderLength.value \
                                             - 2 * (build_ele.RegionOneLength.value \
                                                + build_ele.RegionTwoLength.value \
                                                + build_ele.RegionThreeLength.value \
                                                + build_ele.RegionFourLength.value \
                                                + build_ele.RegionFiveLength.value \
                                                + build_ele.RegionSixLength.value
                                             )

        self.region_length_list = []
        self.region_length_list.append(build_ele.RegionOneLength.value)
        self.region_length_list.append(build_ele.RegionTwoLength.value)
        self.region_length_list.append(build_ele.RegionThreeLength.value)
        self.region_length_list.append(build_ele.RegionFourLength.value)
        self.region_length_list.append(build_ele.RegionFiveLength.value)
        self.region_length_list.append(build_ele.RegionSixLength.value)
        self.region_length_list.append(build_ele.RegionSevenLength.value)

        self.region_spacing_stirrup_list = []
        self.region_spacing_stirrup_list.append(build_ele.RegionOneStirrupSpacing.value)
        self.region_spacing_stirrup_list.append(build_ele.RegionTwoStirrupSpacing.value)
        self.region_spacing_stirrup_list.append(build_ele.RegionThreeStirrupSpacing.value)
        self.region_spacing_stirrup_list.append(build_ele.RegionFourStirrupSpacing.value)
        self.region_spacing_stirrup_list.append(build_ele.RegionFiveStirrupSpacing.value)
        self.region_spacing_stirrup_list.append(build_ele.RegionSixStirrupSpacing.value)
        self.region_spacing_stirrup_list.append(build_ele.RegionSevenStirrupSpacing.value)

        self.region_spacing_web_list = []
        self.region_spacing_web_list.append(build_ele.RegionOneWebSpacing.value)
        self.region_spacing_web_list.append(build_ele.RegionTwoWebSpacing.value)
        self.region_spacing_web_list.append(build_ele.RegionThreeWebSpacing.value)
        self.region_spacing_web_list.append(build_ele.RegionFourWebSpacing.value)
        self.region_spacing_web_list.append(build_ele.RegionFiveWebSpacing.value)
        self.region_spacing_web_list.append(build_ele.RegionSixWebSpacing.value)
        self.region_spacing_web_list.append(build_ele.RegionSevenWebSpacing.value)

        self.top_stirrup                          = build_ele.TopStirrupCheckBox.value
        self.diameter_top_stirrup                 = build_ele.DiameterTopStirrup.value
        
        self.web_stirrup                          = build_ele.WebStirrupCheckBox.value
        self.diameter_web_stirrup                 = build_ele.DiameterWebStirrup.value
        self.anchorage_web_stirrup                = build_ele.AnchorageLengthWebStirrup.value
        self.hook_length_web_stirrup              = build_ele.HookLengthWebStirrup.value
        self.hook_angle_web_stirrup               = build_ele.HookAngleWebStirrup.value

        self.bottom_stirrup                       = build_ele.BottomStirrupCheckBox.value
        self.diameter_bottom_stirrup              = build_ele.DiameterBottomStirrup.value
        self.hook_length_bottom_stirrup           = build_ele.HookLengthBottomStirrup.value
        self.hook_angle_bottom_stirrup            = 2 * math.degrees(self.bottom_inclination_angle)        

        # -------------------- Longitudinal
        self.layer_long_reinf                     = build_ele.LayerLongitudinal.value
        self.top_long_reinf                       = build_ele.TopLongReinfCheckBox.value
        self.bottom_long_reinf                    = build_ele.BottomLongReinfCheckBox.value

        self.mark_num_top_long_reinf              = 4
        self.diameter_top_long_reinf              = build_ele.DiameterTopFlangeReinf.value
        self.count_top_long_reinf                 = build_ele.NumberTopFlangeReinf.value
        self.spacing_top_long_reinf               = build_ele.SpacingTopFlangeReinf.value

        self.mark_num_bottom_long_reinf           = 5
        self.diameter_bottom_long_reinf           = build_ele.DiameterBottomFlangeReinf.value
        self.count_bottom_long_reinf              = build_ele.NumberBottomFlangeReinf.value
        self.spacing_bottom_long_reinf            = build_ele.SpacingBottomFlangeReinf.value

    def create_reinf_common_prop(self, layer):
        """
        Create reinforcement common properties

        Args:
            layer:      Layer

        Returns:
            Common properties
        """

        com_prop = AllplanBaseElements.CommonProperties()

        com_prop.GetGlobalProperties()

        com_prop.Layer = layer

        return com_prop

    def create(self, build_ele):
        """
        Create elements

        Args:
            build_ele:  building element.

        Returns:
            Tuple with created elements and handles
        """
        self.read_geometry_values(build_ele)
        self.read_reinforcement_values(build_ele)

        # create the geometry
        girder_ele = self.create_geometry()
        views = [View2D3D ([girder_ele])]

        # create reinforcement
        reinf_ele_list = []

        reinf_ele_list.extend(self.create_top_stirrup())
        reinf_ele_list.extend(self.create_web_stirrup())
        reinf_ele_list.extend(self.create_bottom_stirrup())
        reinf_ele_list.extend(self.create_top_long_reinf())
        reinf_ele_list.extend(self.create_bottom_long_reinf())

        pythonpart = PythonPart (build_ele.pyp_file_name,
                                    parameter_list   = build_ele.get_params_list(),
                                    hash_value       = build_ele.get_hash(),
                                    python_file      = build_ele.pyp_file_name,
                                    views            = views,
                                    common_props     = self.com_prop,
                                    reinforcement    = reinf_ele_list,
                                    attribute_list   = [])

        self.model_ele_list = pythonpart.create()

        # Transformation model elements
        self.transform_model(self.model_ele_list)

        return (self.model_ele_list, self.handle_list)

    def create_geometry(self):
        """
        Create geometry

        Returns:
            Model element.
        """
        web_height = self.height - self.top_flange_thickness - self.top_flange_inclination_height \
                     - self.bottom_flange_inclination_height - self.bottom_flange_thickness

        # Frist-polygon
        traverse1 = AllplanGeo.Polygon3D()
        traverse1 += AllplanGeo.Point3D(0, -0.5 * self.bottom_flange_width, 0)
        traverse1 += AllplanGeo.Point3D(0, 0.5 * self.bottom_flange_width, 0)
        traverse1 += AllplanGeo.Point3D(0, 0.5 * self.bottom_flange_width, self.bottom_flange_thickness)
        traverse1 += AllplanGeo.Point3D(0, 0.5 * self.web_width, self.bottom_flange_thickness + self.bottom_flange_inclination_height)
        traverse1 += AllplanGeo.Point3D(0, 0.5 * self.web_width, self.bottom_flange_thickness + self.bottom_flange_inclination_height + web_height)
        traverse1 += AllplanGeo.Point3D(0, 0.5 * self.top_flange_width, self.height - self.top_flange_thickness)
        traverse1 += AllplanGeo.Point3D(0, 0.5 * self.top_flange_width, self.height)
        traverse1 += AllplanGeo.Point3D(0, -0.5 * self.top_flange_width, self.height)
        traverse1 += AllplanGeo.Point3D(0, -0.5 * self.top_flange_width, self.height - self.top_flange_thickness)
        traverse1 += AllplanGeo.Point3D(0, -0.5 * self.web_width, self.bottom_flange_thickness + self.bottom_flange_inclination_height + web_height)
        traverse1 += AllplanGeo.Point3D(0, -0.5 * self.web_width, self.bottom_flange_thickness + self.bottom_flange_inclination_height)
        traverse1 += AllplanGeo.Point3D(0, -0.5 * self.bottom_flange_width, self.bottom_flange_thickness)
        traverse1 += AllplanGeo.Point3D(0, -0.5 * self.bottom_flange_width, 0)

        # Second-polygon
        traverse2 = AllplanGeo.Polygon3D()
        traverse2 += AllplanGeo.Point3D(self.length, -0.5 * self.bottom_flange_width, 0)
        traverse2 += AllplanGeo.Point3D(self.length, 0.5 * self.bottom_flange_width, 0)
        traverse2 += AllplanGeo.Point3D(self.length, 0.5 * self.bottom_flange_width, self.bottom_flange_thickness)
        traverse2 += AllplanGeo.Point3D(self.length, 0.5 * self.web_width, self.bottom_flange_thickness + self.bottom_flange_inclination_height)
        traverse2 += AllplanGeo.Point3D(self.length, 0.5 * self.web_width, self.bottom_flange_thickness + self.bottom_flange_inclination_height + web_height)
        traverse2 += AllplanGeo.Point3D(self.length, 0.5 * self.top_flange_width, self.height - self.top_flange_thickness)
        traverse2 += AllplanGeo.Point3D(self.length, 0.5 * self.top_flange_width, self.height)
        traverse2 += AllplanGeo.Point3D(self.length, -0.5 * self.top_flange_width, self.height)
        traverse2 += AllplanGeo.Point3D(self.length, -0.5 * self.top_flange_width, self.height - self.top_flange_thickness)
        traverse2 += AllplanGeo.Point3D(self.length, -0.5 * self.web_width, self.bottom_flange_thickness + self.bottom_flange_inclination_height + web_height)
        traverse2 += AllplanGeo.Point3D(self.length, -0.5 * self.web_width, self.bottom_flange_thickness + self.bottom_flange_inclination_height)
        traverse2 += AllplanGeo.Point3D(self.length, -0.5 * self.bottom_flange_width, self.bottom_flange_thickness)
        traverse2 += AllplanGeo.Point3D(self.length, -0.5 * self.bottom_flange_width, 0)

        # Create the final polyhedron
        err, polyhedron = AllplanGeo.CreatePolyhedron(traverse1, traverse2)
        if err:
            return

        girder_ele = AllplanBasisElements.ModelElement3D(self.com_prop, polyhedron)

        return girder_ele

    def place_stirrup(self, profile, shape_props, type='NONE'):
        """
        place stirrup

        Args:
            profile:            stirrup profile
            shape_props:        shape properties
            type:               stirrup type

        Returns: 
            Reinforcement list.
        """
        reinf_list = []
        region_spacing_list = self.region_spacing_stirrup_list

        rotation_matrix = AllplanGeo.Matrix3D()

        rot_angle = AllplanGeo.Angle()
        rot_angle.SetDeg(90)
        rotation_matrix.Rotation(AllplanGeo.Line3D(
                                     AllplanGeo.Point3D(),
                                     AllplanGeo.Point3D(0, 1000, 0)),
                                     rot_angle)

        # define shape
        shape_builder = AllplanReinf.ReinforcementShapeBuilder(rotation_matrix)

        # fill up a list of points / concrete_cover values
        point_concrete_tuple_list = []
        for index in range(profile.Count()):
            point_concrete_tuple_list.append((profile[index], 0 ))

        shape_builder.AddPoints(point_concrete_tuple_list)

        mark_num = self.mark_num_top_stirrup

        if type == "WEB":
            mark_num = self.mark_num_web_stirrup
            region_spacing_list = self.region_spacing_web_list

            if self.hook_length_web_stirrup: # add hook
               
                try:
                    sgn = profile.GetStartPoint().Y / abs(profile.GetStartPoint().Y)
                except ZeroDivisionError:
                    sgn = 1

                shape_builder.SetHookEnd(self.hook_length_web_stirrup, 
                                         sgn * self.hook_angle_web_stirrup,
                                         AllplanReinf.HookType.eAnchorage)
        
        elif type == "BOTTOM":
            mark_num = self.mark_num_bottom_stirrup

            if self.hook_length_bottom_stirrup: # add hook
                shape_builder.SetHookStart(self.hook_length_bottom_stirrup, 
                                            self.hook_angle_bottom_stirrup,
                                            AllplanReinf.HookType.eAnchorage)

                shape_builder.SetHookEnd(self.hook_length_bottom_stirrup, 
                                            self.hook_angle_bottom_stirrup,
                                            AllplanReinf.HookType.eAnchorage)
            
        shape = shape_builder.CreateStirrup(shape_props, AllplanReinf.StirrupType.FullCircle)

        if shape.IsValid():

            i = 0
            len_sum = 0
            start_cover_factor = 1
            end_cover_factor = 1
            len_sum_factor_start = 0
            len_sum_factor_end = 0

            while i < len(self.region_length_list):

                if i == 6: # midspan
                    reinforcement = LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                        mark_num,
                        shape,
                        AllplanGeo.Point3D(len_sum_factor_start * len_sum + start_cover_factor * self.concrete_cover_start, 0, 0),
                        AllplanGeo.Point3D(self.length - len_sum_factor_end * len_sum - end_cover_factor * self.concrete_cover_end, 0, 0),
                        0, 0, region_spacing_list[i])

                    reinf_list.append(reinforcement)

                else:
                    if self.concrete_cover_start < len_sum + self.region_length_list[i]: # first half
                        reinforcement = LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                            mark_num,
                            shape,
                            AllplanGeo.Point3D(len_sum_factor_start * len_sum + start_cover_factor * self.concrete_cover_start, 0, 0),
                            AllplanGeo.Point3D(len_sum + self.region_length_list[i], 0, 0),
                            0, 0, region_spacing_list[i])

                        reinf_list.append(reinforcement)
                        start_cover_factor = 0
                        len_sum_factor_start = 1

                    if  self.concrete_cover_end < len_sum + self.region_length_list[i]: # second half
                        reinforcement = LinearBarBuilder.create_linear_bar_placement_from_to_by_dist(
                            mark_num,
                            shape,
                            AllplanGeo.Point3D(self.length - len_sum - self.region_length_list[i], 0, 0),
                            AllplanGeo.Point3D(self.length - len_sum_factor_end * len_sum - end_cover_factor * self.concrete_cover_end, 0, 0),
                            0, 0, region_spacing_list[i])

                        reinf_list.append(reinforcement)
                        end_cover_factor = 0
                        len_sum_factor_end = 1

                    len_sum += self.region_length_list[i]

                i += 1

        for reinforcement in reinf_list:
            reinforcement.SetCommonProperties(self.create_reinf_common_prop(self.layer_stirrup))

        return reinf_list

    def create_top_profile(self):
        """
        Create top stirrup profile

        Returns:
            Polyline.
        """
        stirrup_cover = self.concrete_cover_top_reinf - 0.5 * self.diameter_top_long_reinf - 0.5 * self.diameter_top_stirrup

        profile = AllplanGeo.Polygon3D()
        profile += AllplanGeo.Point3D(0, 0.5 * self.top_flange_width - self.concrete_cover_side_top_flange, self.height - stirrup_cover)
        profile += AllplanGeo.Point3D(0, -0.5 * self.top_flange_width + self.concrete_cover_side_top_flange, self.height - stirrup_cover)

        return profile

    def create_top_stirrup(self):
        """
        Create top stirrup

        Returns:
            Reinforcement list.
        """
        if not self.top_stirrup:
            return []

        # get the profile
        profile = self.create_top_profile()

        # define shape properties
        shape_props = ReinforcementShapeProperties.rebar(self.diameter_top_stirrup,
                                                        -1, self.steel_grade,
                                                        self.concrete_grade,
                                                        AllplanReinf.BendingShapeType.Freeform)

        reinf_list = self.place_stirrup(profile, shape_props, 'TOP')

        return reinf_list

    def create_web_profile(self):
        """
        Create web stirrup profile

        Returns:
            Polyline.
        """
        stirrup_cover = self.concrete_cover_bottom_reinf - 0.5 * self.diameter_web_stirrup - 0.5 * self.diameter_bottom_long_reinf

        profiles = []

        profile = AllplanGeo.Polygon3D()
        profile += AllplanGeo.Point3D(0, 0.5 * self.bottom_flange_width - self.concrete_cover_web_stirrup, \
            self.bottom_flange_thickness - self.concrete_cover_side_bottom_flange)
        profile += AllplanGeo.Point3D(0, 0.5 * self.bottom_flange_width - self.concrete_cover_web_stirrup, stirrup_cover)
        profile += AllplanGeo.Point3D(0, -0.5 * self.web_width + self.concrete_cover_web_stirrup, stirrup_cover)
        profile += AllplanGeo.Point3D(0, -0.5 * self.web_width + self.concrete_cover_web_stirrup, self.height + self.anchorage_web_stirrup)
        profiles.append(profile)

        profile = AllplanGeo.Polygon3D()
        profile += AllplanGeo.Point3D(0, -0.5 * self.bottom_flange_width + self.concrete_cover_web_stirrup, \
            self.bottom_flange_thickness - self.concrete_cover_side_bottom_flange)
        profile += AllplanGeo.Point3D(0, -0.5 * self.bottom_flange_width + self.concrete_cover_web_stirrup, stirrup_cover)
        profile += AllplanGeo.Point3D(0, 0.5 * self.web_width - self.concrete_cover_web_stirrup, stirrup_cover)
        profile += AllplanGeo.Point3D(0, 0.5 * self.web_width - self.concrete_cover_web_stirrup, self.height + self.anchorage_web_stirrup)
        profiles.append(profile)

        return profiles

    def create_web_stirrup(self):
        """
        Create web stirrup

        Returns:
            Reinforcement list.
        """
        reinf_list = []
        if not self.web_stirrup:
            return []

        # get the profile
        profiles = self.create_web_profile()

        # define shape properties
        shape_props = ReinforcementShapeProperties.rebar(self.diameter_web_stirrup,
                                                        -1, self.steel_grade,
                                                        self.concrete_grade,
                                                        AllplanReinf.BendingShapeType.Freeform)

        # additional offest for the web, in order to avoid collisions.
        add_offset = 0.5 * self.diameter_web_stirrup

        if self.diameter_bottom_stirrup > self.diameter_top_stirrup or self.hook_length_bottom_stirrup:
            add_offset += 1.5 * self.diameter_bottom_stirrup
        else:
            add_offset += 0.5 * self.diameter_top_stirrup

        for profile in profiles:
            reinf_list.extend(self.place_stirrup(profile, shape_props, 'WEB'))

        return reinf_list

    def create_bottom_profile(self):
        """
        Create bottom stirrup profile

        Returns:
            Polyline.
        """
        stirrup_cover = self.concrete_cover_web_stirrup

        profile = AllplanGeo.Polygon3D()
        profile += AllplanGeo.Point3D(0, 0.5 * self.bottom_flange_width - stirrup_cover, stirrup_cover)
        profile += AllplanGeo.Point3D(0, 0.5 * self.bottom_flange_width - stirrup_cover, \
            self.bottom_flange_thickness - stirrup_cover)
        profile += AllplanGeo.Point3D(0, 0, \
            self.bottom_flange_thickness - stirrup_cover \
                + math.tan(self.bottom_inclination_angle) * (0.5 * self.bottom_flange_width - stirrup_cover))
        profile += AllplanGeo.Point3D(0, -0.5 * self.bottom_flange_width + stirrup_cover, \
            self.bottom_flange_thickness - stirrup_cover)
        profile += AllplanGeo.Point3D(0, -0.5 * self.bottom_flange_width + stirrup_cover, stirrup_cover)

        return profile

    def create_bottom_stirrup(self):
        """
        Create bottom stirrup

        Returns:
            Reinforcement list.
        """
        reinf_list = []
        if not self.bottom_stirrup:
            return []
    
        # get the profile
        profile = self.create_bottom_profile()

        # define shape properties
        shape_props = ReinforcementShapeProperties.rebar(self.diameter_bottom_stirrup,
                                                        -1, self.steel_grade,
                                                        self.concrete_grade,
                                                        AllplanReinf.BendingShapeType.Freeform)

        reinf_list.extend(self.place_stirrup(profile, shape_props))

        return reinf_list

    def place_longitudinal_reinforcement(self, shape, placement_pos="bottom"):
        """
        Place longitudinal reinforcment

        Args:
            shape:              rebar shape
            placement_pos:     (string) placement position

        Returns:
            Reinforcement list.
        """
        if placement_pos == "top":
            diameter            = self.diameter_top_long_reinf
            flange_width        = self.top_flange_width
            spacing             = self.spacing_top_long_reinf
            reinf_count         = self.count_top_long_reinf
            mark_num            = self.mark_num_top_long_reinf
            placement_offset    = self.height - self.concrete_cover_top_reinf
            placement_direction = -1
            to_point            = AllplanGeo.Point3D(0, 0.5 * flange_width - self.concrete_cover_side_top_flange, 0)

        else:
            diameter            = self.diameter_bottom_long_reinf
            flange_width        = self.bottom_flange_width
            spacing             = self.spacing_bottom_long_reinf
            reinf_count         = self.count_bottom_long_reinf
            mark_num            = self.mark_num_bottom_long_reinf
            placement_offset    = self.concrete_cover_bottom_reinf
            placement_direction = 1
            to_point            = AllplanGeo.Point3D(0, 0.5 * flange_width - self.concrete_cover_side_bottom_flange, 0)

        reinf_list = []

        from_point = AllplanGeo.Point3D(0,
                            0.5 * self.web_width - self.concrete_cover_web_stirrup \
                                + self.diameter_web_stirrup + 0.5 * diameter,
                            0)

        per_layer_reinf_count = 2 * math.floor( from_point.GetDistance(to_point) / spacing + 1)

        number_reinf_layers = math.ceil( reinf_count / per_layer_reinf_count)

        j = 0

        while j < number_reinf_layers:

            # -------- right section
            start_shape_right = AllplanReinf.BendingShape(shape)
            start_point = from_point + AllplanGeo.Point3D(0, 0, placement_offset + placement_direction * j * spacing)
            start_shape_right.Move(AllplanGeo.Vector3D(start_point))

            # computing this (i-th) layer's reinf count            
            remaining_count = reinf_count - j * per_layer_reinf_count
            this_layer_count = per_layer_reinf_count if per_layer_reinf_count < remaining_count else remaining_count

            count_right = math.ceil(this_layer_count / 2)

            to_point = from_point + AllplanGeo.Point3D(0, count_right * spacing, 0)

            reinforcement = AllplanReinf.BarPlacement(mark_num,
                                    count_right,
                                    AllplanGeo.Vector3D(0, spacing, 0),
                                    from_point,
                                    to_point,
                                    start_shape_right)

            reinforcement.SetCommonProperties(self.create_reinf_common_prop(self.layer_long_reinf))
            reinf_list.append(reinforcement)

            # -------- left section 
            start_shape_left = AllplanReinf.BendingShape(shape)
            start_point = AllplanGeo.Point3D(0, 0, placement_offset + placement_direction * j * spacing) - from_point
            start_shape_left.Move(AllplanGeo.Vector3D(start_point))

            count_left = this_layer_count - count_right

            to_point = from_point + AllplanGeo.Point3D(0, count_left * spacing, 0)

            reinforcement = AllplanReinf.BarPlacement(mark_num,
                                    count_left, 
                                    AllplanGeo.Vector3D(0, -spacing, 0),
                                    from_point,
                                    to_point,
                                    start_shape_left)

            reinforcement.SetCommonProperties(self.create_reinf_common_prop(self.layer_long_reinf))
            reinf_list.append(reinforcement)

            j += 1 

        return reinf_list

    def create_bottom_long_reinf(self):
        """
        Create bottom longitudinal reinforcment

        Returns:
            Reinforcement list.
        """
        if not self.bottom_long_reinf:
            return [] 

        reinf_list = []
        bendingroller = -1

        shape_props = ReinforcementShapeProperties.rebar(self.diameter_bottom_long_reinf, bendingroller,
                                                         self.steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        # --------- shape
        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints([(AllplanGeo.Point2D(0, 0), self.concrete_cover_start),
                            (AllplanGeo.Point2D(self.length, 0), 0),
                            (self.concrete_cover_end)])

        shape = shape_builder.CreateShape(shape_props)

        model_angles = RotationAngles(90, 0, 0)
        shape.Rotate(model_angles)

        # --------- reinforcement placement
        reinf_list.extend(self.place_longitudinal_reinforcement(shape))
               
        return reinf_list

    def create_top_long_reinf(self):
        """
        Create top longitudinal reinforcment

        Returns:
            Reinforcement list.
        """
        if not self.top_long_reinf:
            return [] 

        reinf_list = []
        bendingroller = -1

        shape_props = ReinforcementShapeProperties.rebar(self.diameter_top_long_reinf, bendingroller,
                                                         self.steel_grade, -1,
                                                         AllplanReinf.BendingShapeType.LongitudinalBar)

        # --------- shape
        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints([(AllplanGeo.Point2D(0, 0), self.concrete_cover_start),
                            (AllplanGeo.Point2D(self.length, 0), 0),
                            (self.concrete_cover_end)])

        shape = shape_builder.CreateShape(shape_props)

        model_angles = RotationAngles(90, 0, 0)
        shape.Rotate(model_angles)

        # --------- reinforcement placement     
        reinf_list.extend(self.place_longitudinal_reinforcement(shape, placement_pos="top"))
           
        return reinf_list

    def transform_model(self, ele):
        """
        Transform the model to the a new position
    
        Args:
            ele:    element to be transformed
        """
        if self.reference_point == 0: # where 1 = bottom, 0 = Top
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, 0, -self.height),
                                        0, 0, 0,
                                        ele)
