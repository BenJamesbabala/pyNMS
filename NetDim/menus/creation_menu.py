# NetDim
# Copyright (C) 2016 Antoine Fourmy (antoine.fourmy@gmail.com)
# Released under the GNU General Public License GPLv3

import tkinter as tk
from os.path import join
from objects.objects import *
from tkinter import ttk
from PIL import ImageTk
from pythonic_tkinter.preconfigured_widgets import *
from collections import OrderedDict
from graph_generation.network_dimension import NetworkDimension
from drawing import drawing_options_window

class CreationMenu(CustomFrame):
    
    def __init__(self, notebook, master):
        super().__init__(width=200, height=600, borderwidth=1, relief='solid')
        self.ms = master
        font = ('Helvetica', 8, 'bold')
        
        # label frame for object selection
        lf_selection = Labelframe(self)
        lf_selection.text = 'Selection mode'
        lf_selection.grid(1, 0, sticky='nsew')
        
        # label frame for object creation
        lf_creation = Labelframe(self)
        lf_creation.text = 'Creation mode'
        lf_creation.grid(2, 0, sticky='nsew')
        
        # label frame for automatic generation of classic graph
        lf_generation = Labelframe(self)
        lf_generation.text = 'Graph generation'
        lf_generation.grid(3, 0, sticky='nsew')
        
        self.dict_image = {}
        
        self.dict_size_image = {
        'netdim': (75, 75), 
        'motion': (75, 75), 
        'multi-layer': (75, 75),
        'ethernet': (85, 15),
        'wdm': (85, 15),
        'static route': (85, 15),
        'BGP peering': (85, 15),
        'OSPF virtual link': (85, 15),
        'Label Switched Path': (85, 15),
        'routed traffic': (85, 15),
        'static traffic': (85, 15),
        'ring': (50, 40), 
        'tree': (50, 30), 
        'star': (50, 50), 
        'full-mesh': (50, 45)
        }
        
        for image_type, image_size in self.dict_size_image.items():
            x, y = image_size
            img_path = join(self.ms.path_icon, image_type + '.png')
            img_pil = ImageTk.Image.open(img_path).resize(image_size)
            img = ImageTk.PhotoImage(img_pil)
            print(image_type)
            self.dict_image[image_type] = img
        
        self.type_to_button = {}
        
        self.type_to_action = {
        'netdim': lambda: Computation(self.ms),
        'motion': lambda: self.switch_to('motion'),
        'multi-layer': lambda: self.ms.cs.switch_display_mode(),
        # 'text': lambda: self.change_creation_mode('text'),
        # 'rectangle': lambda: self.change_creation_mode('rectangle'),
        # 'circle': lambda: 43,
        # 'color': lambda: 44
        }
        
        for topo in ('tree', 'star', 'full-mesh', 'ring'):
            self.type_to_action[topo] = lambda t=topo: NetworkDimension(self.ms.cs, t)
            
        for obj_type in object_properties:
            if obj_type not in ('l2vc', 'l3vc'):
                cmd = lambda o=obj_type: self.change_creation_mode(o)
                self.type_to_action[obj_type] = cmd
        
        for button_type, cmd in self.type_to_action.items():
            button = TKButton(self, relief=tk.FLAT, command=cmd)                
            if button_type in self.ms.cs.ntw.link_class:
                button.configure(text={
                                       'ethernet': 'Ethernet link',
                                       'wdm': 'WDM link',
                                       'static route': 'Static route',
                                       'BGP peering': 'BGP peering',
                                       'OSPF virtual link': 'OSPF virtual link',
                                       'Label Switched Path': 'MPLS LSP',
                                       'routed traffic': 'Routed traffic',
                                       'static traffic': 'Static traffic' 
                            }[button_type], compound='top', font=font)
                button.config(width=160, height=40)
            elif button_type in ('text', 'rectangle'):
                button.configure(compound='top', font=font, text=button_type)
            else:
                button.configure(compound='top', font=font)                                                        
            if button_type not in self.ms.cs.ntw.node_subtype:
                button.config(image=self.dict_image[button_type])
            else:
                button.config(image=self.ms.dict_image['default'][button_type])
                button.config(width=75, height=75)
            if button_type in ('tree', 'star', 'full-mesh', 'ring'):
                button.config(width=75, height=75)
            self.type_to_button[button_type] = button
                
        # netdim mode: motion or creation
        self.type_to_button['netdim'].grid(0, 0, sticky='ew')
        self.type_to_button['motion'].grid(0, 0, 2, padx=20, in_=lf_selection)
        
        #self.type_to_button['multi-layer'].grid(row=2, column=2, columnspan=2)
        
        # radio button to choose between link and node selection
        selection_value = tk.StringVar()
        selection_value.set('node') 

        node_selection = Radiobutton(self, variable=selection_value, value='node')
        node_selection.text = 'Select nodes'
        node_selection.command = lambda: self.change_selection('node')

        link_selection = Radiobutton(self, variable=selection_value, value='link')
        link_selection.text = 'Select links'
        link_selection.command = lambda: self.change_selection('link')
        
        # affichage des radio button
        node_selection.grid(0, 1, in_=lf_selection)
        link_selection.grid(1, 1, in_=lf_selection)

        # creation mode: type of node or link
        self.type_to_button['router'].grid(0, 0, padx=2, in_=lf_creation)
        self.type_to_button['switch'].grid(0, 1, padx=2, in_=lf_creation)
        self.type_to_button['oxc'].grid(0, 2, padx=2, in_=lf_creation)
        self.type_to_button['host'].grid(0, 3, padx=2, in_=lf_creation)
        self.type_to_button['regenerator'].grid(1, 0, padx=2, in_=lf_creation)
        self.type_to_button['splitter'].grid(1, 1, padx=2, in_=lf_creation)
        self.type_to_button['antenna'].grid(1, 2, padx=2, in_=lf_creation)
        self.type_to_button['cloud'].grid(1, 3, padx=2, in_=lf_creation)
        
        sep = Separator(self)
        sep.grid(2, 0, 1, 4, in_=lf_creation)
        
        self.type_to_button['ethernet'].grid(3, 0, 1, 2, in_=lf_creation)
        self.type_to_button['wdm'].grid(3, 2, 1, 2, in_=lf_creation)
                                                
        self.type_to_button['static route'].grid(4, 0, 1, 2, in_=lf_creation)
        self.type_to_button['BGP peering'].grid(4, 2, 1, 2, in_=lf_creation)
        self.type_to_button['OSPF virtual link'].grid(5, 0, 1, 2, in_=lf_creation)
        self.type_to_button['Label Switched Path'].grid(5, 2, 1, 2, in_=lf_creation)
        
        self.type_to_button['routed traffic'].grid(6, 0, 1, 2, in_=lf_creation)
        self.type_to_button['static traffic'].grid(6, 2, 1, 2, in_=lf_creation)
        
        # graph generation
        self.type_to_button['tree'].grid(0, 0, in_=lf_generation)
        self.type_to_button['star'].grid(0, 1, in_=lf_generation)
        self.type_to_button['full-mesh'].grid(0, 2, in_=lf_generation)
        self.type_to_button['ring'].grid(0, 3, in_=lf_generation)

        # 
        # # drawing
        # label_drawing = tk.Label(self, text='Graph generation', 
        #                                     bg='#A1DBCD', font=font)
        # label_drawing.grid(row=24, columnspan=4, sticky='ew')
        # self.type_to_button['text'].grid(row=25, column=0, sticky='w')
        # self.type_to_button['rectangle'].grid(row=25, column=1, sticky='w')
        # self.type_to_button['circle'].grid(row=25, column=2, sticky='w')
        # self.type_to_button['color'].grid(row=25, column=3, sticky='w')

    def update_display(self):
        display_settings = list(map(lambda x: x.get(), self.layer_boolean))
        self.ms.cs.display_layer = display_settings
        self.ms.cs.draw_all(False)
        
    def change_selection(self, mode):
        self.ms.cs.obj_selection = mode
        
    def switch_to(self, mode):
        relief = tk.SUNKEN if mode == 'motion' else tk.RAISED
        self.type_to_button['motion'].config(relief=relief)
        self.ms.cs._mode = mode
        self.ms.cs.switch_binding()
        
    def change_creation_mode(self, mode):
        # change the mode to creation 
        self.switch_to('creation')
        self.ms.cs._creation_mode = mode
        for obj_type in self.type_to_button:
            if mode == obj_type:
                self.type_to_button[obj_type].config(relief=tk.SUNKEN)
            else:
                self.type_to_button[obj_type].config(relief=tk.FLAT)
        self.ms.cs.switch_binding()
        
    def erase_graph(self, scenario):
        scenario.erase_graph()
        scenario.ntw.erase_network()
        
class Computation(CustomTopLevel):
            
    def __init__(self, master):
        super().__init__()
        self.ms = master

        self.functions = OrderedDict([
        ('Update AS topology', self.ms.cs.ntw.update_AS_topology),
        ('Interface allocation', self.ms.cs.ntw.interface_allocation),
        ('IP addressing', self.ms.cs.ntw.ip_allocation),
        ('Create routing tables', self.ms.cs.ntw.rt_creation),
        ('Route traffic links', self.ms.cs.ntw.path_finder),
        ('Refresh labels', self.ms.cs.refresh_all_labels)
        ])
        
        self.lb_functions = ObjectListbox(self, activestyle='none', width=15, 
                                            height=7, selectmode='extended')
                                            
        for function in self.functions:
            self.lb_functions.insert(function) 
            
        # button to confirm selection and trigger functions
        self.OK_button = ttk.Button(self, text='OK', command=self.OK)
                                
        self.lb_functions.pack(fill=tk.BOTH, expand=1)
        self.OK_button.pack()
        
    def OK(self):
        for function in self.lb_functions.selected():
            print(function)
            self.functions[function]()
        self.destroy()
        