
import Tkinter as tk
import serial


small_text = ("Lucida\ Console", 12)

serial_port = "/dev/ttyACM0"

class ColorChanger:

    def __init__(self, parent):
        self.parent = parent
        parent.title('Tri-Color LED Control Pannel')
        parent.option_add("*Font", "Lucida\ Console 30")

        self.no_dweeno = False
        
        self.red_val = 0
        self.blue_val = 0
        self.green_val = 0
        
        self.old_red = 0
        self.old_blue = 0
        self.old_green = 0
        
        self.red_ON = True
        self.blue_ON = True
        self.green_ON = True
        
        self.val_dict = {'red':self.red_val, 'blue':self.blue_val, 'green':self.green_val}
        self.old_dict = {'red':self.old_red, 'blue':self.old_blue, 'green':self.old_green}
        self.on_dict = {'red':self.red_ON, 'blue':self.blue_ON, 'green':self.green_ON}

        try:
            self.ser = serial.Serial(serial_port, 9600)
        except serial.serialutil.SerialException:
            print "Plug in your Dweeno."
            self.no_dweeno = True
            
#-- CREATE WIDGETS --#
        label_red = tk.Label(parent, text='red', fg='tomato')
        label_blue = tk.Label(parent, text='blue', fg='deep sky blue')
        label_green = tk.Label(parent, text='green', fg='lime green')
        
        self.toggle_red = tk.Button(parent, text='On', font=small_text,
                                    command=lambda: self.deactivate_color('red'))
        self.toggle_blue = tk.Button(parent, text='On', font=small_text,
                                    command=lambda: self.deactivate_color('blue'))
        self.toggle_green = tk.Button(parent, text='On', font=small_text,
                                    command=lambda: self.deactivate_color('green'))

        self.slider_red = tk.Scale(parent, orient=tk.HORIZONTAL, from_=0, to=255, length=200,
                              showvalue=0, command=lambda x: self.get_slider_value('red') )
        self.slider_blue = tk.Scale(parent, orient=tk.HORIZONTAL, from_=0, to=255, length=200,
                              showvalue=0, command=lambda x: self.get_slider_value('blue') )
        self.slider_green = tk.Scale(parent, orient=tk.HORIZONTAL, from_=0, to=255, length=200,
                              showvalue=0, command=lambda x: self.get_slider_value('green') )

        self.red_val_display = tk.Label(parent, text=self.scale_for_display(self.red_val), width=5)
        self.blue_val_display = tk.Label(parent, text=self.scale_for_display(self.blue_val), width=5)
        self.green_val_display = tk.Label(parent, text=self.scale_for_display(self.green_val), width=5)

        no_dweeno_message = tk.Label(parent, text='''Arduino is not plugged in.
                 \nContinuing in GUI Dev Mode.''', font=("Lucida\ Console 12"))

#-- GRID WIDGETS --#
        label_red.grid(row=0, column=0, padx=50)
        label_green.grid(row=1, column=0, padx=50)
        label_blue.grid(row=2, column=0, padx=50)
        
        self.toggle_red.grid(row=0, column=1)
        self.toggle_green.grid(row=2, column=1)
        self.toggle_blue.grid(row=1, column=1)

        self.slider_red.grid(row=0, column=2)
        self.slider_blue.grid(row=1, column=2)
        self.slider_green.grid(row=2, column=2)

        self.red_val_display.grid(row=0, column=3)
        self.blue_val_display.grid(row=1, column=3)
        self.green_val_display.grid(row=2, column=3)

        if self.no_dweeno:
            no_dweeno_message.grid(row=3,column=0, columnspan=4)

#-- PLACE WIDGETS IN DICTIONARIES --#
        # sliders, val displays, toggles, 
        self.slider_dict = {'red':self.slider_red, 'blue':self.slider_blue, 'green':self.slider_green}        
        self.val_display_dict = {'red':self.red_val_display,'blue':self.blue_val_display,'green':self.green_val_display}
        self.etoggle_dict = {'red':self.toggle_red,'blue':self.toggle_blue,'green':self.toggle_green}

