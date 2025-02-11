from Module.DB import *
from Device_Placer import BStarTreeNode
from Device_Placer import Simulated_Annealing as sa 
import copy

def device_placement(circuit: Circuit) -> None:
    """
    @brief: device placement of the instance
    @param: tech -> Technology object
    @param: circuit -> Circuit object
    """
    modules = []

    # get the layout and pin information of the instances
    for group_id in circuit.group:
        inst: Group = circuit.group[group_id]
        
        # boundary of the instances [x0, x1, y0, y1]
        height = inst.boundary.y[1] - inst.boundary.y[0]
        width  = inst.boundary.x[1] - inst.boundary.x[0]

        # create the bstar tree node
        modules.append(BStarTreeNode(group_id, width, height, copy.deepcopy(inst.pin)))

    # placement of the modules
    tree = sa.optimal_simulated_annealing(modules, circuit.port, 100, 1, 10000) # orig 20000

    # get width and height of the floorplan
    for module in tree.get_modules():
        # if module x1 larger than width, update width
        if module.x + module.width > circuit.width:
            circuit.width = module.x + module.width

        # if module y1 larger than height, update height
        if module.y + module.height > circuit.height:
            circuit.height = module.y + module.height

    print("Update Floorplan... width:", circuit.width, "height:", circuit.height)

    # update the instance layout
    for module in tree.get_modules():
        inst = circuit.group[module.name]

        # get the reference position by subtracting the movement from the original position
        ref_x = module.x - inst.boundary.x[0]
        ref_y = module.y - inst.boundary.y[0]

        # loop through each layers
        for layer in inst.shape:
            # loop through each shapes
            for shape in inst.shape[layer]:
                # update the BOX shape position by adding the reference position
                if isinstance(shape, Box):
                    shape.x = [shape.x[0] + ref_x, shape.x[1] + ref_x]
                    shape.y = [shape.y[0] + ref_y, shape.y[1] + ref_y]

                # update the TEXT shape position by adding the reference position
                elif isinstance(shape, Text):
                    shape.x = shape.x + ref_x
                    shape.y = shape.y + ref_y

                # update the SREF shape position by adding the reference position
                elif isinstance(shape, SRef):
                    shape.x = shape.x + ref_x
                    shape.y = shape.y + ref_y

        # loop through each pins
        for pin in inst.pin:
            # update the pin position by adding the reference position
            pin.pt1 = [pin.pt1[0] + ref_x, pin.pt1[1] + ref_y]
            pin.pt2 = [pin.pt2[0] + ref_x, pin.pt2[1] + ref_y]
    

