# NetDim (contact@netdim.fr)

import os
import tkinter as tk
from autonomous_system import AS
from objects.objects import *
import ip_networks.configuration as conf
import ip_networks.troubleshooting as ip_ts
import ip_networks.ping as ip_ping
import ip_networks.switching_table as switching_table
import ip_networks.arp_table as arp_table
import ip_networks.routing_table as ip_rt
import ip_networks.bgp_table as ip_bgpt
import graph_generation.multiple_objects as mobj
from miscellaneous import site_operations
from .alignment_menu import AlignmentMenu
from .map_menu import MapMenu
from objects.object_management_window import PropertyChanger
from collections import OrderedDict
from objects.interface_window import InterfaceWindow
from .base_selection_rightclick_menu import BaseSelectionRightClickMenu
from miscellaneous.decorators import empty_selection_and_destroy_menu
                                
class SiteSelectionRightClickMenu(BaseSelectionRightClickMenu):
    
    def __init__(self, event, controller, from_view=True):
        super().__init__(event, from_view, controller)
                
        # exactly one node: configuration menu
        if self.no_link and self.no_shape and self.one_node:
            node ,= self.view.so['node']
            
            self.add_command(label='Enter site', 
                        command=lambda: self.enter_site(node))
            
        # make the menu appear    
        self.tk_popup(event.x_root, event.y_root)
            
    @empty_selection_and_destroy_menu
    def enter_site(self, site):
        self.controller.view_menu.enter_site(site)
        
        