# --FUNCTINOS-- #
    def create_string(self):
        return str(self.red_val)+','+str(self.green_val)+','+str(self.blue_val)+'>'
    
    def scale_for_display(self, value):
        sf = 11./255
        scaled = str(value*sf)
        head, tail = scaled.split('.')
        
        try:
            tail = tail[:2]
        except IndexError:
            tail = tail + '0'*(2-len(tail))
        
        return head+'.'+tail

    def get_slider_value(self, slider_name):
        
        if slider_name == 'red':
            self.red_val = self.slider_red.get()
            self.red_val_display.config(text=self.scale_for_display(self.red_val))

        elif slider_name == 'blue':
            self.blue_val = self.slider_blue.get()
            self.blue_val_display.config(text=self.scale_for_display(self.blue_val))

        elif slider_name == 'green':
            self.green_val = self.slider_green.get()
            self.green_val_display.config(text=self.scale_for_display(self.green_val))
        
        output = self.create_string()

        if self.no_dweeno:
            print output
        else:
            self.ser.write(output)

    def deactivate_color(self, color):
    
        if self.on_dict[color]:
            self.val_dict[color] = 0
            self.old_dict[color] = self.slider_dict[color].get()
            
            self.val_display_dict[color].config(text=self.scale_for_display(self.val_dict[color] ) )
            self.slider_dict[color].config(state=tk.DISABLED, sliderrelief=tk.SUNKEN, relief=tk.RIDGE)
            self.toggle_dict[color].config(relief=tk.SUNKEN, text='Off')
            
            if self.no_dweeno:
                print self.create_string()
            else:
                self.ser.write(self.create_string() )
            
            self.on_dict[color] = False
            
        else:
            self.val_dict[color] = self.old_dict[color]
            
            self.val_display_dict[color].config(text=self.scale_for_display(self.val_dict[color]))
            self.slider_dict[color].config(state=tk.NORMAL, sliderrelief=tk.RAISED, relief=tk.FLAT)
            self.toggle_dict[color].config(relief=tk.RAISED, text="On")
            
            if self.no_dweeno:
                print self.create_string()
            else:
                self.ser.write(self.create_string() )
            
            self.on_dict[color] = True

#            else:
#                self.red_val = self.old_red
#                
#                self.red_val_display.config(text=self.scale_for_display(self.red_val))
#                self.slider_red.config(state=tk.NORMAL, sliderrelief=tk.RAISED, relief=tk.FLAT)
#                self.toggle_red.config(relief=tk.RAISED, text='On')
#                
#                if self.no_dweeno:
#                    print self.create_string()
#                else:
#                    self.ser.write(self.create_string())
#                
#                self.red_ON = True

#        elif color == 'blue':
#            if self.blue_ON:
#                self.blue_val = 0
#                self.old_blue = self.slider_blue.get()

#                self.blue_val_display.config(text=self.scale_for_display(self.blue_val))
#                self.slider_blue.config(state=tk.DISABLED, sliderrelief=tk.SUNKEN, relief=tk.RIDGE)
#                self.toggle_blue.config(relief=tk.SUNKEN, text='Off')

#                if self.no_dweeno:
#                    print self.create_string()
#                else:
#                    self.ser.write(self.create_string())

#                self.blue_ON = False

#            else:
#                self.blue_val = self.old_blue
#                
#                self.blue_val_display.config(text=self.scale_for_display(self.blue_val))
#                self.slider_blue.config(state=tk.NORMAL, sliderrelief=tk.RAISED, relief=tk.FLAT)
#                self.toggle_blue.config(relief=tk.RAISED, text='On')
#                
#                if self.no_dweeno:
#                    print self.create_string()
#                else:
#                    self.ser.write(self.create_string())
#                
#                self.blue_ON = True
#             
#        elif color == 'green':
#            if self.green_ON:
#                self.green_val = 0
#                self.old_green = self.slider_green.get()

#                self.green_val_display.config(text=self.scale_for_display(self.green_val))
#                self.slider_green.config(state=tk.DISABLED, sliderrelief=tk.SUNKEN, relief=tk.RIDGE)
#                self.toggle_green.config(relief=tk.SUNKEN, text='Off')

#                if self.no_dweeno:
#                    print self.create_string()
#                else:
#                    self.ser.write(self.create_string())

#                self.green_ON = False

#            else:
#                self.green_val = self.old_green
#                
#                self.green_val_display.config(text=self.scale_for_display(self.green_val))
#                self.slider_green.config(state=tk.NORMAL, sliderrelief=tk.RAISED, relief=tk.FLAT)
#                self.toggle_green.config(relief=tk.RAISED, text='On')
#                
#                if self.no_dweeno:
#                    print self.create_string()
#                else:
#                    self.ser.write(self.create_string())
#                
#                self.green_ON = True



root = tk.Tk()
app = ColorChanger(root)
root.mainloop()