def port_placement(tech: Tech, circuit: Circuit) -> None:
    """
    @brief: port placement
    """
    # design rules
    m1_width = tech.min_width_rule["metal1"]
    m1_area = tech.min_area_rule["metal1"]
    m1_extend = m1_area / (2 * m1_width)
    m1_x_pitch = 2*tech.min_width_rule["metal1"] + 2*tech.min_enclosure_rule[("metal1","via12")] + tech.min_spacing_rule[("metal1","metal1")]
    m1_y_pitch = 2*tech.min_width_rule["metal1"] + 2*tech.min_enclosure_rule[("metal1","via12","end")] + tech.min_spacing_rule[("metal1","metal1")]


    # get the width and height of the instance
    width  = circuit.width
    height = circuit.height
    
    count = {"top-full": 0, "bottom-full": 0, "left-full": 0, "right-full": 0, 
             "top": 0, "bottom": 0, "left": 0, "right": 0, 
             "top-left": 0, "left-top": 0, "top-right": 0, "right-top": 0, 
             "bottom-left": 0, "left-bottom": 0, "bottom-right": 0, "right-bottom": 0}
    
    # calculate the ports coordinates
    for name in circuit.port:
        x0, x1, y0, y1 = 0, 0, 0, 0

        # full
        if circuit.port[name].position == "top-full":
            top = height + count["top-full"] * m1_y_pitch
            x0, x1 = 0 - m1_width, width + m1_width
            y0, y1 = top - m1_width, top + m1_width

            count["top-full"] += 1

        elif circuit.port[name].position == "bottom-full":
            btm = 0 - count["bottom-full"] * m1_y_pitch
            x0, x1 = 0 - m1_width, width + m1_width
            y0, y1 = btm - m1_width, btm + m1_width 

            count["bottom-full"] += 1

        elif circuit.port[name].position == "left-full":
            left = 0 - count["left-full"] * m1_x_pitch
            x0, x1 = left - m1_width, left + m1_width
            y0, y1 = 0 - m1_width, height + m1_width

            count["left-full"] += 1

        elif circuit.port[name].position == "right-full":
            right = width + count["right-full"] * m1_x_pitch
            x0, x1 = right - m1_width, right + m1_width
            y0, y1 = 0 - m1_width, height + m1_width

            count["right-full"] += 1

        # exact
        elif circuit.port[name].position == "top":
            top = height
            y0, y1 = top - m1_extend, top + m1_width
            mid = (int((width/2) / m1_x_pitch) * m1_x_pitch) + (count["top"] * m1_x_pitch)
            x0, x1 = mid - m1_width, mid + m1_width

            count["top"] += 1

        elif circuit.port[name].position == "bottom":
            btm = 0
            y0, y1 = btm - m1_width, btm + m1_extend
            mid = (int((width/2) / m1_x_pitch) * m1_x_pitch) + (count["bottom"] * m1_x_pitch)
            x0, x1 = mid - m1_width, mid + m1_width

            count["bottom"] += 1

        elif circuit.port[name].position == "left":
            left = 0
            x0, x1 = left - m1_width, left + m1_extend
            mid = (int((height/2) / m1_y_pitch) * m1_y_pitch) + (count["left"] * m1_y_pitch) 
            y0, y1 = mid - m1_width, mid + m1_width

            count["left"] += 1

        elif circuit.port[name].position == "right":
            right = width
            x0, x1 = right - m1_extend, right + m1_width
            mid = (int((height/2) / m1_y_pitch) * m1_y_pitch) + (count["right"] * m1_y_pitch)
            y0, y1 = mid - m1_width, mid + m1_width

            count["right"] += 1

        # corner
        elif circuit.port[name].position == "top-left":
            top = height
            left = 0 + (count["top-left"] + 1) * m1_x_pitch
            x0, x1 = left - m1_width, left + m1_width
            y0, y1 = top - m1_extend, top + m1_width

            count["top-left"] += 1

        elif circuit.port[name].position == "left-top":
            top = height - (count["left-top"] + 1) * m1_y_pitch
            left = 0
            x0, x1 = left - m1_width, left + m1_extend
            y0, y1 = top - m1_width, top + m1_width

            count["left-top"] += 1

        elif circuit.port[name].position == "top-right":
            top = height
            right = width - (count["top-right"] + 1) * m1_x_pitch

            x0, x1 = right - m1_width, right + m1_width
            y0, y1 = top - m1_extend, top + m1_width

            count["top-right"] += 1

        elif circuit.port[name].position == "right-top":
            top = height - (count["right-top"] + 1) * m1_y_pitch
            right = width
            x0, x1 = right - m1_extend, right + m1_width
            y0, y1 = top - m1_width, top + m1_width

            count["right-top"] += 1

        elif circuit.port[name].position == "bottom-left":
            btm = 0
            left = 0 + (count["bottom-left"] + 1) * m1_x_pitch
            x0, x1 = left - m1_width, left + m1_width
            y0, y1 = btm - m1_width, btm + m1_extend

            count["bottom-left"] += 1

        elif circuit.port[name].position == "left-bottom":
            btm = 0 + (count["left-bottom"] + 1) * m1_y_pitch
            left = 0
            x0, x1 = left - m1_width, left + m1_extend
            y0, y1 = btm - m1_width, btm + m1_width

            count["left-bottom"] += 1
            
        elif circuit.port[name].position == "bottom-right":
            btm = 0
            right = width - (count["bottom-right"] + 1) * m1_x_pitch
            x0, x1 = right - m1_width, right + m1_width
            y0, y1 = btm - m1_width, btm + m1_extend

            count["bottom-right"] += 1
            
        elif circuit.port[name].position == "right-bottom":
            btm = 0 + (count["right-bottom"] + 1) * m1_y_pitch
            right = width
            x0, x1 = right - m1_extend, right + m1_width
            y0, y1 = btm - m1_width, btm + m1_width

            count["right-bottom"] += 1


        # update the port shape
        if circuit.port[name].position:
            circuit.port[name].shape["m1_text"] = [Text("m1_text", [(x0 + x1)/2, (y0 + y1)/2], name)]
            circuit.port[name].shape["metal1"] = [Box("metal1", [x0, y0], [x1, y1])]
            