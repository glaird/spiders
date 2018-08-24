# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 22:05:11 2018

@author: Garrett
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 16:45:04 2018

@author: Garrett
"""
from numpy import random
import matplotlib.pyplot as plt
import math
import matplotlib
import seaborn as sns
#from tkinter import *
import Tkinter
from ttk import *

#################################################
# Variables
num_competitive_spiders = 100
num_non_competitive_spiders = 100
survival_rate = 0.10
competitive_survival_rate = survival_rate          #use same survival rate, but allow for distinct
non_competitive_survival_rate = survival_rate     #use same survival rate, but allow for distinct
competitive_spider_mean_size = 0.5
non_competitive_spider_mean_size = 0.5
start_world_size = 1.0
num_babies = 10
spider_radius = 0.01
move_scale = 0.1
competition_factor = 0.5
max_age = 2
cut_throat=False
##################################################

def originate(num_competitive_spiders=num_competitive_spiders, 
              num_non_competitive_spiders=num_non_competitive_spiders, 
              competitive_spider_mean_size=competitive_spider_mean_size,
              non_competitive_spider_mean_size=non_competitive_spider_mean_size,
              num_babies=num_babies, start_world_size=start_world_size):
    spiders = []
    for i in range(num_competitive_spiders):
        size = random.normal(loc=competitive_spider_mean_size, scale=1.0)
        x_loc = random.uniform(low=start_world_size*-1, high=start_world_size)
        y_loc = random.uniform(low=start_world_size*-1, high=start_world_size)
        spiders.append(Spider('competitive', size, num_babies, (x_loc, y_loc),[], 0))
    
    for i in range(num_non_competitive_spiders):
        size = random.normal(loc=non_competitive_spider_mean_size, scale=1.0)
        x_loc = random.uniform(low=start_world_size*-1, high=start_world_size)
        y_loc = random.uniform(low=start_world_size*-1, high=start_world_size)
        spiders.append(Spider('non_competitive', size, num_babies, (x_loc, y_loc),[],0))
        
    return spiders
    
def get_spider_count(spiders):
    count_competitive = 0
    count_non_competitive = 0
    for spider in spiders:
        if spider.spider_type=='competitive':
            count_competitive+=1
        elif spider.spider_type=='non_competitive':
            count_non_competitive+=1
    print '\t' + str(count_competitive) + ' competitive spiders'
    print '\t' + str(count_non_competitive) + ' non-competitive spiders'
    return count_competitive, count_non_competitive
    
def get_world_range(spiders):
    min_x_val = 0
    max_x_val = 0
    min_y_val = 0
    max_y_val = 0
    for spider in spiders:
        if spider.loc[0] < min_x_val:
            min_x_val=spider.loc[0]
        if spider.loc[0] > max_x_val:
            max_x_val=spider.loc[0]
        if spider.loc[1] < min_y_val:
            min_y_val = spider.loc[1]
        if spider.loc[1] > max_y_val:
            max_y_val = spider.loc[1]

    #print 'Min X-coordinate: ' + str(min_x_val)
    #print 'Max X-coordinate: ' + str(max_x_val)
    #print 'Min Y-coordinate: ' + str(min_y_val)
    #print 'Max Y-coordinate: ' + str(max_y_val)
    return min_x_val, max_x_val, min_y_val, max_y_val

    
def run_one_cycle():
    print 'Run one cycle'
    
def seed_new_cycle():
    print 'Seed new cycle'
    
def make_world():
    spiders = originate()
    min_x, max_x, min_y, max_y = get_world_range(spiders)
    start_world = World(spiders, min_x, max_x, min_y, max_y, spider_radius, 0)
    start_world.print_world()
    return start_world
    
class Spider:
    
    def __init__(self, spider_type, spider_size, num_babies, loc, neighbors, age):
        self.spider_type = spider_type
        self.spider_size = spider_size
        self.num_babies = num_babies
        self.loc = loc
        self.neighbors=neighbors
        self.age=age
        
    def reproduce(self):
        babies = []
        for i in range(self.num_babies):
            size = random.normal(loc=self.spider_size, scale=1.0)
            babies.append(Spider(self.spider_type, size, self.num_babies, self.loc, [], 0))
        return babies
    
    def random_move(self, move_scale):
        x_loc = random.normal(loc=self.loc[0], scale=move_scale)
        y_loc = random.normal(loc=self.loc[1], scale=move_scale)
        x_loc = min(x_loc, start_world_size)
        x_loc = max(x_loc, start_world_size*-1)
        y_loc = min(y_loc, start_world_size)
        y_loc = max(y_loc, start_world_size*-1)
        self.loc=(x_loc, y_loc)

class World:
        
    def __init__(self, spiders, min_x, max_x, min_y, max_y, spider_radius, year, survival_rate,
                 competition_factor, cut_throat, max_age, move_scale):
        self.spiders=spiders
        self.min_x=min_x
        self.max_x=max_x
        self.min_y=min_y
        self.max_y=max_y
        self.spider_radius=spider_radius
        self.year=year
        self.survival_rate=survival_rate
        self.competition_factor=competition_factor
        self.cut_throat=cut_throat
        self.max_age=max_age
        self.move_scale=move_scale
        
    def print_world(self):
        X = []
        Y = []
        colors = []
        for spider in self.spiders:
            X.append(spider.loc[0])
            Y.append(spider.loc[1])
            if spider.spider_type == 'competitive':
                colors.append('competitive')
            elif spider.spider_type == 'non_competitive':
                colors.append('non-competitive')
            else:
                colors.append('other')
        color_map = ['red','blue','green']
        
        fig, ax = plt.subplots()
        ax = sns.scatterplot(X, Y, hue=colors, hue_order=['competitive','non-competitive'])
        #ax.scatter(X, Y, c=colors, cmap=matplotlib.colors.ListedColormap(color_map),
        #           label=['competitive','non-competitive','other'])
        plt.xlim(self.min_x, self.max_x)
        plt.ylim(self.min_y, self.max_y)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=2)
        plt.show()
        #ax.legend()
        #fig.show()
        
    def get_neighbors(self):
        for spider in self.spiders:
            neighbors = []
            for s2 in self.spiders:
                if spider!=s2:
                    if self.get_distance(spider, s2) <= self.spider_radius:
                        neighbors.append(s2)
            spider.neighbors=neighbors
            
    def reconcile_differences(self):
        eaten_spiders = []
        for spider in self.spiders[:]:
            i = self.spiders.index(spider)
            for neighbor in spider.neighbors:
                if spider.spider_size < neighbor.spider_size:
                    if self.cut_throat:
                        eaten_spiders.append(self.spiders.pop(i))
                        break
                    else:
                        spider.random_move(self.move_scale)
                        spider.neighbors=[]
                        for s2 in self.spiders:
                            if spider!=s2:
                                if self.get_distance(spider, s2) <= self.spider_radius:
                                    spider.neighbors.append(s2)
                 
        if len(eaten_spiders) > 0:
            eaten_spiders = list(set(eaten_spiders))
        return eaten_spiders
                        
        
    def run_cycle(self):
        print 'Initial State: Year ' + str(self.year)
        get_spider_count(self.spiders)
        print
        
        self.get_neighbors()
        eaten_spiders = self.reconcile_differences()
        print 'The following spiders were cannibalized'
        get_spider_count(eaten_spiders)
        print 'Competitive State'
        get_spider_count(self.spiders)
        print
        
        natural_causes = self.natural_causes()
        print 'The following spiders died of natural causes:'
        get_spider_count(natural_causes)
        #print str(len(natural_causes)) + ' died of natural causes'
        print 'Survival State'
        get_spider_count(self.spiders)
        print
        
        self.next_generation()
        print 'Reproduction State'
        get_spider_count(self.spiders)
        print
        
        old_age=self.old_age()
        print 'The folowing spiders died of old age'
        get_spider_count(old_age)
        print 'End State'
        #print str(len(old_age)) + ' spiders died of old age'
        get_spider_count(self.spiders)
        print
        
        self.min_x, self.max_x, self.min_y, self.max_y = get_world_range(self.spiders)
        self.year+=1
        
        self.print_world()
        
    def get_distance(self, spider1, spider2):
        x1 = spider1.loc[0]
        x2 = spider2.loc[0]
        y1 = spider1.loc[1]
        y2 = spider2.loc[1]
        x_dist = math.fabs(x1-x2)
        y_dist = math.fabs(y1-y2)
        dist = math.sqrt(x_dist**2 + y_dist**2)
        return dist
        
    def next_generation(self):
        new_spiders = []
        for spider in self.spiders:
            babies = spider.reproduce()
            for baby in babies:
                baby.random_move(self.move_scale)
                new_spiders.append(baby)
        self.spiders = self.spiders + new_spiders
        
    def natural_causes(self):
        natural_causes = []
        randoms = []
        adjusted_survival_probs = []
        dead_count = 0
        total_count = 0
        for spider in self.spiders[:]:
            total_count+=1
            num_neighbors = len(spider.neighbors)
            survival_prob = self.survival_rate*(self.competition_factor**num_neighbors)
            adjusted_survival_probs.append(survival_prob)
            rand = random.random()
            randoms.append(rand)
            if rand > survival_prob:
                natural_causes.append(self.spiders.pop(self.spiders.index(spider)))
                dead_count+=1
        return natural_causes
        
    def old_age(self):
        old_age = []
        for spider in self.spiders[:]:
            spider.age += 1
            if spider.age>max_age:
                old_age.append(self.spiders.pop(self.spiders.index(spider)))
        return old_age

        
class App(Frame):
    def __init__(self, master=None, world=None):
        Frame.__init__(self, master)
        self.world=world
        
        self.num_competitive_label = Label(text='Enter number of competitive spiders to start with')
        self.num_competitive_label.grid(row=0, sticky=E)
        
        self.num_competitive_spiders_entry = Entry()
        self.num_competitive_spiders_entry.grid(row=0, column=1, padx=10)
        
        # here is the application variable
        self.num_competitive_spiders = StringVar()
        # set it to some value
        self.num_competitive_spiders.set("100")
        # tell the entry widget to watch this variable
        self.num_competitive_spiders_entry["textvariable"] = self.num_competitive_spiders
        
        self.num_non_competitive_spiders_label = Label(text='Enter number of non-competitive spiders to start with')
        self.num_non_competitive_spiders_label.grid(row=1, sticky=E)
        self.num_non_competitive_spiders_entry = Entry()
        self.num_non_competitive_spiders_entry.grid(row=1, column=1)
        self.num_non_competitive_spiders = StringVar()
        self.num_non_competitive_spiders.set("100")
        self.num_non_competitive_spiders_entry["textvariable"] = self.num_non_competitive_spiders
        
        self.survival_rate_label = Label(text='Enter survival rate. This is the probability that a spider will survive during any cycle.')
        self.survival_rate_label.grid(row=2, sticky=E)
        self.survival_rate_entry = Entry()
        self.survival_rate_entry.grid(row=2, column=1)
        self.survival_rate = StringVar()
        self.survival_rate.set("0.10")
        self.survival_rate_entry["textvariable"] = self.survival_rate
        
        self.num_babies_label = Label(text='Enter the number of babies that surviving spiders will have')
        self.num_babies_label.grid(row=3, sticky=E)
        self.num_babies_entry = Entry()
        self.num_babies_entry.grid(row=3, column=1)
        self.num_babies = StringVar()
        self.num_babies.set("10")
        self.num_babies_entry["textvariable"] = self.num_babies
        
        self.spider_movement_label = Label(text='Enter the standard deviation for the movement of new spiders')
        self.spider_movement_label.grid(row=4, sticky=E)
        self.spider_movement_entry = Entry()
        self.spider_movement_entry.grid(row=4, column=1)
        self.spider_movement = StringVar()
        self.spider_movement.set("0.1")
        self.spider_movement_entry["textvariable"] = self.spider_movement
        
        self.spider_radius_label = Label(text='Enter the radius within which spiders will compete')
        self.spider_radius_label.grid(row=5, sticky=E)
        self.spider_radius_entry = Entry()
        self.spider_radius_entry.grid(row=5, column=1)
        self.spider_radius = StringVar()
        self.spider_radius.set("0.01")
        self.spider_radius_entry["textvariable"] = self.spider_radius
        
        self.competition_factor_label = Label(text='How detrimental is competition? Choose from range [0, 1], where 0 means all spiders will die with any competition and 1 means competition does not have an adverse effect.')
        self.competition_factor_label.grid(row=6, sticky=E)
        self.competition_factor_entry = Entry()
        self.competition_factor_entry.grid(row=6, column=1)
        self.competition_factor = StringVar()
        self.competition_factor.set("0.5")
        self.competition_factor_entry["textvariable"] = self.competition_factor
        
        self.max_age_label = Label(text='What is the maximum age a spider can reach?')
        self.max_age_label.grid(row=7, sticky=E)
        self.max_age_entry = Entry()
        self.max_age_entry.grid(row=7, column=1)
        self.max_age = StringVar()
        self.max_age.set("2")
        self.max_age_entry["textvariable"] = self.max_age
        
        self.cut_throat_label = Label(text='Cut throat True or False? True means competitive spiders will kill smaller spiders in their radius. False means they will merely force them to a new location.')
        self.cut_throat_label.grid(row=8, sticky=E)
        self.cut_throat_entry = Entry()
        self.cut_throat_entry.grid(row=8, column=1)
        self.cut_throat = StringVar()
        self.cut_throat.set("False")
        self.cut_throat_entry["textvariable"] = self.cut_throat

        self.max_iterations_label = Label(text='Maximum number if iterations if "Run to Extinction" is pressed.')
        self.max_iterations_label.grid(row=9, sticky=E)
        self.max_iterations_entry = Entry()
        self.max_iterations_entry.grid(row=9, column=1)
        self.max_iterations = StringVar()
        self.max_iterations.set("100")
        self.max_iterations_entry["textvariable"] = self.max_iterations

        self.num_batches_label = Label(text='Number of simulations to run if "Run Batch of Simulations" is pressed')
        self.num_batches_label.grid(row=10, sticky=E)
        self.num_batches_entry = Entry()
        self.num_batches_entry.grid(row=10, column=1)
        self.num_batches = StringVar()
        self.num_batches.set("100")
        self.num_batches_entry["textvariable"] = self.num_batches

        self.make_world_button = Button(text='Create World', command=self.bind_variables)
        self.make_world_button.grid(row=11)
        
        self.run_cycle_button = Button(text='Run Cycle', command=self.run_cycle)
        self.run_cycle_button.grid(row=11, column=1)
        
        self.run_to_extinction_button = Button(text='Run to Extinction', command=self.run_to_extinction)
        self.run_to_extinction_button.grid(row=12)
        
        self.run_batch_button = Button(text='Run Batch of Simulations', command=self.run_batch)
        self.run_batch_button.grid(row=12, column=1)
        
        self.cycles_complete = StringVar()
        self.cycles_complete.set("0")
        self.cycles_complete_label = Label(text=self.cycles_complete.get())
        self.cycles_complete_label.grid(row=13)
        
        self.simulations_complete = StringVar()
        self.simulations_complete.set("0")
        self.simulations_complete_label = Label(text=self.simulations_complete.get())
        self.simulations_complete_label.grid(row=13, column=1)
        

    def bind_variables(self):
        num_competitive_spiders = int(self.num_competitive_spiders.get())
        num_non_competitive_spiders = int(self.num_non_competitive_spiders.get())
        survival_rate = float(self.survival_rate.get())
        num_babies = int(self.num_babies.get())
        spider_radius = float(self.spider_radius.get())
        move_scale = float(self.spider_movement.get())
        competition_factor = float(self.competition_factor.get())
        max_age = int(self.max_age.get())
        cut_throat = self.cut_throat.get()
        
        spiders = originate(num_competitive_spiders=num_competitive_spiders, 
                            num_non_competitive_spiders=num_non_competitive_spiders, num_babies=num_babies)
        min_x, max_x, min_y, max_y = get_world_range(spiders)
        start_world = World(spiders, min_x, max_x, min_y, max_y, spider_radius, 0, survival_rate,
                            competition_factor, cut_throat, max_age, move_scale)
        start_world.print_world()
        self.world = start_world
        
    def run_cycle(self):
        cycles_complete = int(self.cycles_complete.get())
        self.world.run_cycle()
        self.cycles_complete.set(str(cycles_complete+1))
        
    def run_to_extinction(self):
        self.bind_variables()
        self.cycles_complete.set("0")
        counter = 0
        max_iterations = int(self.max_iterations.get())
        num_competitive_spiders = int(self.num_competitive_spiders.get())
        num_non_competitive_spiders = int(self.num_non_competitive_spiders.get())
        while counter < max_iterations and num_competitive_spiders>0 and num_non_competitive_spiders>0:
            self.world.run_cycle()
            num_competitive_spiders, num_non_competitive_spiders = get_spider_count(self.world.spiders)
            counter+=1
        if counter==max_iterations:
            if num_competitive_spiders>num_non_competitive_spiders:
                return 'competitive spiders won'
            elif num_non_competitive_spiders > num_competitive_spiders:
                return 'non-competitive spiders won'
            else:
                return 'stalemate'
        elif num_competitive_spiders==0 and num_non_competitive_spiders>0:
            return 'non-competitive spiders dominated'
        elif num_non_competitive_spiders==0 and num_competitive_spiders>0:
            return 'competitive spiders dominated'
        elif num_non_competitive_spiders==0 and num_competitive_spiders==0:
            return 'all spiders died'
        else:
            return 'error'
            
    def run_batch(self):
        num_batches = int(self.num_batches.get())
        stalemates = 0
        comp_wins = 0
        non_comp_wins = 0
        comp_dominations = 0
        non_comp_dominations=0
        all_dead = 0
        error = 0
        other_error = 0
        #sys.stdout = os.devnull
        for i in range(num_batches):
            result = self.run_to_extinction()
            if result=='stalemate':
                stalemates+=1
            elif result=='non-competitive spiders won':
                non_comp_wins+=1
            elif result=='competitive spiders won':
                comp_wins+=1
            elif result=='all spiders died':
                all_dead+=1
            elif result=='error':
                error+=1
            elif result=='non-competitive spiders dominated':
                non_comp_dominations+=1
            elif result=='competitive spiders dominated':
                comp_dominations+=1
            else:
                other_error+=1
                
        #sys.stdout = sys.__stdout__
        print str(stalemates) + ' stalemates'
        print str(comp_wins) + ' competitive spider wins'
        print str(non_comp_wins) + ' non-competitive spider wins'
        print str(comp_dominations) + ' competitive spider dominations'
        print str(non_comp_dominations) + ' non-competitive spider dominations'
        print str(error) + ' errors'
        print str(other_error) + ' other errors'
        
# create the application
root = Tk()
myapp = App()

#
# here are method calls to the window manager class
#
myapp.master.title("Spider Simulation")
myapp.master.maxsize(2000, 1000)

# start the program
myapp.mainloop()     
    
        
    