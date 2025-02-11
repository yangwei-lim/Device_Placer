import random

class BStarTreeNode:
    def __init__(self, name, width, height, pin=[]):
        self.name   = name
        self.width  = width
        self.height = height

        self.area   = width * height
        self.pin    = pin
        
        self.x      = 0
        self.y      = 0

        self.left   = None
        self.right  = None
        self.parent = None

class BStarTree:
    def __init__(self):
        self.root = None
        self.h_contour = []
    
    def insert_root(self, new_node: BStarTreeNode) -> bool:
        """
        @brief: Insert new node to the root
        @param: new_node -> new node to be inserted
        """
        if self.root is None:
            self.root = new_node
            new_node.parent = None
            return True
        else:
            return False


    def insert_left(self, node: BStarTreeNode, new_node: BStarTreeNode) -> bool:
        """
        @brief: Insert the new node to the left of the node
        @param: node -> new node inserted to the left of this node
        @param: new_node -> new node to be inserted
        """
        if node.left is None:
            node.left = new_node
            new_node.parent = node
        else:
            _tmp_ = node.left
            node.left = new_node
            new_node.parent = node
            new_node.left = _tmp_
            _tmp_.parent = new_node

        return True


    def insert_right(self, node: BStarTreeNode, new_node: BStarTreeNode) -> bool:
        """
        @brief: Insert module to the right node of the tree
        @param: node -> new node inserted to the right of this node
        @param: new_node -> new node to be inserted
        """
        if node.right is None:
            node.right = new_node
            new_node.parent = node
        else:
            _tmp_ = node.right
            node.right = new_node
            new_node.parent = node
            new_node.right = _tmp_
            _tmp_.parent = new_node

        return True


    def insert_recursive(self, node: BStarTreeNode, new_node: BStarTreeNode) -> bool:
        """
        @brief: Insert module to the tree recursively
        @param: node -> current node
        @param: new_node -> new node to be inserted
        """
        if node.left is None and node.right is None:
            if random.randint(0,1) == 0:
                self.insert_left(node, new_node)
            else:
                self.insert_right(node, new_node)
        elif node.left is None:
            self.insert_left(node, new_node)
        elif node.right is None:
            self.insert_right(node, new_node)
        else:
            if random.randint(0,1) == 0:
                self.insert_recursive(node.left, new_node)
            else:
                self.insert_recursive(node.right, new_node)


    def delete(self, delete_node: BStarTreeNode) -> None:
        """
        @brief: Delete module from the tree
        @param: delete_node -> node to be deleted
        """
        # Case 1: delete node has no child
        if delete_node.left is None and delete_node.right is None:
            # delete node is the root
            if delete_node.parent is None:
                self.root = None
            # delete node is the left node of the parent node
            elif delete_node.parent.left == delete_node:
                delete_node.parent.left = None
            # delete node is the right node of the parent node
            elif delete_node.parent.right == delete_node:
                delete_node.parent.right = None

        # Case 2a: delete node has one left child
        elif delete_node.left is not None and delete_node.right is None:
            # delete node is the root
            if delete_node.parent is None:
                self.root = None
                self.insert_root(delete_node.left)
            # delete node is the left node of the parent node
            elif delete_node.parent.left == delete_node:
                delete_node.parent.left = None
                self.insert_left(delete_node.parent, delete_node.left)
            # delete node is the right node of the parent node
            elif delete_node.parent.right == delete_node:
                delete_node.parent.right = None
                self.insert_right(delete_node.parent, delete_node.left)

        # Case 2b: delete node has one right child
        elif delete_node.left is None and delete_node.right is not None:
            # delete node is the root
            if delete_node.parent is None:
                self.root = None
                self.insert_root(delete_node.right)
            # delete node is the left node of the parent node
            elif delete_node.parent.left == delete_node:
                delete_node.parent.left = None
                self.insert_left(delete_node.parent, delete_node.right)
            # delete node is the right node of the parent node
            elif delete_node.parent.right == delete_node:
                delete_node.parent.right = None
                self.insert_right(delete_node.parent, delete_node.right)

        # Case 3: delete node has two children
        elif delete_node.left is not None and delete_node.right is not None:
            if random.randint(0,1) == 0:
                replace_node = delete_node.left
                another_node = delete_node.right
            else:
                replace_node = delete_node.right
                another_node = delete_node.left

            # delete node is the root
            if delete_node.parent is None:
                self.root = None
                self.insert_root(replace_node)
                self.insert_recursive(replace_node, another_node)
            # delete node is the left node of the parent node
            elif delete_node.parent.left == delete_node:
                delete_node.parent.left = None
                self.insert_left(delete_node.parent, replace_node)
                self.insert_recursive(replace_node, another_node)
            # delete node is the right node of the parent node
            elif delete_node.parent.right == delete_node:
                delete_node.parent.right = None
                self.insert_right(delete_node.parent, replace_node)
                self.insert_recursive(replace_node, another_node)

        # Reset the delete node
        delete_node.parent = None
        delete_node.left = None
        delete_node.right = None

        
    def move(self, from_node: BStarTreeNode, to_node: BStarTreeNode, direction: str) -> None:
        """
        @brief: Move module from one place to another place
        @param: from_node -> source node
        @param: to_node -> destination node
        @param: direction -> direction of the movement (left or right)
        """
        self.delete(from_node)
        if direction == 'left':
            self.insert_left(to_node, from_node)
        elif direction == 'right':
            self.insert_right(to_node, from_node)


    def rotate(self, node: BStarTreeNode) -> None:
        """
        @brief: Rotate module
        @param: node -> source node
        """
        pass


    def swap(self, node1: BStarTreeNode, node2: BStarTreeNode) -> None:
        """
        @brief: Swap two modules
        @param: node1 -> first node to be swapped
        @param: node2 -> second node to be swapped
        """
        # get information
        _tmp_name_ = node1.name
        _tmp_width_ = node1.width
        _tmp_height_ = node1.height
        _tmp_area_ = node1.area
        _tmp_pin_ = node1.pin
        _tmp_x_ = node1.x
        _tmp_y_ = node1.y

        # swap information
        node1.name = node2.name
        node1.width = node2.width
        node1.height = node2.height
        node1.area = node2.area
        node1.pin = node2.pin
        node1.x = node2.x
        node1.y = node2.y

        node2.name = _tmp_name_
        node2.width = _tmp_width_
        node2.height = _tmp_height_
        node2.area = _tmp_area_
        node2.pin = _tmp_pin_
        node2.x = _tmp_x_
        node2.y = _tmp_y_


    def update_coordinates(self, node: BStarTreeNode) -> None:
        """
        @brief: Update all block coordinates after certain operation (move, rotate, swap, etc.)
        @param: node -> B*-tree node
        @addition: Update the pin coordinates
        """
        if node is None:
            return

        # reset pin coordinates
        for pin in node.pin:
            pin.pt1[0] -= node.x
            pin.pt2[0] -= node.x
            pin.pt1[1] -= node.y
            pin.pt2[1] -= node.y

        # update the x coordinates based on the parent node
        # left child stack on the right of the parent
        if node.parent.left == node:
            node.x = node.parent.x + node.parent.width      # xi = xj + wj    

        # right child stack on the top of the parent 
        elif node.parent.right == node:
            node.x = node.parent.x                          # xi = xj

        # update the y coordinates based on the contour
        # get the contour y coordinates that are horizontally overlapped with the node
        hclist = [hc[1] for hc in self.h_contour if hc[0] >= node.x and hc[0] < node.x + node.width]
        node.y = max(hclist) if hclist else 0               # yi = max(ycontour)

        # update pin coordinates
        for pin in node.pin:
            pin.pt1[0] += node.x
            pin.pt2[0] += node.x
            pin.pt1[1] += node.y
            pin.pt2[1] += node.y

        # update the contour
        for i, hc in enumerate(self.h_contour):
            # hc point < x0 (do nothing if the hc point is before the module)
            if hc[0] < node.x:
                continue

            # hc point = x0 (update hc point for x0)
            elif hc[0] == node.x:
                hc[1] = node.y + node.height
                
            # hc point > x0 and < x1 (update hc point in between the module)
            elif hc[0] > node.x and hc[0] < node.x + node.width:
                hc[1] = node.y + node.height

            # hc point = x1 (found a hc point there, stop looking for other points)
            elif hc[0] == node.x + node.width:
                break

            # hc point > x1 (there is no hc point at x1, add a new hc point there)
            elif hc[0] > node.x + node.width:
                self.h_contour.insert(i, [node.x + node.width, node.y])
                break

        # add new point if contour is short than the node
        if node.x + node.width > self.h_contour[-1][0]:
            self.h_contour.append([node.x + node.width, node.y])
        
        # update the left and right child coordinates
        self.update_coordinates(node.left)
        self.update_coordinates(node.right)
    

    def update_floorplan(self) -> None:
        """
        @brief: Update the floorplan
        @addition: Update the pin coordinates
        """
        # reset root pin coordinates
        for pin in self.root.pin:
            pin.pt1[0] -= self.root.x
            pin.pt2[0] -= self.root.x
            pin.pt1[1] -= self.root.y
            pin.pt2[1] -= self.root.y

        # reset root coordinates and contour
        self.root.x = 0
        self.root.y = 0
        self.h_contour = [[0,self.root.height], [self.root.width, 0]]

        # update contour and coordinates
        self.update_coordinates(self.root.left)
        self.update_coordinates(self.root.right)


    def get_modules(self, node: BStarTreeNode="root") -> list:
        """
        @brief: Get all modules from the B*-tree
        @param: node -> bstar tree node (default: root node)
        """
        nodes = []

        if node == "root":
            node = self.root
        
        if node is None:
            return nodes

        nodes.append(node)
        nodes.extend(self.get_modules(node.left))
        nodes.extend(self.get_modules(node.right))

        return nodes


    def get_nets(self) -> dict:
        """
        @brief: Get all nets from the B*-tree
        @param: node -> bstar tree node (default: root node)
        """
        nets = {}

        modules = self.get_modules()

        for module in modules:
            for pin in module.pin:
                if pin.net not in nets:
                    nets[pin.net] = [[pin.pt1[0], pin.pt1[1], pin.pt2[0], pin.pt2[1]]]
                else:
                    nets[pin.net].append([pin.pt1[0], pin.pt1[1], pin.pt2[0], pin.pt2[1]])

        return nets