import tkinter as tk
from math import sin, cos, pi
from time import time
from PIL import Image, ImageTk

class App:
    def __init__(self, master):
        self.user_input = {}
        self.user_entry_bars = {}
        self.time_multiplier = 1
        self.reset_counter = 0

        ##### Main frame setup #####
        self.main_frame = tk.Frame(master, bg='#222222')
        self.main_frame.place(width=900, height=500)
        main = self.main_frame

        #### draw a label to communicate with the user ####
        self.info_label = tk.Label(main, text='', fg='white', bg='#222222', font=('Calibri',11), justify='center', relief='solid')
        self.info_label.place(x=635, y=270, width=245, height=45)

        ##### Canvas setup  (where sketch goes) #####
        self.sketch = self.draw_sketch(main, self.user_input)

        self.sketch.place(width=600, height=400, x=15, y=15)

        #draws input entries and returns the list of them
        self.user_entry_bars = self.draw_user_input_entries(main, x=750, y=20, spacing=45, font=('Calibri', 13), size={'width':130, 'height':30})

        #draws labels (coordinates should be adjusted to fit entries to label)
        self.draw_input_entries_labels(main, x=748, y=22, spacing=45, font=('Calibri', 12), fg='white', bg='#222222', anchor='ne')

        #draw button that that runs a simulation
        run_sim_button = tk.Button(main, text='Run Simulation', command=self.open_simulation_window, font=('Calibri', 11))
        run_sim_button.place(width=130, height=45, x=15, y=435)

        #draw button that updates the sketch
        update_button = tk.Button(main, text='Update Sketch', command=self.update_sketch, font=('Calibri', 11))
        update_button.place(width=130, height=45, x=160, y=435)

        #draw logo and sign
        logo_path = 'logo.png'
        self.draw_logo_and_sign(main, x=625, y=475, link_size={'width':200,'height':25}, font=('Dubai', 11), fg='white', bg='#222222',
            image_path=logo_path, logo_size=55)


    def read_user_input_entries(self):
        #iter over all entry bars and put the values inside user_input
        for entry_bar in self.user_entry_bars.items():
            self.user_input[entry_bar[0]] = entry_bar[1].get()

        for item in self.user_input.items():
            try:
                if len(item[1]) != 0:
                    #transform values to float
                    self.user_input[item[0]] = float(item[1])
                else:
                    self.info_label.config(text='Entries cannot be empty')
                    return False
            except ValueError:
                self.info_label.config(text='Only numbers allowed')
                return False

        return True


    def draw_sketch(self, frame, data):
        ball_position = {}

        #canvas init
        canvas = tk.Canvas(frame, bg='white')

        #last data check
        if len(data) != 0:
            error = False
            error = self.is_invalid_data(data)
            if error != False:
                self.info_label.config(text=error)
                return canvas



        #interpreting data
        if len(data) == 0:
            #default info
            ball_position['y'] = 290
            ball_position['x'] = 200

            data = {}
            data['angle'] = 30
        else:
            #scaling height to avoid problems
            data['height'] = ((data['height'] / 20.0)) * 160

            if data['height'] == 0:
                data['height'] = 0
            elif data['height'] < 30:
                data['height'] = 30
            elif data['height'] > 160:
                data['height'] = 160

            ball_position['y'] = 290 - data['height']
            ball_position['x'] = 200



        x_axis = canvas.create_line(10, 290, 570, 290, width=2, arrow=tk.LAST, arrowshape=(10,12,5))
        y_axis = canvas.create_line(20, 390, 20, 50, width=2, arrow=tk.LAST, arrowshape=(10,12,5))


        #just for readability
        y = ball_position['y']
        x = ball_position['x']

        height_arrow = canvas.create_line(100, 290, 100, y, width=1, fill='darkblue', arrow=tk.BOTH, arrowshape=(10,12,5))
        height_dashed_line = canvas.create_line(50, y, x+100, y, width=1, dash=True)

        r = 10
        ball = canvas.create_oval(x-r, y+r, x+r, y-r, fill='grey')

        gravity_vector_coords = x, y, x, y+90
        gravity_vector = canvas.create_line(gravity_vector_coords, fill='green', width=2, arrow=tk.LAST, arrowshape=(10,12,5))

        velocity_vector_coords = self.calculate_vector_coords(data['angle'], x, y, 150)
        velocity_vector = canvas.create_line(velocity_vector_coords, fill='red', width=2, arrow=tk.LAST, arrowshape=(10,12,5))

        r = 60
        angle_arc_vector_coords = x+r, y-r, x-r, y+r
        angle_arc = canvas.create_arc(angle_arc_vector_coords, start=0, extent=data['angle'], width=2, style='arc')

        #Creating a key, because its very difficult to label vectors and not look bad
        self.draw_key(x=550, y=50, spacing=50, length=45, canvas=canvas, font=('Calibri', 12))

        #return the canvas object to place it in the window later
        return canvas


    def draw_user_input_entries(self, frame, x, y, spacing, size, font):
        angle = tk.Entry(frame, font=font)
        angle.place(x=x, y=y, width=size['width'], height=size['height'])

        vel = tk.Entry(frame, font=font)
        vel.place(x=x, y=y+spacing, width=size['width'], height=size['height'])

        gravity = tk.Entry(frame, font=font)
        gravity.place(x=x, y=y+spacing*2, width=size['width'], height=size['height'])

        height = tk.Entry(frame, font=font)
        height.place(x=x, y=y+spacing*3, width=size['width'], height=size['height'])

        time_multi = tk.Entry(frame, font=font)
        time_multi.place(x=x, y=y+spacing*4, width=size['width'], height=size['height'])

        #return the tuple of all entries programmed here
        return {'angle':angle, 'vel':vel, 'grav':gravity, 'height':height, 'time_multi':time_multi}


    def draw_input_entries_labels(self, frame, x, y, spacing, font, fg, bg, anchor):
        angle_label = tk.Label(frame, text='Angle [deg]  = ', font=font, fg=fg, bg=bg)
        angle_label.place(x=x, y=y, anchor=anchor)

        vel_label = tk.Label(frame, text='Velocity [m/s]  = ', font=font, fg=fg, bg=bg)
        vel_label.place(x=x, y=y+spacing, anchor=anchor)

        gravity_label = tk.Label(frame, text='Gravity [m/s^2]  = ', font=font, fg=fg, bg=bg)
        gravity_label.place(x=x, y=y+spacing*2, anchor=anchor)

        height_label = tk.Label(frame, text='Height [m]  = ', font=font, fg=fg, bg=bg)
        height_label.place(x=x, y=y+spacing*3, anchor=anchor)

        time_multi_label = tk.Label(frame, text='Time multiplier  = ', font=font, fg=fg, bg=bg)
        time_multi_label.place(x=x, y=y+spacing*4, anchor=anchor)


    def update_sketch(self):
        #read all entry_bars and pre-validate input
        if self.read_user_input_entries() != True:
            return None

        error = False
        error = self.is_invalid_data(self.user_input)
        if error != False:
            self.info_label.config(text=error)
            return False

        #clear previous version
        self.sketch.delete('all')
        for child in self.sketch.winfo_children():
            child.destroy()

        self.sketch = self.draw_sketch(self.main_frame, self.user_input)
        self.sketch.place(width=600, height=400, x=15, y=15)

        if self.reset_counter == 0:
            self.info_label.config(text='Sketch redrawn')
        elif self.reset_counter > 0 and self.reset_counter < 9e+3:
            self.info_label.config(text=f'Sketch redrawn (x{self.reset_counter})')
        else:
            print('enough redrawing')
            raise Exception

        self.reset_counter = self.reset_counter + 1


    def is_invalid_data(self, data):
        mx = 1e+7

        try:
            if data['angle'] > 90 or data['angle'] < 0:
                return 'Angle must belong to <0, 90> range'
            
            if data['vel'] <= 0:
                return 'Velocity must be positive'
            elif data['vel'] > mx:
                return 'Velocity too high'

            if data['grav'] <= 0:
                return 'Gravity must be positive'
            elif data['grav'] > mx:
                return 'Gravity too high'

            if data['height'] < 0:
                return 'Height must not be negative'
            elif data['height'] > mx:
                return 'Height too large'

            if data['time_multi'] > 1000 or data['time_multi'] < 0.001:
                return 'Time multiplier must belong to\n <0.001, 1000> range'

            #when all checks are passed
            return False
            
        except KeyError:
            print('Wrong/missing data, check self.is_invalid_data')
            return 'Wrong/missing data, check self.is_invalid_data'


    def calculate_vector_coords(self, angle, x_start, y_start, length):
        radians = angle*pi/180
        
        vector_length = length

        x_end = cos(radians) * vector_length
        y_end = sin(radians) * vector_length

        x_end = x_end + x_start
        y_end = - y_end + y_start

        coords = x_start, y_start, x_end, y_end
        return coords


    def draw_key(self, x, y, spacing, length, canvas, font):

        key_height_arrow = canvas.create_line(x+length/4, y-40, x+length/4, y+10, width=1, fill='darkblue', arrow=tk.BOTH, arrowshape=(10,12,5))
        key_vel_label = tk.Label(canvas, text='Height', font=font, bg='white')
        key_vel_label.place(x=x-65, y=y-26)

        key_vel_vector = canvas.create_line(self.calculate_vector_coords(45, x, y+spacing, length), fill='red', width=2, arrow=tk.LAST, arrowshape=(10,12,5))
        key_vel_label = tk.Label(canvas, text='Velocity', font=font, bg='white')
        key_vel_label.place(x=x-65, y=(y+spacing)-length/1.4)

        key_grav_vector = canvas.create_line(self.calculate_vector_coords(45, x, y+spacing*2, length), fill='green', width=2, arrow=tk.LAST, arrowshape=(10,12,5))
        key_grav_label = tk.Label(canvas, text='Gravity', font=font, bg='white')
        key_grav_label.place(x=x-65, y=(y+spacing*2)-length/1.4)


    def draw_logo_and_sign(self, frame, x, y, image_path, font, link_size, logo_size, fg, bg):
        #logo_path = 'logo.png'
        #logo_style = {'bg':'color', 'fg':'color'}
        #sign_font = ('font', size)

        link_label = tk.Label(frame, font=font, text='https://github.com/NotSirius-A', fg=fg, bg=bg)
        link_label.place(x=x, y=y, width=link_size['width'], height=link_size['height'])


        image = Image.open(image_path)
        image = image.resize((logo_size, logo_size), Image.ANTIALIAS)

        logo = ImageTk.PhotoImage(image)

        logo_label = tk.Label(frame, image=logo, bg=bg)
        logo_label.image = logo

        logo_label.place(x=x+link_size['width']+5, y=y-logo_size/10, anchor='w')


    def open_simulation_window(self):
        #update data
        if self.read_user_input_entries() != True:
            return None

        #last data check
        if len(self.user_input) != 0:
            error = False
            error = self.is_invalid_data(self.user_input)
            if error != False:
                self.info_label.config(text=error)
                return None

        sim = tk.Tk()

        sim.title('Simulation')

        sim.geometry("1200x770")

        app = Simulator(sim, self.user_input)

        sim.resizable(False, False)

        sim.mainloop()


class Simulator:
    def __init__(self, master, data):
        #!! Data here should be already clean, no data checks ahead 
        #!! Data must be {'height':h, 'vel':V, 'grav':g, 'angle':a, 'time multiplier':t} and all within allowed range
        #!! All should be SI units
        #It's written for 1200x770 size, but it should be possible to switch, with relatively low effort
        self.master = master
        self.data = data
        self.time_multiplier = self.data['time_multi']
        self.time = {'start':0, 'last':0}
        self.CONSTANTS = {}




        ## CONSTANTS ##
        self.CONSTANTS.update({'plane_size':(1200,700)})
        self.CONSTANTS.update({'plane_style':{
            'bg':'white',
            }})

        self.CONSTANTS.update({'bottom_frame_size':(1200,70)})
        self.CONSTANTS.update({'bottom_frame_style':{
            'bg':'#222222',
            }})

        self.CONSTANTS.update({'OX_coords':(25,645,1180,645)})
        self.CONSTANTS.update({'OY_coords':(55,675,55,20)})

        self.CONSTANTS.update({'reference_marks':{
            'x_max_coord':0.85 * self.CONSTANTS['plane_size'][0],
            'y_max_coord':0.15 * self.CONSTANTS['plane_size'][1],
            'fill':'darkred',
            'width':2,
            'length':15,
            }})   

        self.CONSTANTS['reference_marks'].update({'label':{
            'fg':'black',
            'bg':'white',
            'font':('Calibri',11),
            'spacing':20,
            'relief':'ridge'
            }})      

        self.CONSTANTS.update({'ball':{
            'radius':12,
            'fill':'red',
            'outline':'black',
            'ball_object_id': None
            }})

        self.CONSTANTS.update({'guide_lines':{
            'fill':'grey',
            'width':1,
            'object_ids': None,
            'dash':4
            }})

        self.CONSTANTS.update({'footprints':{
            'fill':'grey',
            'radius':1,
            'outline':'black',
            'object_ids': [],
            'width':0
            }})

        self.CONSTANTS.update({'button':{
            'x':30,
            'y':15,
            'spacing':130,
            'width':110,
            'height':40,
            'fg':'black',
            'font':('Calibri',11)
            }})

        self.CONSTANTS.update({'coords_labels':{
            'x':310,
            'y':15,
            'spacing':210,
            'width':190,
            'height':40,
            'fg':'white',
            'bg':'#222222',
            'font':('Calibri',12),
            'relief':'groove'
            }})

        self.CONSTANTS.update({'update_period_ms':5})

        self.reference_points = self.get_reference_points(data)
        ## CONSTANTS ##




        #Initializing the canvas that will contain the kartesian plane
        self.xy_plane = tk.Canvas(master, self.CONSTANTS['plane_style'])

        #Draw objects on the xy plane
        self.draw_gridlines(self.xy_plane, self.CONSTANTS, color='lightgrey')
        self.draw_axis(self.xy_plane, self.CONSTANTS)
        self.draw_reference_marks(self.xy_plane, self.reference_points, self.CONSTANTS)

        #Draw ball (initially)
        self.draw_ball(initial=True)

        #Placing the canvas
        self.xy_plane.place(width=self.CONSTANTS['plane_size'][0], height=self.CONSTANTS['plane_size'][1])

        #Placing the frame at the bottom
        self.bottom_frame = tk.Frame(master, self.CONSTANTS['bottom_frame_style'])
        self.bottom_frame.place(width=self.CONSTANTS['bottom_frame_size'][0], height=self.CONSTANTS['bottom_frame_size'][1],
                                x=0, y=self.CONSTANTS['plane_size'][1])

        #draw buttons at the bottom
        self.draw_buttons(self.bottom_frame, self.CONSTANTS)

        #draw coords labels at the bottom (the x,y,t)
        self.coords_labels = self.draw_coords_labels(self.bottom_frame, self.CONSTANTS)

        #draw logo and sign (actually just sign, bc logo is broken and it'll take too long to fix)
        logo_path = 'Logo.png'
        self.draw_logo_and_sign(self.bottom_frame, x=995, y=40, link_size={'width':200,'height':25}, font=('Dubai', 11), fg='white', bg='#222222',
            image_path=logo_path, logo_size=55)


    def draw_axis(self, canvas, CONSTANTS):
        canvas.create_line(CONSTANTS['OX_coords'], width=2, arrow=tk.LAST, arrowshape=(10,12,5))
        canvas.create_line(CONSTANTS['OY_coords'], width=2, arrow=tk.LAST, arrowshape=(10,12,5))

        self.draw_axis_marks(canvas, CONSTANTS, color='black', size=8)


    def draw_gridlines(self, canvas, CONSTANTS, horizontal=True, vertical=True, color='lightgrey'):
        x = CONSTANTS['OY_coords'][0]
        y = CONSTANTS['plane_size'][1] - CONSTANTS['OX_coords'][1]
        y_2 = CONSTANTS['OX_coords'][1]

        if horizontal:
            draw = True
            i=0
            while draw:
                if y*i > CONSTANTS['plane_size'][1]:
                    draw = False
                    break

                canvas.create_line(0, y_2-y*i, CONSTANTS['plane_size'][0], y_2-y*i, width=1, fill=color)

                i = i+1

        if vertical:
            draw = True
            i=1
            while draw:
                if x*i > CONSTANTS['plane_size'][0]:
                    draw = False
                    break

                canvas.create_line(x*i, 0, x*i, CONSTANTS['plane_size'][1], width=1, fill=color)

                i = i+1


    def draw_axis_marks(self, canvas, CONSTANTS, horizontal=True, vertical=True, color='black', size=10):
        #CONSTANTS - declared in __init__
        x = CONSTANTS['OY_coords'][0]
        y = CONSTANTS['plane_size'][1] - CONSTANTS['OX_coords'][1]
        y_2 = CONSTANTS['OX_coords'][1]

        if horizontal:
            draw = True
            i=1
            while draw:
                if y*i > CONSTANTS['plane_size'][1]:
                    draw = False
                    break

                canvas.create_line(x-size/2, y_2-y*i, x+size/2, y_2-y*i, width=2, fill=color)

                i = i+1

        if vertical:
            draw = True
            i=2
            while draw:
                if x*i > CONSTANTS['plane_size'][0]:
                    draw = False
                    break

                canvas.create_line(x*i, y_2-size/2, x*i, y_2+size/2, width=2, fill=color)

                i = i+1


    def draw_reference_marks(self, canvas, reference_points, CONSTANTS):
        pos_SI = {}
        marks = CONSTANTS['reference_marks']
        label = CONSTANTS['reference_marks']['label']
        CONSTANTS['OY_coords'][0]

        #use already existing function to get coords of x_max and y_max
        #just insert according values for pos_SI
        pos_SI['x'] = reference_points['x_max']
        pos_SI['y'] = 0
        x_max_point = self.get_current_position_coords(pos_SI, reference_points, CONSTANTS)

        x_max_mark = canvas.create_line(x_max_point['x'], CONSTANTS['OX_coords'][1]+marks['length']/2,
            x_max_point['x'], CONSTANTS['OX_coords'][1]-marks['length']/2,
            width=marks['width'], fill=marks['fill'])

        val = round(reference_points['x_max'],2)
        x_max_label = tk.Label(canvas, text=f"{val}m", font=label['font'], fg=label['fg'], bg=label['bg'], relief=label['relief'])
        x_max_label.place(x=x_max_point['x'], y=CONSTANTS['OX_coords'][1]+label['spacing'], anchor='ne')


        #now for the y axis
        pos_SI['x'] = reference_points['x(t_y)']
        pos_SI['y'] = reference_points['y_max']
        y_max_point = self.get_current_position_coords(pos_SI, reference_points, CONSTANTS)

        y_max_mark = canvas.create_line(CONSTANTS['OY_coords'][0]+marks['length']/2, y_max_point['y'],
            CONSTANTS['OY_coords'][0]-marks['length']/2, y_max_point['y'],
            width=marks['width'], fill=marks['fill'])

        val = round(reference_points['y_max'],2)
        y_max_label = tk.Label(canvas, text=f"{val}m", font=label['font'], fg=label['fg'], bg=label['bg'], relief=label['relief'])
        y_max_label.place(x=CONSTANTS['OY_coords'][0]+label['spacing'], y=y_max_point['y']-label['spacing'], anchor='w')

        #now the x for y max point axis
        pos_SI['x'] = reference_points['x(t_y)']
        pos_SI['y'] = reference_points['y_max']
        xy_max_point = self.get_current_position_coords(pos_SI, reference_points, CONSTANTS)

        xy_max_mark = canvas.create_line(xy_max_point['x'], CONSTANTS['OX_coords'][1]+marks['length']/2,
            xy_max_point['x'], CONSTANTS['OX_coords'][1]-marks['length']/2,
            width=marks['width'], fill=marks['fill'])

        val = round(reference_points['x(t_y)'],2)
        xy_max_label = tk.Label(canvas, text=f"{val}m", font=label['font'], fg=label['fg'], bg=label['bg'], relief=label['relief'])
        xy_max_label.place(x=xy_max_point['x'], y=CONSTANTS['OX_coords'][1]+label['spacing'])


    def draw_ball(self, initial=False):
        style = self.CONSTANTS['ball']
        reference_points = self.reference_points

        if initial:
            time = 0
        else: 
            time = self.get_simulation_time() * self.time_multiplier

        #this if statement is to draw the ball at exactly (x, 0) when simulation ends
        #because the update rate is always larger then 0, ball would always by slightly offset, this is to prevent it
        if time <= reference_points['t_max']:
            pos_SI = self.get_current_position_SI(time, self.data)
        else:
            time = reference_points['t_max']
            pos_SI = self.get_current_position_SI(time, self.data)
            pos_SI['y'] = 0

        coords = self.get_current_position_coords(pos_SI, reference_points, self.CONSTANTS)

        if initial == False:
            #draw guide lines and save object ids
            self.CONSTANTS['guide_lines']['object_ids'] = self.draw_guide_lines(self.xy_plane, self.CONSTANTS,coords)

            #update the labels at the bottom
            self.update_coords_labels(self.coords_labels, time, pos_SI)

            self.CONSTANTS['footprints']['object_ids'].append(self.draw_footprint(self.xy_plane, self.CONSTANTS, coords))

        r = style['radius']
        ball = self.xy_plane.create_oval(coords['x']-r, coords['y']+r, coords['x']+r, coords['y']-r, fill=style['fill'], outline=style['outline'])

        #save ball object id for later manipulation
        self.CONSTANTS['ball']['object_id'] = ball

        if time >= reference_points['t_max']:
            #return false to indicate that t max has been reached (used to stop simulation)
            return False
        else:
            return True


    def draw_guide_lines(self, canvas, CONSTANTS, coords):
        style = CONSTANTS['guide_lines']
        x_size = CONSTANTS['plane_size'][0]
        y_size = CONSTANTS['plane_size'][1]

        x_guide_line = canvas.create_line(0, coords['y'], x_size, coords['y'], fill=style['fill'], width=style['width'], dash=style['dash'])

        y_guide_line = canvas.create_line(coords['x'], 0, coords['x'], y_size, fill=style['fill'], width=style['width'], dash=style['dash'])

        return (x_guide_line, y_guide_line)


    def draw_footprint(self, canvas, CONSTANTS, coords):
        style = CONSTANTS['footprints']
        r = style['radius']

        footprint = canvas.create_oval(coords['x']-r, coords['y']+r, coords['x']+r, coords['y']-r,
            fill=style['fill'], outline=style['outline'], width=style['width'])

        return footprint


    def update_simulation(self):
        self.update_simulation_job = self.master.after(self.CONSTANTS['update_period_ms'], self.update_simulation)
        
        #delete previous ball and draw new, updated one
        self.xy_plane.delete(self.CONSTANTS['ball']['object_id'])

        #delete all guide lines, ids can be None, so thats why the try except block
        try:
            for line in self.CONSTANTS['guide_lines']['object_ids']:
                self.xy_plane.delete(line) 
        except: pass

        #self.draw_ball should return false when ball crosses the x axis (reaches ground)
        if self.draw_ball() == False:
            self.stop_btn_func()

            #delete all guide lines, ids can be None, so thats why the try except block
            try:
                for line in self.CONSTANTS['guide_lines']['object_ids']:
                    self.xy_plane.delete(line) 
            except: pass

            #return false when done, used later to self-shutdown
            return False


    def get_current_position_SI(self, time, data):
        #all should be SI units
        t = time
        h = data['height']
        V = data['vel']
        g = data['grav']
        a_rad = data['angle']*pi/180

        coords = {}

        #x(t) = Vcos(a)*t
        coords['x'] = V*cos(a_rad)*t

        #y(t) = h + Vsin(a)t - 1/2*gt^2
        coords['y'] = h + V*sin(a_rad)*t - 1/2*(g*t**2)

        coords['time'] = t

        return coords


    def get_current_position_coords(self, pos_SI, reference_points, CONSTANTS):
        coords = {}
        y_max = reference_points['y_max']
        x_max = reference_points['x_max']

        x_max_coord = CONSTANTS['reference_marks']['x_max_coord']
        y_max_coord = CONSTANTS['reference_marks']['y_max_coord']

        #translate points to match with xy_plane(instead of top-left corner)
        mx = self.translate_canvas_coords_to_xy_plane(x_max_coord, y_max_coord, CONSTANTS)

        #basically scale axis with the reference to the bigger value
        if y_max >= x_max:
            coords['y'] = pos_SI['y']/y_max * mx['y']
            coords['x'] = pos_SI['x']/y_max * mx['x']
        else:
            coords['y'] = pos_SI['y']/x_max * mx['y']
            coords['x'] = pos_SI['x']/x_max * mx['x']

        #translate the coords to match with xy_plane(instead of top-left corner)
        coords = self.translate_canvas_coords_to_xy_plane(coords['x'], coords['y'], CONSTANTS)

        return coords


    def translate_canvas_coords_to_xy_plane(self, x, y, CONSTANTS):
        x = x + CONSTANTS['OY_coords'][0]
        y = -y + CONSTANTS['OX_coords'][1]

        return {'x':x, 'y':y}


    def get_reference_points(self, data):
        #all should be SI units
        rv = {}
        h = data['height']
        V = data['vel']
        g = data['grav']
        a_rad = data['angle']*pi/180

        #time when object reaches the ground (max time) = t_max
        #t_max = (Vsin(a)+sqrt(discriminant))/g
        #discriminant = (Vsin(a))^2 + 2hg
        sqrt_d = ((V*sin(a_rad))**2+2*h*g)**0.5
        t_max = (V*sin(a_rad)+sqrt_d)/g
        rv['t_max'] = t_max

        #x value when object reaches the ground = x_max = x(t_max)
        #x(t_max) = Vcos(a_rad)t_max
        x_max = V*cos(a_rad)*t_max
        rv['x_max'] = x_max

        #time when y is at maximum = t_y (when speed in y is 0)
        #t_y = Vsin(a)/g
        t_y = V*sin(a_rad)/g
        rv['t_y'] = t_y

        #maximum y value = y_max = y(t_y)
        #y_max = h + Vsin(a)t_y - 1/2(gt_y^2)
        y_max = h + V*sin(a_rad)*t_y - 1/2*(g*t_y**2)
        rv['y_max'] = y_max

        #x when y is at maximum = x_y = x(t_y)
        #x_y = Vcos(a)t_y
        x_y = V*cos(a_rad)*t_y
        rv['x(t_y)'] = x_y

        return rv


    def draw_buttons(self, frame, CONSTANTS):
        style = CONSTANTS['button']

        #start/stop button init and placement
        self.StartStop_btn = tk.Button(frame, bg='#00a87a', text='Start', font=style['font'], fg=style['fg'], command=self.start_btn_func)
        self.StartStop_btn.place(width=style['width'], height=style['height'],
                                x=style['x'], y=style['y'])


        #reset button init and placement
        self.reset_btn = tk.Button(frame, bg='#ff6700', text='Reset', font=style['font'], fg=style['fg'], command=self.reset_btn_func)
        self.reset_btn.place(width=style['width'], height=style['height'],
                            x=style['x']+style['spacing'], y=style['y'])


    def start_btn_func(self):

        #transfrom into stop button
        self.StartStop_btn.config(bg='#F00030', text='Stop', command=self.stop_btn_func)

        #lock the reset button
        self.reset_btn.config(state='disabled')

        #start counting time here
        self.time['start'] = time()

        #start the update job
        self.update_simulation()


    def stop_btn_func(self):
        #unlock the reset button
        self.reset_btn.config(state='normal')

        #transform into start button
        self.StartStop_btn.config(bg='#00a87a', text='Start', command=self.start_btn_func)

        #save the last time value 
        self.time['last'] = self.get_simulation_time()

        #stop the update job
        self.master.after_cancel(self.update_simulation_job)


    def reset_btn_func(self):
        self.time = {'start':0, 'last':0}

        self.xy_plane.delete(self.CONSTANTS['ball']['object_id'])

        self.draw_ball(initial=True)

        self.update_coords_labels(self.coords_labels, time=0, pos_SI={'x':0,'y':self.data['height']})

        try:
            #delete guidelines
            for line in self.CONSTANTS['guide_lines']['object_ids']:
                self.xy_plane.delete(line)
            self.CONSTANTS['guide_lines']['object_ids'] = None

            #delete footprints
            for footprint in self.CONSTANTS['footprints']['object_ids']:
                self.xy_plane.delete(footprint)
            self.CONSTANTS['footprints']['object_ids'] = []

        except: pass


    def draw_coords_labels(self, frame, CONSTANTS):
        style = CONSTANTS['coords_labels']

        time_label = tk.Label(frame, text='t = 0s', font=style['font'], fg=style['fg'], bg=style['bg'], relief=style['relief'])
        time_label.place(x=style['x'], y=style['y'], width=style['width'], height=style['height'])

        x_label = tk.Label(frame, text='x = 0m', font=style['font'], fg=style['fg'], bg=style['bg'], relief=style['relief'])
        x_label.place(x=style['x']+style['spacing'], y=style['y'], width=style['width'], height=style['height'])

        y_label = tk.Label(frame, text=f"y = {self.data['height']}m", font=style['font'], fg=style['fg'], bg=style['bg'], relief=style['relief'])
        y_label.place(x=style['x']+style['spacing']*2, y=style['y'], width=style['width'], height=style['height'])

        return (time_label, x_label, y_label)


    def update_coords_labels(self, labels, time, pos_SI):
        time = round(time, 3)
        pos_SI['x'] = round(pos_SI['x'], 3)
        pos_SI['y'] = round(pos_SI['y'], 3)

        for label in labels:
            if label['text'][0] == 't':
                label.config(text=f"t = {time}s")

            if label['text'][0] == 'x':
                label.config(text=f"x = {pos_SI['x']}m")

            if label['text'][0] == 'y':
                label.config(text=f"y = {pos_SI['y']}m")


    def get_simulation_time(self):
        value = self.time_since_seconds(self.time['start'])

        value = value + self.time['last']

        return value


    def time_since_seconds(self, time_start=0):
        time_now = time()
        rv = time_now - time_start
        return round(rv, 5)


    def draw_logo_and_sign(self, frame, x, y, image_path, font, link_size, logo_size, fg, bg):
        link_label = tk.Label(frame, font=font, text='https://github.com/NotSirius-A', fg=fg, bg=bg)
        link_label.place(x=x, y=y, width=link_size['width'], height=link_size['height'])

        # image = Image.open(image_path)
        # image = image.resize((logo_size, logo_size), Image.ANTIALIAS)

        # logo = ImageTk.PhotoImage(image)

        # logo_label = tk.Label(frame, image=logo, bg=bg)
        # logo_label.image = logo

        # logo_label.place(x=x+link_size['width']+5, y=y-logo_size/10, anchor='w')


if __name__ == '__main__':
    root = tk.Tk()

    root.title('parabolic')

    root.geometry("900x500")

    root.resizable(False, False)

    app = App(root)

    root.mainloop()

    #this is handy for debugging the simulation, just uncomment the below part and comment out the above part

    # sim = tk.Tk()

    # sim.title('Simulation')

    # sim.geometry("1200x770")

    # app = Simulator(sim, {'angle': 50, 'vel': 10, 'grav': 10, 'height': 5, 'time_multi':1})

    # sim.resizable(False, False)

    # sim.mainloop()

